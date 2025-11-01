"""
Pydantic Schemas for Request/Response models
"""

from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


# ============================================
# Member Schemas
# ============================================

class MemberSignup(BaseModel):
    email: EmailStr
    password: str


class MemberSignupResponse(BaseModel):
    id: int
    email: str
    created_at: datetime


class MemberLogin(BaseModel):
    email: EmailStr
    password: str


class MemberLoginResponse(BaseModel):
    access_token: str
    token_type: str
    member_id: int


class MemberInfoResponse(BaseModel):
    id: int
    email: str
    created_at: datetime


# ============================================
# Course Schemas
# ============================================

class CourseCreate(BaseModel):
    title: str
    description: str
    difficulty: str
    owner_id: int


class CourseResponse(BaseModel):
    id: int
    title: str
    description: str
    difficulty: str
    owner_id: int
    created_at: datetime


class ChapterBasic(BaseModel):
    id: int
    title: str


class CourseDetailResponse(BaseModel):
    id: int
    title: str
    description: str
    difficulty: str
    chapters: List[ChapterBasic]


# ============================================
# Chapter Schemas
# ============================================

class ChapterCreate(BaseModel):
    course_id: int
    title: str
    description: str
    owner_id: int


class ChapterCreateResponse(BaseModel):
    chapter_id: int
    concept_id: int
    exercise_id: int
    quiz_slots: List[int]
    created_at: datetime


class ConceptStatus(BaseModel):
    id: int
    is_complete: bool


class ExerciseStatus(BaseModel):
    id: int
    is_complete: bool


class QuizSlot(BaseModel):
    slot_number: int
    status: str  # pending, completed


class ChapterDetailResponse(BaseModel):
    id: int
    title: str
    description: str
    is_active: bool
    concept: ConceptStatus
    exercise: ExerciseStatus
    quiz: List[QuizSlot]


# ============================================
# Concept Schemas
# ============================================

class ConceptResponse(BaseModel):
    id: int
    chapter_id: int
    title: str
    content: str
    is_complete: bool


class ConceptComplete(BaseModel):
    is_complete: bool


class ConceptCompleteResponse(BaseModel):
    chapter_id: int
    is_complete: bool
    updated_at: datetime


# ============================================
# Exercise Schemas
# ============================================

class ExerciseResponse(BaseModel):
    id: int
    chapter_id: int
    question: str
    difficulty: str
    is_complete: bool


class ExerciseComplete(BaseModel):
    is_complete: bool


class ExerciseCompleteResponse(BaseModel):
    chapter_id: int
    is_complete: bool
    updated_at: datetime


# ============================================
# Quiz Schemas
# ============================================

class QuizItem(BaseModel):
    slot_number: int
    question: str
    options: Optional[List[str]] = None
    type: str  # multiple, short, boolean


class QuizSubmit(BaseModel):
    slot_number: int
    answer: str
    member_id: int


class QuizSubmitResponse(BaseModel):
    slot_number: int
    is_correct: bool
    explanation: str
    score: int


class QuizComplete(BaseModel):
    status: str  # completed


class QuizCompleteResponse(BaseModel):
    chapter_id: int
    status: str
    updated_at: datetime


class QuizResultResponse(BaseModel):
    chapter_id: int
    correct_count: int
    total: int
    score: int
    accuracy: float


class QuizRestartResponse(BaseModel):
    chapter_id: int
    reset_status: bool
    updated_at: datetime
