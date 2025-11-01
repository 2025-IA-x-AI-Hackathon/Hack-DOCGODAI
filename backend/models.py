"""
SQLAlchemy 데이터베이스 모델
ㅁㅁ.sql 스키마를 기반으로 생성됨
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum, ForeignKey, JSON
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()


class DifficultyEnum(str, enum.Enum):
    """난이도 열거형"""
    easy = "easy"
    medium = "medium"
    hard = "hard"


class QuizTypeEnum(str, enum.Enum):
    """퀴즈 유형 열거형"""
    multiple = "multiple"
    short = "short"
    boolean = "boolean"


class Member(Base):
    """회원 모델"""
    __tablename__ = "member"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    courses = relationship("Course", back_populates="owner", cascade="all, delete-orphan")
    chapters = relationship("Chapter", back_populates="owner", cascade="all, delete-orphan")
    concepts = relationship("Concept", back_populates="owner", cascade="all, delete-orphan")
    exercises = relationship("Exercise", back_populates="owner", cascade="all, delete-orphan")
    quizzes = relationship("Quiz", back_populates="owner", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Member(id={self.id}, email={self.email})>"


class Course(Base):
    """코스 모델"""
    __tablename__ = "course"

    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("member.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    difficulty = Column(Enum(DifficultyEnum), default=DifficultyEnum.medium)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    owner = relationship("Member", back_populates="courses")
    chapters = relationship("Chapter", back_populates="course", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Course(id={self.id}, title={self.title}, owner_id={self.owner_id})>"


class Chapter(Base):
    """챕터 모델"""
    __tablename__ = "chapter"

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)
    owner_id = Column(Integer, ForeignKey("member.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    order_index = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    course = relationship("Course", back_populates="chapters")
    owner = relationship("Member", back_populates="chapters")
    concepts = relationship("Concept", back_populates="chapter", cascade="all, delete-orphan")
    exercises = relationship("Exercise", back_populates="chapter", cascade="all, delete-orphan")
    quizzes = relationship("Quiz", back_populates="chapter", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Chapter(id={self.id}, title={self.title}, course_id={self.course_id})>"


class Concept(Base):
    """개념 모델"""
    __tablename__ = "concept"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chapter_id = Column(Integer, ForeignKey("chapter.id"), nullable=False)
    owner_id = Column(Integer, ForeignKey("member.id"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(LONGTEXT, nullable=False)
    is_complete = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    chapter = relationship("Chapter", back_populates="concepts")
    owner = relationship("Member", back_populates="concepts")

    def __repr__(self):
        return f"<Concept(id={self.id}, title={self.title}, chapter_id={self.chapter_id})>"


class Exercise(Base):
    """연습문제 모델"""
    __tablename__ = "exercise"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chapter_id = Column(Integer, ForeignKey("chapter.id"), nullable=False)
    owner_id = Column(Integer, ForeignKey("member.id"), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    explanation = Column(Text, nullable=True)
    difficulty = Column(Enum(DifficultyEnum), default=DifficultyEnum.medium)
    is_complete = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    chapter = relationship("Chapter", back_populates="exercises")
    owner = relationship("Member", back_populates="exercises")

    def __repr__(self):
        return f"<Exercise(id={self.id}, chapter_id={self.chapter_id})>"


class Quiz(Base):
    """퀴즈 모델"""
    __tablename__ = "quiz"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chapter_id = Column(Integer, ForeignKey("chapter.id"), nullable=False)
    owner_id = Column(Integer, ForeignKey("member.id"), nullable=False)
    question = Column(Text, nullable=False)
    options = Column(JSON, nullable=True)
    correct_answer = Column(String(255), nullable=False)
    explanation = Column(Text, nullable=True)
    type = Column(Enum(QuizTypeEnum), default=QuizTypeEnum.multiple)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    chapter = relationship("Chapter", back_populates="quizzes")
    owner = relationship("Member", back_populates="quizzes")

    def __repr__(self):
        return f"<Quiz(id={self.id}, chapter_id={self.chapter_id}, type={self.type})>"
