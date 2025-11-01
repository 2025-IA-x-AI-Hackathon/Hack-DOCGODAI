"""
Quiz Repository
퀴즈 관련 데이터베이스 작업
"""

from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.sql.expression import func
from repository.base_repository import BaseRepository
from models import Quiz, QuizTypeEnum


class QuizRepository(BaseRepository[Quiz]):
    """퀴즈 Repository"""

    def __init__(self, db: Session):
        super().__init__(Quiz, db)

    def get_by_chapter(self, chapter_id: int, skip: int = 0, limit: int = 100) -> List[Quiz]:
        """
        챕터별 퀴즈 조회

        Args:
            chapter_id: 챕터 ID
            skip: 건너뛸 레코드 수
            limit: 최대 조회 수

        Returns:
            퀴즈 리스트
        """
        return self.db.query(Quiz).filter(
            Quiz.chapter_id == chapter_id
        ).offset(skip).limit(limit).all()

    def get_by_type(self, chapter_id: int, quiz_type: QuizTypeEnum) -> List[Quiz]:
        """
        챕터 내 유형별 퀴즈 조회

        Args:
            chapter_id: 챕터 ID
            quiz_type: 퀴즈 유형

        Returns:
            퀴즈 리스트
        """
        return self.db.query(Quiz).filter(
            and_(Quiz.chapter_id == chapter_id, Quiz.type == quiz_type)
        ).all()

    def get_random_quizzes(self, chapter_id: int, limit: int = 10) -> List[Quiz]:
        """
        챕터의 랜덤 퀴즈 조회

        Args:
            chapter_id: 챕터 ID
            limit: 최대 조회 수

        Returns:
            랜덤 퀴즈 리스트
        """
        return self.db.query(Quiz).filter(
            Quiz.chapter_id == chapter_id
        ).order_by(func.random()).limit(limit).all()
