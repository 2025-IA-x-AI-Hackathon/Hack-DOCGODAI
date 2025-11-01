"""
Concept Repository
개념 관련 데이터베이스 작업
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from repository.base_repository import BaseRepository
from models import Concept


class ConceptRepository(BaseRepository[Concept]):
    """개념 Repository"""

    def __init__(self, db: Session):
        super().__init__(Concept, db)

    def get_by_chapter(self, chapter_id: int, skip: int = 0, limit: int = 100) -> List[Concept]:
        """
        챕터별 개념 조회

        Args:
            chapter_id: 챕터 ID
            skip: 건너뛸 레코드 수
            limit: 최대 조회 수

        Returns:
            개념 리스트
        """
        return self.db.query(Concept).filter(
            Concept.chapter_id == chapter_id
        ).offset(skip).limit(limit).all()

    def get_completed_by_chapter(self, chapter_id: int) -> List[Concept]:
        """
        챕터의 완료된 개념만 조회

        Args:
            chapter_id: 챕터 ID

        Returns:
            완료된 개념 리스트
        """
        return self.db.query(Concept).filter(
            and_(Concept.chapter_id == chapter_id, Concept.is_complete == True)
        ).all()

    def mark_complete(self, concept_id: int) -> Optional[Concept]:
        """
        개념 완료 표시

        Args:
            concept_id: 개념 ID

        Returns:
            업데이트된 개념 또는 None
        """
        return self.update(concept_id, {"is_complete": True})
