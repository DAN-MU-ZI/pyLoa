"""Tests for LostArkAPI client."""
import pytest
from unittest.mock import Mock, patch
from pyloa.client import LostArkAPI
from pyloa.rate_limiter import RateLimiter


def test_client_initialization():
    """Client should initialize with API key."""
    api = LostArkAPI(api_key="test_jwt_token")
    
    assert api.api_key == "test_jwt_token"
    assert api.base_url == "https://developer-lostark.game.onstove.com"


def test_client_creates_session_with_headers():
    """Client should create session with proper headers."""
    api = LostArkAPI(api_key="test_jwt_token")
    
    assert api.session is not None
    assert "authorization" in api.session.headers
    assert api.session.headers["authorization"] == "bearer test_jwt_token"
    assert api.session.headers["accept"] == "application/json"


def test_client_initializes_rate_limiter():
    """Client should create RateLimiter instance."""
    api = LostArkAPI(api_key="test_jwt_token")
    
    assert isinstance(api.rate_limiter, RateLimiter)
    assert api.rate_limiter.limit == 100
    assert api.rate_limiter.remaining == 100


def test_api_key_is_required():
    """Client should require API key."""
    with pytest.raises(TypeError):
        LostArkAPI()


def test_api_key_immutable():
    """API key should not be modifiable after initialization."""
    api = LostArkAPI(api_key="test_jwt_token")
    
    # Should raise AttributeError when trying to set
    with pytest.raises(AttributeError):
        api.api_key = "new_key"
