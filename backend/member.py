"""
Member Router
회원가입, 로그인, 유저 정보 조회
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import timedelta
import schemas
import models
from database import get_db
from auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(prefix="/v1/member", tags=["member"])


@router.post("/signup", response_model=schemas.MemberSignupResponse)
def signup(member: schemas.MemberSignup, db: Session = Depends(get_db)):
    """
    회원가입
    새 사용자를 등록합니다.
    """
    # 이메일 중복 확인
    existing_member = db.query(models.Member).filter(models.Member.email == member.email).first()
    if existing_member:
        raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다.")

    # 비밀번호 해싱
    hashed_password = get_password_hash(member.password)

    # 회원 생성
    new_member = models.Member(
        email=member.email,
        password=hashed_password
    )

    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    return schemas.MemberSignupResponse(
        id=new_member.id,
        email=new_member.email,
        created_at=new_member.created_at
    )


@router.post("/login", response_model=schemas.MemberLoginResponse)
def login(member: schemas.MemberLogin, db: Session = Depends(get_db)):
    """
    로그인
    사용자 로그인 후 JWT 토큰을 발급합니다.
    """
    # 이메일로 회원 조회
    db_member = db.query(models.Member).filter(models.Member.email == member.email).first()
    if not db_member:
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다.")

    # 비밀번호 검증
    if not verify_password(member.password, db_member.password):
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다.")

    # JWT 토큰 생성
    access_token = create_access_token(
        data={"user_id": db_member.id, "email": db_member.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return schemas.MemberLoginResponse(
        access_token=access_token,
        token_type="bearer",
        member_id=db_member.id
    )


@router.get("/", response_model=schemas.MemberInfoResponse)
def get_member_info(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    유저 정보 조회
    로그인된 사용자 정보를 반환합니다.
    (헤더에 Authorization: Bearer <token> 필요)
    """
    member = db.query(models.Member).filter(models.Member.id == current_user["user_id"]).first()
    if not member:
        raise HTTPException(status_code=404, detail="회원 정보를 찾을 수 없습니다.")

    return schemas.MemberInfoResponse(
        id=member.id,
        email=member.email,
        created_at=member.created_at
    )
