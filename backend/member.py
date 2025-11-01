"""
Member Router
회원가입, 로그인, 유저 정보 조회
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

import schemas
from database import get_db
from repository import MemberRepository
from auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(prefix="/v1/member", tags=["member"])


@router.post("/signup", response_model=schemas.MemberSignupResponse, status_code=status.HTTP_201_CREATED)
def signup(
    member_data: schemas.MemberSignupRequest,
    db: Session = Depends(get_db)
):
    """
    회원가입
    새 사용자를 등록합니다.
    """
    repo = MemberRepository(db)

    # 이메일 중복 확인
    if repo.exists_by_email(member_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 등록된 이메일입니다."
        )

    # 비밀번호 해싱
    hashed_password = get_password_hash(member_data.password)

    # 회원 생성
    new_member = repo.create({
        "email": member_data.email,
        "password": hashed_password
    })

    return schemas.MemberSignupResponse(
        id=new_member.id,
        email=new_member.email,
        created_at=new_member.created_at
    )


@router.post("/login", response_model=schemas.MemberLoginResponse)
def login(
    login_data: schemas.MemberLoginRequest,
    db: Session = Depends(get_db)
):
    """
    로그인
    사용자 로그인 후 JWT 토큰을 발급합니다.
    """
    repo = MemberRepository(db)

    # 이메일로 회원 조회
    member = repo.get_by_email(login_data.email)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다."
        )

    # 비밀번호 검증
    if not verify_password(login_data.password, member.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다."
        )

    # JWT 토큰 생성
    access_token = create_access_token(
        data={
            "user_id": member.id,
            "email": member.email
        },
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return schemas.MemberLoginResponse(
        access_token=access_token,
        token_type="bearer",
        member_id=member.id
    )


@router.get("/", response_model=schemas.MemberInfoResponse)
def get_member_info(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    유저 정보 조회
    로그인된 사용자 정보를 반환합니다.
    (헤더에 Authorization: Bearer <token> 필요)
    """
    repo = MemberRepository(db)

    member = repo.get(current_user["user_id"])
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="회원 정보를 찾을 수 없습니다."
        )

    return schemas.MemberInfoResponse(
        id=member.id,
        email=member.email,
        created_at=member.created_at
    )
