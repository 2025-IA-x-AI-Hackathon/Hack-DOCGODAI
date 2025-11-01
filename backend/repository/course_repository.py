"""
Course Repository
코스 관련 데이터베이스 작업
"""

from typing import List
from sqlalchemy.orm import Session
from repository.base_repository import BaseRepository
from models import Course, DifficultyEnum


class CourseRepository(BaseRepository[Course]):
    """코스 Repository"""

    def __init__(self, db: Session):
        super().__init__(Course, db)

    def get_by_owner(self, owner_id: int, skip: int = 0, limit: int = 100) -> List[Course]:
        """
        소유자별 코스 조회

        Args:
            owner_id: 소유자 ID
            skip: 건너뛸 레코드 수
            limit: 최대 조회 수

        Returns:
            코스 리스트
        """
        return self.db.query(Course).filter(
            Course.owner_id == owner_id
        ).offset(skip).limit(limit).all()

    def get_by_difficulty(self, difficulty: DifficultyEnum, skip: int = 0, limit: int = 100) -> List[Course]:
        """
        난이도별 코스 조회

        Args:
            difficulty: 난이도
            skip: 건너뛸 레코드 수
            limit: 최대 조회 수

        Returns:
            코스 리스트
        """
        return self.db.query(Course).filter(
            Course.difficulty == difficulty
        ).offset(skip).limit(limit).all()

    def search_by_title(self, keyword: str, skip: int = 0, limit: int = 100) -> List[Course]:
        """
        제목으로 코스 검색

        Args:
            keyword: 검색 키워드
            skip: 건너뛸 레코드 수
            limit: 최대 조회 수

        Returns:
            코스 리스트
        """
        return self.db.query(Course).filter(
            Course.title.like(f"%{keyword}%")
        ).offset(skip).limit(limit).all()
