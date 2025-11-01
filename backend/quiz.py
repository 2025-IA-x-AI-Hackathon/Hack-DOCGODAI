"""
Quiz Router
퀴즈 목록 조회, 퀴즈 풀이 제출, 형성평가 채점 완료, 결과 보기, 다시 풀기
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

import schemas
from database import get_db
from repository import QuizRepository
from models import Quiz

router = APIRouter(prefix="/v1/quiz", tags=["quiz"])


@router.get("/{chapter_id}", response_model=List[schemas.QuizItem])
def get_quiz_list(
    chapter_id: int,
    db: Session = Depends(get_db)
):
    """
    퀴즈 목록 조회
    챕터에 속한 3개의 퀴즈(slot 1~3)를 조회합니다.
    """
    repo = QuizRepository(db)

    # 챕터의 퀴즈 조회
    quizzes = repo.get_by_chapter(chapter_id, limit=3)

    if not quizzes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"챕터 ID {chapter_id}의 퀴즈를 찾을 수 없습니다."
        )

    # 퀴즈 리스트 생성
    quiz_items = []
    for i, quiz in enumerate(quizzes, start=1):
        # options가 JSON 형태로 저장되어 있다면 파싱
        options = None
        if quiz.options:
            if isinstance(quiz.options, list):
                options = quiz.options
            elif isinstance(quiz.options, str):
                import json
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


@router.post("/{chapter_id}", response_model=schemas.QuizSubmitResponse)
def submit_quiz_answer(
    chapter_id: int,
    submit_data: schemas.QuizSubmitRequest,
    db: Session = Depends(get_db)
):
    """
    퀴즈 풀이 제출
    특정 슬롯 퀴즈에 대한 답안을 제출합니다.
    """
    repo = QuizRepository(db)

    # 챕터의 퀴즈 조회
    quizzes = repo.get_by_chapter(chapter_id, limit=3)

    if not quizzes or len(quizzes) < submit_data.slot_number:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"슬롯 {submit_data.slot_number}의 퀴즈를 찾을 수 없습니다."
        )

    # 해당 슬롯의 퀴즈
    quiz = quizzes[submit_data.slot_number - 1]

    # 정답 확인
    is_correct = (submit_data.answer.strip().lower() == quiz.correct_answer.strip().lower())

    # 점수 계산 (각 문제당 10점)
    score = 10 if is_correct else 0

    # TODO: 사용자별 퀴즈 제출 결과를 별도 테이블에 저장
    # quiz_submission_repo.create({
    #     "quiz_id": quiz.id,
    #     "member_id": submit_data.member_id,
    #     "answer": submit_data.answer,
    #     "is_correct": is_correct,
    #     "score": score
    # })

    return schemas.QuizSubmitResponse(
        slot_number=submit_data.slot_number,
        is_correct=is_correct,
        explanation=quiz.explanation or "설명이 없습니다.",
        score=score
    )


@router.patch("/{chapter_id}", response_model=schemas.QuizCompleteResponse)
def complete_quiz_evaluation(
    chapter_id: int,
    complete_data: schemas.QuizCompleteRequest,
    db: Session = Depends(get_db)
):
    """
    형성평가 채점 완료
    챕터의 퀴즈 채점을 완료 상태로 변경합니다.
    """
    repo = QuizRepository(db)

    # 챕터의 퀴즈 조회
    quizzes = repo.get_by_chapter(chapter_id)

    if not quizzes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"챕터 ID {chapter_id}의 퀴즈를 찾을 수 없습니다."
        )

    # TODO: 챕터별 퀴즈 완료 상태를 별도로 관리해야 할 수 있음
    # 현재는 각 퀴즈에 is_complete 플래그가 없으므로 확장 필요

    return schemas.QuizCompleteResponse(
        chapter_id=chapter_id,
        status=complete_data.status,
        updated_at=datetime.utcnow()
    )


@router.get("/result/{chapter_id}", response_model=schemas.QuizResultResponse)
def get_quiz_result(
    chapter_id: int,
    db: Session = Depends(get_db)
):
    """
    결과 보기
    퀴즈 점수 및 정답률을 조회합니다.
    """
    repo = QuizRepository(db)

    # 챕터의 퀴즈 조회
    quizzes = repo.get_by_chapter(chapter_id, limit=3)

    if not quizzes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"챕터 ID {chapter_id}의 퀴즈 결과를 찾을 수 없습니다."
        )

    # TODO: 실제로는 quiz_submission 테이블에서 사용자의 제출 결과를 조회해야 함
    # 현재는 더미 데이터 반환
    total = len(quizzes)
    correct_count = 0  # TODO: 실제 정답 개수 계산
    score = 0  # TODO: 실제 점수 계산
    accuracy = correct_count / total if total > 0 else 0.0

    return schemas.QuizResultResponse(
        chapter_id=chapter_id,
        correct_count=correct_count,
        total=total,
        score=score,
        accuracy=accuracy
    )


@router.post("/restart/{chapter_id}", response_model=schemas.QuizRestartResponse)
def restart_quiz(
    chapter_id: int,
    db: Session = Depends(get_db)
):
    """
    다시 풀기
    기존 채점 결과를 초기화하고 퀴즈를 다시 풀 수 있게 합니다.
    """
    repo = QuizRepository(db)

    # 챕터의 퀴즈 조회
    quizzes = repo.get_by_chapter(chapter_id)

    if not quizzes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"챕터 ID {chapter_id}의 퀴즈를 찾을 수 없습니다."
        )

    # TODO: quiz_submission 테이블에서 해당 챕터의 모든 제출 결과 삭제
    # quiz_submission_repo.delete_by_chapter(chapter_id)

    return schemas.QuizRestartResponse(
        chapter_id=chapter_id,
        reset_status=True,
        updated_at=datetime.utcnow()
    )
