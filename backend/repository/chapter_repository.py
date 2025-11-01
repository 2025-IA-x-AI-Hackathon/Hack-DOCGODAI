"""
Chapter Repository
챕터 관련 데이터베이스 작업
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from repository.base_repository import BaseRepository
from models import Chapter


class ChapterRepository(BaseRepository[Chapter]):
    """챕터 Repository"""

    def __init__(self, db: Session):
        super().__init__(Chapter, db)

    def get_by_course(self, course_id: int, skip: int = 0, limit: int = 100) -> List[Chapter]:
        """
        코스별 챕터 조회

        Args:
            course_id: 코스 ID
            skip: 건너뛸 레코드 수
            limit: 최대 조회 수

        Returns:
            챕터 리스트
        """
        return self.db.query(Chapter).filter(
            Chapter.course_id == course_id
        ).order_by(Chapter.order_index).offset(skip).limit(limit).all()

    def get_active_by_course(self, course_id: int) -> List[Chapter]:
        """
        코스의 활성화된 챕터만 조회

        Args:
            course_id: 코스 ID

        Returns:
            활성 챕터 리스트
        """
        return self.db.query(Chapter).filter(
            and_(Chapter.course_id == course_id, Chapter.is_active == True)
        ).order_by(Chapter.order_index).all()

    def get_by_owner(self, owner_id: int, skip: int = 0, limit: int = 100) -> List[Chapter]:
        """
        소유자별 챕터 조회

        Args:
            owner_id: 소유자 ID
            skip: 건너뛸 레코드 수
            limit: 최대 조회 수

        Returns:
            챕터 리스트
        """
        return self.db.query(Chapter).filter(
            Chapter.owner_id == owner_id
        ).offset(skip).limit(limit).all()

    def update_order(self, chapter_id: int, new_order: int) -> Optional[Chapter]:
        """
        챕터 순서 변경

        Args:
            chapter_id: 챕터 ID
            new_order: 새로운 순서

        Returns:
            업데이트된 챕터 또는 None
        """
        return self.update(chapter_id, {"order_index": new_order})
