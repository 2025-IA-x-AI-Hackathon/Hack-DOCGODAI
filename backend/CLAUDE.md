# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastAPI-based backend for an AI-powered learning platform (DOCGODAI) that generates personalized course content. The system integrates with N8N workflows and Gemini AI to automatically generate concepts, exercises, and quizzes for educational chapters.

## Architecture

### Core Components

**Database Layer (SQLAlchemy + MySQL)**
- `database.py`: Database connection setup, session management, and repository factory functions
- `models.py`: SQLAlchemy ORM models defining the database schema
- Environment variables required: `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME`

**Repository Pattern**
- `repository/base_repository.py`: Generic base repository with CRUD operations
- Specific repositories in `repository/`: `MemberRepository`, `CourseRepository`, `ChapterRepository`, `ConceptRepository`, `ExerciseRepository`, `QuizRepository`
- All repositories inherit from `BaseRepository[T]` and provide type-safe database operations

**Authentication (JWT)**
- `auth.py`: JWT token creation/validation, password hashing with bcrypt
- Functions: `verify_password()`, `get_password_hash()`, `create_access_token()`, `decode_access_token()`, `get_current_user()`
- Uses `SECRET_KEY` environment variable

**API Routes (FastAPI)**
- `course.py`: Course CRUD operations
- `chapter.py`: Chapter management with N8N/Gemini webhook integration
- `concept.py`: Concept summary viewing
- `exercise.py`: Exercise content and completion tracking
- All routes use dependency injection for database sessions via `Depends(get_db)`

### Data Model Hierarchy

```
Member (회원)
└── Course (강의)
    └── Chapter (챕터)
        ├── Concept (개념정리)
        ├── Exercise (실습과제)
        └── Quiz (형성평가)
```

**Key Relationships:**
- Each entity has `owner_id` FK to `member.id` for access control
- Chapters belong to courses via `course_id`
- Concepts, exercises, and quizzes belong to chapters via `chapter_id`
- All relationships use cascade delete (`cascade="all, delete-orphan"`)

### Event-Driven Architecture

**Kafka Integration** (referenced but implementation not in codebase):
- `send_course_created_event()`: Triggered when course is created
- `send_chapter_created_event()`: Triggers N8N workflow to generate AI content
- `send_concept_created_event()`, `send_exercise_created_event()`: Event notifications

**N8N Webhook Flow**:
1. Chapter created → Kafka event → N8N workflow triggered
2. N8N calls Gemini AI to generate content (concepts/exercises/quizzes)
3. N8N posts results back to webhook endpoints:
   - `POST /v1/chapter/{chapter_id}/concept-finish`
   - `POST /v1/chapter/{chapter_id}/exercise-finish`
   - `POST /v1/chapter/{chapter_id}/quiz-finish`
4. Webhooks save data to DB and emit Socket.IO events to frontend

**Socket.IO Integration** (referenced but implementation not in codebase):
- `emit_concept_finish()`, `emit_exercise_finish()`, `emit_quiz_finish()`: Real-time updates to connected clients

## Database Setup

Initialize database tables:
```python
from database import init_db
init_db()
```

Drop all tables (development only):
```python
from database import drop_db
drop_db()
```

## Development Patterns

### Using Repositories

Instead of direct SQLAlchemy queries, use repository pattern:

```python
from database import get_db, get_course_repository
from sqlalchemy.orm import Session

def some_function(db: Session = Depends(get_db)):
    course_repo = get_course_repository(db)
    course = course_repo.get(course_id)
    all_courses = course_repo.get_multi(skip=0, limit=10)
```

### Authentication in Routes

Protect routes with JWT authentication:

```python
from auth import get_current_user

@router.post("/")
def create_resource(
    data: schemas.ResourceCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # current_user contains: {"user_id": int, "email": str}
    pass
```

### JSON Fields in MySQL

The `Course.link` field stores JSON arrays as strings. Handle serialization:

```python
import json

# When creating
link_json = json.dumps(course.link)  # list → string
new_course = models.Course(link=link_json, ...)

# When reading
link_list = json.loads(course.link) if course.link else []
```

### Webhook Implementation Pattern

Webhooks from N8N should:
1. Validate chapter/resource exists
2. Save AI-generated data to database
3. Emit Socket.IO event for real-time updates
4. Return the webhook data back as confirmation
5. Use try/except with db.rollback() on errors

## Known TODOs in Codebase

- `course.py:24`: Implement completed chapter count calculation
- `course.py:99-100`: Add actual chapter generation status and completion tracking
- `chapter.py:77`: Implement automatic chapter ordering (order_num)
- Models may need additional fields for tracking AI generation status

## Important Notes

- Database uses MySQL with `pymysql` driver (connection string: `mysql+pymysql://...`)
- Connection pooling configured: pool_size=10, max_overflow=20, pool_recycle=3600
- All models have `created_at` and `updated_at` timestamps (UTC)
- The codebase has commented-out "old" endpoint implementations - these show evolution of API design
- Korean comments/docstrings are prevalent throughout the codebase
