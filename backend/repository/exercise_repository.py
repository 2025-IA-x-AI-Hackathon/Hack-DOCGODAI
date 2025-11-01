"""
Exercise Repository
연습문제 관련 데이터베이스 작업
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from repository.base_repository import BaseRepository
from models import Exercise, DifficultyEnum


class ExerciseRepository(BaseRepository[Exercise]):
    """연습문제 Repository"""

    def __init__(self, db: Session):
        super().__init__(Exercise, db)

    def get_by_chapter(self, chapter_id: int, skip: int = 0, limit: int = 100) -> List[Exercise]:
        """
        챕터별 연습문제 조회

        Args:
            chapter_id: 챕터 ID
            skip: 건너뛸 레코드 수
            limit: 최대 조회 수

        Returns:
            연습문제 리스트
        """
        return self.db.query(Exercise).filter(
            Exercise.chapter_id == chapter_id
        ).offset(skip).limit(limit).all()

    def get_by_difficulty(self, chapter_id: int, difficulty: DifficultyEnum) -> List[Exercise]:
        """
        챕터 내 난이도별 연습문제 조회

        Args:
            chapter_id: 챕터 ID
            difficulty: 난이도

        Returns:
            연습문제 리스트
        """
        return self.db.query(Exercise).filter(
            and_(Exercise.chapter_id == chapter_id, Exercise.difficulty == difficulty)
        ).all()

    def get_incomplete_by_chapter(self, chapter_id: int) -> List[Exercise]:
        """
        챕터의 미완료 연습문제만 조회

        Args:
            chapter_id: 챕터 ID

        Returns:
            미완료 연습문제 리스트
        """
        return self.db.query(Exercise).filter(
            and_(Exercise.chapter_id == chapter_id, Exercise.is_complete == False)
        ).all()

    def mark_complete(self, exercise_id: int) -> Optional[Exercise]:
        """
        연습문제 완료 표시

        Args:
            exercise_id: 연습문제 ID

        Returns:
            업데이트된 연습문제 또는 None
        """
        return self.update(exercise_id, {"is_complete": True})
