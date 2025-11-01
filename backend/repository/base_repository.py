"""
Base Repository
모든 CRUD 작업의 기본 클래스
"""

from typing import List, Optional, TypeVar, Generic, Type, Dict, Any
from sqlalchemy.orm import Session

T = TypeVar('T')


class BaseRepository(Generic[T]):
    """기본 Repository 클래스 - 모든 CRUD 작업 제공"""

    def __init__(self, model: Type[T], db: Session):
        self.model = model
        self.db = db

    def create(self, obj_in: Dict[str, Any]) -> T:
        """
        새 레코드 생성

        Args:
            obj_in: 생성할 데이터 딕셔너리

        Returns:
            생성된 객체
        """
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def get(self, id: int) -> Optional[T]:
        """
        ID로 단일 레코드 조회

        Args:
            id: 조회할 ID

        Returns:
            조회된 객체 또는 None
        """
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, skip: int = 0, limit: int = 100) -> List[T]:
        """
        여러 레코드 조회 (페이징)

        Args:
            skip: 건너뛸 레코드 수
            limit: 최대 조회 수

        Returns:
            레코드 리스트
        """
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def update(self, id: int, obj_in: Dict[str, Any]) -> Optional[T]:
        """
        레코드 업데이트

        Args:
            id: 업데이트할 ID
            obj_in: 업데이트할 데이터 딕셔너리

        Returns:
            업데이트된 객체 또는 None
        """
        db_obj = self.get(id)
        if db_obj:
            for key, value in obj_in.items():
                if hasattr(db_obj, key):
                    setattr(db_obj, key, value)
            self.db.commit()
            self.db.refresh(db_obj)
        return db_obj

    def delete(self, id: int) -> bool:
        """
        레코드 삭제

        Args:
            id: 삭제할 ID

        Returns:
            삭제 성공 여부
        """
        db_obj = self.get(id)
        if db_obj:
            self.db.delete(db_obj)
            self.db.commit()
            return True
        return False

    def count(self) -> int:
        """
        전체 레코드 수 조회

        Returns:
            레코드 수
        """
        return self.db.query(self.model).count()
