"""
Exercise Router
실습 과제 보기, 실습 과제 완료
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import schemas
import models
from database import get_db

router = APIRouter(prefix="/v1/exercise", tags=["exercise"])


@router.get("/{chapter_id}", response_model=schemas.ExerciseResponse)
def get_exercise(chapter_id: int, db: Session = Depends(get_db)):
    """
    실습 과제 보기
    해당 챕터의 실습 과제를 조회합니다.
    """
    # 챕터의 실습과제 조회
    exercise = db.query(models.Exercise).filter(models.Exercise.chapter_id == chapter_id).first()

    if not exercise:
        raise HTTPException(status_code=404, detail=f"Exercise for chapter {chapter_id} not found")

    return schemas.ExerciseResponse(
        id=exercise.id,
        chapter_id=exercise.chapter_id,
        question=exercise.question or "",
        difficulty=exercise.difficulty.value if exercise.difficulty else "medium",
        is_complete=exercise.is_complete or False
    )


@router.patch("/{chapter_id}", response_model=schemas.ExerciseCompleteResponse)
def complete_exercise(
    chapter_id: int,
    complete_data: schemas.ExerciseComplete,
    db: Session = Depends(get_db)
):
    """
    실습 과제 완료
    실습 과제 완료 여부를 업데이트합니다.
    """
    # 챕터의 실습과제 조회
    exercise = db.query(models.Exercise).filter(models.Exercise.chapter_id == chapter_id).first()

    if not exercise:
        raise HTTPException(status_code=404, detail=f"Exercise for chapter {chapter_id} not found")

    # 완료 상태 업데이트
    exercise.is_complete = complete_data.is_complete
    db.commit()

    return schemas.ExerciseCompleteResponse(
        chapter_id=chapter_id,
        is_complete=complete_data.is_complete,
        updated_at=datetime.utcnow()
    )
