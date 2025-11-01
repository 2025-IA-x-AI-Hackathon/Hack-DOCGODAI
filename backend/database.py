"""
데이터베이스 연결 설정
SQLAlchemy를 사용한 MySQL 연결
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from typing import Generator
import os

# 환경 변수에서 데이터베이스 설정 가져오기
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "your_database_name")

# 데이터베이스 URL 생성
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

# SQLAlchemy 엔진 생성
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,  # 커넥션 풀 크기
    max_overflow=20,  # 최대 추가 커넥션
    pool_pre_ping=True,  # 연결 상태 확인
    pool_recycle=3600,  # 1시간마다 커넥션 재생성
    echo=False,  # SQL 로그 출력 (개발 시 True로 설정)
)

# SessionLocal 클래스 생성
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db() -> Generator[Session, None, None]:
    """
    데이터베이스 세션 의존성
    FastAPI Depends에서 사용

    Usage:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            ...

    Yields:
        Session: 데이터베이스 세션
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    데이터베이스 초기화
    모든 테이블 생성

    Usage:
        from database import init_db
        init_db()
    """
    from models import Base
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


def drop_db():
    """
    모든 테이블 삭제 (주의: 개발 환경에서만 사용)

    Usage:
        from database import drop_db
        drop_db()
    """
    from models import Base
    Base.metadata.drop_all(bind=engine)
    print("All database tables dropped!")
