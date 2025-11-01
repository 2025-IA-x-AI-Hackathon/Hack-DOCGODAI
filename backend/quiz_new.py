"""
Quiz Router
퀴즈 목록 조회, 퀴즈 풀이 제출, 형성평가 채점 완료, 결과 보기, 다시 풀기
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import json
import schemas
import models
from database import get_db
from kafka_producer import send_quiz_answer_submit_event

router = APIRouter(prefix="/v1/quiz", tags=["quiz"])


@router.get("/{chapter_id}", response_model=List[schemas.QuizItem])
def get_quiz_list(chapter_id: int, db: Session = Depends(get_db)):
    """
    퀴즈 목록 조회
    챕터에 속한 3개의 퀴즈(slot 1~3)를 조회합니다.
    """
    # 챕터의 퀴즈 조회 (최대 3개)
    quizzes = db.query(models.Quiz).filter(models.Quiz.chapter_id == chapter_id).limit(3).all()

    if not quizzes:
        raise HTTPException(status_code=404, detail=f"Quiz for chapter {chapter_id} not found")

    # 퀴즈 리스트 생성
    quiz_items = []
    for i, quiz in enumerate(quizzes, start=1):
        # options가 JSON으로 저장되어 있다면 파싱
        options = None
        if quiz.options:
            if isinstance(quiz.options, list):
                options = quiz.options
            elif isinstance(quiz.options, str):
                try:
                    options = json.loads(quiz.options)
                except:
                    options = None

        quiz_items.append(
            schemas.QuizItem(
                slot_number=i,
                question=quiz.question or "",
                options=options,
                type=quiz.type.value if quiz.type else "multiple"
            )
        )

    return quiz_items


@router.post("/{chapter_id}")
def submit_quiz_answer(
    chapter_id: int,
    submit_data: schemas.QuizSubmit,
    db: Session = Depends(get_db)
):
    """
    퀴즈 풀이 제출 (비동기 처리)

    흐름:
    1. 즉시 응답 반환 (status: submitted)
    2. Kafka 이벤트 발행 → N8N → Gemini 채점
    3. Webhook으로 결과 수신 → Socket.IO로 클라이언트에게 알림

    Returns:
        즉시 응답: { "status": "submitted", "message": "..." }
    """
    # 챕터 및 코스 정보 조회
    chapter = db.query(models.Chapter).filter(models.Chapter.id == chapter_id).first()
    if not chapter:
        raise HTTPException(status_code=404, detail=f"Chapter {chapter_id} not found")

    course = db.query(models.Course).filter(models.Course.id == chapter.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail=f"Course not found")

    # 퀴즈 조회
    quizzes = db.query(models.Quiz).filter(models.Quiz.chapter_id == chapter_id).limit(3).all()
    if not quizzes or len(quizzes) < submit_data.slot_number:
        raise HTTPException(
            status_code=404,
            detail=f"Quiz slot {submit_data.slot_number} for chapter {chapter_id} not found"
        )

    # 해당 슬롯의 퀴즈
    quiz = quizzes[submit_data.slot_number - 1]

    # Kafka 이벤트 발행 (비동기 처리)
    send_quiz_answer_submit_event(
        chapter_id=chapter_id,
        quiz_id=quiz.id,
        slot_number=submit_data.slot_number,
        member_id=submit_data.member_id,
        course_title=course.title,
        course_description=course.description or "",
        quiz_question=quiz.question or "",
        user_answer=submit_data.answer
    )

    # 즉시 응답 반환 (리턴 1)
    return {
        "status": "submitted",
        "message": "답안이 제출되었습니다. 채점 결과는 실시간으로 전송됩니다.",
        "chapter_id": chapter_id,
        "quiz_id": quiz.id,
        "slot_number": submit_data.slot_number
    }


@router.patch("/{chapter_id}", response_model=schemas.QuizCompleteResponse)
def complete_quiz_evaluation(
    chapter_id: int,
    complete_data: schemas.QuizComplete,
    db: Session = Depends(get_db)
):
    """
    형성평가 채점 완료
    챕터의 퀴즈 채점을 완료 상태로 변경합니다.
    """
    # 챕터의 퀴즈 조회
    quizzes = db.query(models.Quiz).filter(models.Quiz.chapter_id == chapter_id).all()

    if not quizzes:
        raise HTTPException(status_code=404, detail=f"Quiz for chapter {chapter_id} not found")

    # TODO: 챕터별 퀴즈 완료 상태를 별도 테이블에서 관리
    # chapter_quiz_status = models.ChapterQuizStatus(
    #     chapter_id=chapter_id,
    #     status=complete_data.status
    # )
    # db.add(chapter_quiz_status)
    # db.commit()

    return schemas.QuizCompleteResponse(
        chapter_id=chapter_id,
        status=complete_data.status,
        updated_at=datetime.utcnow()
    )


@router.get("/result/{chapter_id}", response_model=schemas.QuizResultResponse)
def get_quiz_result(chapter_id: int, db: Session = Depends(get_db)):
    """
    결과 보기
    퀴즈 점수 및 정답률을 조회합니다.
    """
    # 챕터의 퀴즈 조회
    quizzes = db.query(models.Quiz).filter(models.Quiz.chapter_id == chapter_id).limit(3).all()

    if not quizzes:
        raise HTTPException(status_code=404, detail=f"Quiz for chapter {chapter_id} not found")

    # TODO: quiz_submission 테이블에서 실제 제출 결과 조회
    # submissions = db.query(models.QuizSubmission).filter(
    #     models.QuizSubmission.quiz_id.in_([q.id for q in quizzes])
    # ).all()
    # correct_count = sum(1 for s in submissions if s.is_correct)
    # total_score = sum(s.score for s in submissions)

    # 임시 데이터 (실제로는 submission 테이블에서 가져와야 함)
    total = len(quizzes)
    correct_count = 0  # TODO: 실제 정답 개수
    score = 0  # TODO: 실제 점수
    accuracy = correct_count / total if total > 0 else 0.0

    return schemas.QuizResultResponse(
        chapter_id=chapter_id,
        correct_count=correct_count,
        total=total,
        score=score,
        accuracy=accuracy
    )


@router.post("/restart/{chapter_id}", response_model=schemas.QuizRestartResponse)
def restart_quiz(chapter_id: int, db: Session = Depends(get_db)):
    """
    다시 풀기
    기존 채점 결과를 초기화하고 퀴즈를 다시 풀 수 있게 합니다.
    """
    # 챕터의 퀴즈 조회
    quizzes = db.query(models.Quiz).filter(models.Quiz.chapter_id == chapter_id).all()

    if not quizzes:
        raise HTTPException(status_code=404, detail=f"Quiz for chapter {chapter_id} not found")

    # TODO: quiz_submission 테이블에서 해당 챕터의 모든 제출 결과 삭제
    # db.query(models.QuizSubmission).filter(
    #     models.QuizSubmission.quiz_id.in_([q.id for q in quizzes])
    # ).delete(synchronize_session=False)
    # db.commit()

    return schemas.QuizRestartResponse(
        chapter_id=chapter_id,
        reset_status=True,
        updated_at=datetime.utcnow()
    )
