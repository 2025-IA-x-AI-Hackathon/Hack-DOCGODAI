"""
N8N Webhook Client
Gemini를 호출하기 위한 N8N Webhook 클라이언트
"""

import os
import httpx
import json
from typing import Optional
import schemas

# N8N Webhook Base URL
N8N_BASE_URL = os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678/webhook")


async def call_concept_webhook(request_data: schemas.WebhookConceptRequest) -> Optional[schemas.WebhookConceptResponse]:
    """
    개념 정리 생성 Webhook 호출

    Args:
        request_data: 개념 정리 생성 요청 데이터

    Returns:
        WebhookConceptResponse 또는 None
    """
    url = f"{N8N_BASE_URL}/concept"

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                url,
                json=request_data.model_dump()
            )
            response.raise_for_status()

            # Response 처리 - "output:" 문자열이 앞에 있을 수 있음
            response_text = response.text.strip()
            if response_text.startswith("output:"):
                response_text = response_text[7:].strip()

            data = json.loads(response_text)
            return schemas.WebhookConceptResponse(**data)

    except Exception as e:
        print(f"Error calling concept webhook: {e}")
        return None


async def call_exercise_webhook(request_data: schemas.WebhookExerciseRequest) -> Optional[schemas.WebhookExerciseResponse]:
    """
    실습 생성 Webhook 호출

    Args:
        request_data: 실습 생성 요청 데이터

    Returns:
        WebhookExerciseResponse 또는 None
    """
    url = f"{N8N_BASE_URL}/exercise"

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                url,
                json=request_data.model_dump()
            )
            response.raise_for_status()

            # Response 처리 - "output:" 문자열이 앞에 있을 수 있음
            response_text = response.text.strip()
            if response_text.startswith("output:"):
                response_text = response_text[7:].strip()

            data = json.loads(response_text)
            return schemas.WebhookExerciseResponse(**data)

    except Exception as e:
        print(f"Error calling exercise webhook: {e}")
        return None


async def call_quiz_webhook(request_data: schemas.WebhookQuizRequest) -> Optional[schemas.WebhookQuizResponse]:
    """
    형성평가 생성 Webhook 호출

    Args:
        request_data: 형성평가 생성 요청 데이터

    Returns:
        WebhookQuizResponse 또는 None
    """
    url = f"{N8N_BASE_URL}/quiz"

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                url,
                json=request_data.model_dump()
            )
            response.raise_for_status()

            # Response 처리 - "output:" 문자열이 앞에 있을 수 있음
            response_text = response.text.strip()
            if response_text.startswith("output:"):
                response_text = response_text[7:].strip()

            data = json.loads(response_text)
            return schemas.WebhookQuizResponse(**data)

    except Exception as e:
        print(f"Error calling quiz webhook: {e}")
        return None


async def call_answer_webhook(request_data: schemas.WebhookAnswerRequest) -> Optional[schemas.WebhookAnswerResponse]:
    """
    퀴즈 정답 제출 Webhook 호출

    Args:
        request_data: 퀴즈 정답 제출 요청 데이터

    Returns:
        WebhookAnswerResponse 또는 None
    """
    url = f"{N8N_BASE_URL}/answer"

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                url,
                json=request_data.model_dump()
            )
            response.raise_for_status()

            # Response 처리 - "output:" 문자열이 앞에 있을 수 있음
            response_text = response.text.strip()
            if response_text.startswith("output:"):
                response_text = response_text[7:].strip()

            data = json.loads(response_text)
            return schemas.WebhookAnswerResponse(**data)

    except Exception as e:
        print(f"Error calling answer webhook: {e}")
        return None
