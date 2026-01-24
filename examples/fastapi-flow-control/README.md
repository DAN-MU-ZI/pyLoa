# FastAPI Rate Limiting 예제

pyLoa 라이브러리를 FastAPI + SlowAPI + Redis 환경에서 사용하는 예제입니다.

## 구조

```
fastapi-flow-control/
├── docker-compose.yml  # FastAPI + Redis 컨테이너
├── Dockerfile          # FastAPI 앱 빌드
├── requirements.txt    # 의존성
├── app/
│   └── main.py         # SlowAPI 기반 rate limiting 적용
├── test_rate_limit.py  # 자동화 테스트
└── README.md           # 본 문서
```

## 실행 방법

### 1. 환경 변수 설정

```bash
# .env 파일 생성
echo "LOSTARK_API_KEY=your_jwt_token_here" > .env
```

### 2. Docker Compose 실행

```bash
docker-compose up -d
```

### 3. API 테스트

```bash
# 이벤트 조회
curl http://localhost:8000/api/events

# 캐릭터 조회
curl http://localhost:8000/api/character/캐릭터명

# Rate limit 테스트
curl http://localhost:8000/api/test
```

## Rate Limiting 동작 방식

1. **SlowAPI**: FastAPI용 rate limiting 라이브러리
2. **Redis**: 멀티 프로세스 간 상태 공유 (요청 카운트)
3. **분당 100회**: 로스트아크 API 제한과 동일하게 설정

```python
@limiter.limit("100/minute")  # 분당 100회 제한
async def get_events(request: Request):
    ...
```

## 자동화 테스트

```bash
# 테스트 실행 (docker-compose 실행 상태에서)
pip install pytest httpx
pytest test_rate_limit.py -v
```

## 참고

- [SlowAPI 문서](https://github.com/laurentS/slowapi)
- [Redis 공식 사이트](https://redis.io/)
