"""Flask + Flask-Limiter를 활용한 Rate Limiting 예제.

이 모듈은 pyLoa 라이브러리를 멀티 프로세스 환경에서 안전하게
사용하기 위한 Redis 기반 유량 제어 패턴을 보여줍니다.
"""

import os
from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from pyloa import LostArkAPI, RateLimitError, APIError


# Flask 앱 초기화
app = Flask(__name__)

# Redis URL (docker-compose에서 주입)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Flask-Limiter 설정 (Redis 기반)
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    storage_uri=REDIS_URL,
    default_limits=["100 per minute"],  # 기본 제한: 분당 100회
)

# API 클라이언트 초기화
api_key = os.getenv("LOSTARK_API_KEY")
if api_key:
    loa_api = LostArkAPI(api_key=api_key)
else:
    loa_api = None


@app.route("/")
def root():
    """헬스 체크 엔드포인트."""
    return jsonify({"status": "ok"})


@app.route("/api/events")
@limiter.limit("100/minute")  # 분당 100회 제한
def get_events():
    """진행 중인 이벤트 조회.

    Flask-Limiter가 분당 100회 요청으로 제한합니다.
    멀티 프로세스 환경에서도 Redis를 통해 전역적으로 제한이 적용됩니다.
    """
    if not loa_api:
        return jsonify({"error": "LOSTARK_API_KEY not configured"}), 500

    try:
        events = loa_api.news.get_events()
        return jsonify(
            [
                {
                    "title": event.title,
                    "thumbnail": event.thumbnail,
                    "link": event.link,
                    "start_date": event.start_date,
                    "end_date": event.end_date,
                }
                for event in events
            ]
        )
    except RateLimitError:
        return jsonify({"error": "Rate limit exceeded"}), 429
    except APIError as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/character/<character_name>")
@limiter.limit("100/minute")
def get_character(character_name: str):
    """캐릭터 기본 정보 조회."""
    if not loa_api:
        return jsonify({"error": "LOSTARK_API_KEY not configured"}), 500

    try:
        siblings = loa_api.characters.get_siblings(character_name)
        return jsonify(
            [
                {
                    "server_name": char.server_name,
                    "character_name": char.character_name,
                    "character_class": char.character_class_name,
                    "item_level": char.item_avg_level,
                }
                for char in siblings
            ]
        )
    except RateLimitError:
        return jsonify({"error": "Rate limit exceeded"}), 429
    except APIError as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/test")
@limiter.limit("100/minute")
def test_endpoint():
    """Rate limiting 테스트용 엔드포인트."""
    return jsonify({"message": "Request successful"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
