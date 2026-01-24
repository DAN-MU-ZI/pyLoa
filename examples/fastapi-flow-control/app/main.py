"""FastAPI + SlowAPI를 활용한 Rate Limiting 예제.

이 모듈은 pyLoa 라이브러리를 멀티 프로세스 환경에서 안전하게
사용하기 위한 Redis 기반 유량 제어 패턴을 보여줍니다.
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from pyloa import LostArkAPI, RateLimitError, APIError


# Redis URL (docker-compose에서 주입)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# SlowAPI Limiter 설정 (Redis 기반)
limiter = Limiter(key_func=get_remote_address, storage_uri=REDIS_URL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 수명 주기 관리."""
    # 시작 시 API 클라이언트 초기화
    api_key = os.getenv("LOSTARK_API_KEY")
    if not api_key:
        raise ValueError("LOSTARK_API_KEY 환경 변수가 설정되지 않았습니다.")
    app.state.loa_api = LostArkAPI(api_key=api_key)
    yield
    # 종료 시 정리


app = FastAPI(
    title="pyLoa Rate Limiting Example",
    description="Redis 기반 유량 제어가 적용된 FastAPI 예제",
    lifespan=lifespan,
)

# SlowAPI 미들웨어 등록
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/")
async def root():
    """헬스 체크 엔드포인트."""
    return {"status": "ok"}


@app.get("/api/events")
@limiter.limit("100/minute")  # 분당 100회 제한 (로스트아크 API 제한과 동일)
async def get_events(request: Request):
    """진행 중인 이벤트 조회.

    SlowAPI가 분당 100회 요청으로 제한합니다.
    멀티 프로세스 환경에서도 Redis를 통해 전역적으로 제한이 적용됩니다.
    """
    api: LostArkAPI = request.app.state.loa_api
    try:
        events = api.news.get_events()
        return [
            {
                "title": event.title,
                "thumbnail": event.thumbnail,
                "link": event.link,
                "start_date": event.start_date,
                "end_date": event.end_date,
            }
            for event in events
        ]
    except RateLimitError:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    except APIError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/character/{character_name}")
@limiter.limit("100/minute")
async def get_character(request: Request, character_name: str):
    """캐릭터 기본 정보 조회."""
    api: LostArkAPI = request.app.state.loa_api
    try:
        siblings = api.characters.get_siblings(character_name)
        return [
            {
                "server_name": char.server_name,
                "character_name": char.character_name,
                "character_class": char.character_class_name,
                "item_level": char.item_avg_level,
            }
            for char in siblings
        ]
    except RateLimitError:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    except APIError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/test")
@limiter.limit("100/minute")
async def test_endpoint(request: Request):
    """Rate limiting 테스트용 엔드포인트."""
    return {"message": "Request successful"}
