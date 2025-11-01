"""
Member Repository
회원 관련 데이터베이스 작업
"""

from typing import Optional
from sqlalchemy.orm import Session
from repository.base_repository import BaseRepository
from models import Member


class MemberRepository(BaseRepository[Member]):
    """회원 Repository"""

    def __init__(self, db: Session):
        super().__init__(Member, db)

    def get_by_email(self, email: str) -> Optional[Member]:
        """
        이메일로 회원 조회

        Args:
            email: 조회할 이메일

        Returns:
            회원 객체 또는 None
        """
        return self.db.query(Member).filter(Member.email == email).first()

    def exists_by_email(self, email: str) -> bool:
        """
        이메일 존재 여부 확인

        Args:
            email: 확인할 이메일

        Returns:
            존재 여부
        """
        return self.db.query(Member).filter(Member.email == email).count() > 0
