"""
Pydantic Schemas for Request/Response models
"""

from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


# ============================================
# Member Schemas
# ============================================

class MemberSignupRequest(BaseModel):
    """회원가입 요청"""
    email: EmailStr
    password: str


class MemberSignupResponse(BaseModel):
    """회원가입 응답"""
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class MemberLoginRequest(BaseModel):
    """로그인 요청"""
    email: EmailStr
    password: str


class MemberLoginResponse(BaseModel):
    """로그인 응답"""
    access_token: str
    token_type: str = "bearer"
    member_id: int


class MemberInfoResponse(BaseModel):
    """유저 정보 응답"""
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================
# Course Schemas
# ============================================

class ChapterBasic(BaseModel):
    """챕터 기본 정보"""
    id: int
    title: str


class CourseListItem(BaseModel):
    """강의 리스트 아이템"""
    id: int
    title: str
    description: str
    difficulty: str
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class CourseCreateRequest(BaseModel):
    """강의 생성 요청"""
    title: str
    description: str
    difficulty: str
    owner_id: int


class CourseCreateResponse(BaseModel):
    """강의 생성 응답"""
    id: int
    title: str
    description: str
    difficulty: str
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class CourseDetailResponse(BaseModel):
    """강의 상세 응답"""
    id: int
    title: str
    description: str
    difficulty: str
    chapters: List[ChapterBasic]

    class Config:
        from_attributes = True


# ============================================
# Chapter Schemas
# ============================================

class ChapterCreateRequest(BaseModel):
    """챕터 생성 요청"""
    course_id: int
    title: str
    description: str
    owner_id: int


class ChapterCreateResponse(BaseModel):
    """챕터 생성 응답"""
    chapter_id: int
    concept_id: int
    exercise_id: int
    quiz_slots: List[int] = [1, 2, 3]
    created_at: datetime


class QuizSlotStatus(BaseModel):
    """퀴즈 슬롯 상태"""
    slot_number: int
    status: str  # pending, completed


class ChapterConceptStatus(BaseModel):
    """챕터의 개념 상태"""
    id: int
    is_complete: bool


class ChapterExerciseStatus(BaseModel):
    """챕터의 실습 상태"""
    id: int
    is_complete: bool


class ChapterDetailResponse(BaseModel):
    """챕터 상세 응답"""
    id: int
    title: str
    description: str
    is_active: bool
    concept: ChapterConceptStatus
    exercise: ChapterExerciseStatus
    quiz: List[QuizSlotStatus]


# ============================================
# Concept Schemas
# ============================================

class ConceptDetailResponse(BaseModel):
    """개념 정리 조회 응답"""
    id: int
    chapter_id: int
    title: str
    content: str
    is_complete: bool

    class Config:
        from_attributes = True


class ConceptCompleteRequest(BaseModel):
    """개념 학습 완료 요청"""
    is_complete: bool


class ConceptCompleteResponse(BaseModel):
    """개념 학습 완료 응답"""
    chapter_id: int
    is_complete: bool
    updated_at: datetime


# ============================================
# Exercise Schemas
# ============================================

class ExerciseDetailResponse(BaseModel):
    """실습 과제 조회 응답"""
    id: int
    chapter_id: int
    question: str
    difficulty: str
    is_complete: bool

    class Config:
        from_attributes = True


class ExerciseCompleteRequest(BaseModel):
    """실습 과제 완료 요청"""
    is_complete: bool


class ExerciseCompleteResponse(BaseModel):
    """실습 과제 완료 응답"""
    chapter_id: int
    is_complete: bool
    updated_at: datetime


# ============================================
# Quiz Schemas
# ============================================

class QuizItem(BaseModel):
    """퀴즈 아이템"""
    slot_number: int
    question: str
    options: Optional[List[str]] = None
    type: str  # multiple, short, boolean


class QuizSubmitRequest(BaseModel):
    """퀴즈 풀이 제출 요청"""
    slot_number: int
    answer: str
    member_id: int


class QuizSubmitResponse(BaseModel):
    """퀴즈 풀이 제출 응답"""
    slot_number: int
    is_correct: bool
    explanation: str
    score: int


class QuizCompleteRequest(BaseModel):
    """형성평가 채점 완료 요청"""
    status: str  # completed


class QuizCompleteResponse(BaseModel):
    """형성평가 채점 완료 응답"""
    chapter_id: int
    status: str
    updated_at: datetime


class QuizResultResponse(BaseModel):
    """퀴즈 결과 응답"""
    chapter_id: int
    correct_count: int
    total: int
    score: int
    accuracy: float


class QuizRestartResponse(BaseModel):
    """퀴즈 다시 풀기 응답"""
    chapter_id: int
    reset_status: bool
    updated_at: datetime
