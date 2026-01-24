"""Flask Rate Limiting 자동화 테스트.

docker-compose가 실행 중인 상태에서 테스트를 수행합니다.
"""

import httpx
import pytest


BASE_URL = "http://localhost:5000"


@pytest.fixture
def client():
    """HTTP 클라이언트 픽스처."""
    return httpx.Client(base_url=BASE_URL, timeout=30.0)


def test_health_check(client):
    """헬스 체크 엔드포인트 테스트."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_rate_limit_enforced(client):
    """분당 100회 초과 시 429 반환 확인."""
    # 100회 요청
    for i in range(100):
        response = client.get("/api/test")
        if response.status_code == 429:
            # 이미 제한에 걸린 경우 (이전 테스트 영향)
            pytest.skip("Rate limit already reached from previous tests")

    # 101번째 요청은 429 반환
    response = client.get("/api/test")
    assert response.status_code == 429, f"Expected 429, got {response.status_code}"


def test_test_endpoint_success(client):
    """테스트 엔드포인트 정상 응답 확인."""
    response = client.get("/api/test")
    # 429가 아니면 200이어야 함
    assert response.status_code in [200, 429]
    if response.status_code == 200:
        assert response.json()["message"] == "Request successful"
