"""Tests for RateLimiter."""
import pytest
from datetime import datetime, timedelta
from unittest.mock import patch
from pyloa.rate_limiter import RateLimiter


def test_rate_limiter_initialization():
    """RateLimiter should initialize with default values."""
    limiter = RateLimiter()
    assert limiter.limit == 100
    assert limiter.remaining == 100
    assert limiter.reset_time is None


def test_update_from_headers():
    """RateLimiter should update from response headers."""
    limiter = RateLimiter()
    
    # Simulate response headers
    future_time = datetime.now() + timedelta(seconds=60)
    headers = {
        'X-RateLimit-Limit': '100',
        'X-RateLimit-Remaining': '95',
        'X-RateLimit-Reset': str(int(future_time.timestamp()))
    }
    
    limiter.update(headers)
    
    assert limiter.limit == 100
    assert limiter.remaining == 95
    assert limiter.reset_time is not None


def test_get_wait_duration_returns_zero_when_remaining():
    """get_wait_duration should return 0.0 when requests remain."""
    limiter = RateLimiter()
    limiter.remaining = 50
    limiter.reset_time = datetime.now() + timedelta(seconds=60)
    
    assert limiter.get_wait_duration() == 0.0


def test_get_wait_duration_returns_seconds_when_limited():
    """get_wait_duration should return remaining seconds when limit exceeded."""
    limiter = RateLimiter()
    limiter.remaining = 0
    # Set reset time to 5 seconds in the future
    limiter.reset_time = datetime.now() + timedelta(seconds=5)
    
    duration = limiter.get_wait_duration()
    assert 4.0 < duration <= 5.0


def test_get_wait_duration_returns_zero_after_reset():
    """get_wait_duration should return 0.0 if reset time has passed."""
    limiter = RateLimiter()
    limiter.remaining = 0
    limiter.reset_time = datetime.now() - timedelta(seconds=10)  # Past time
    
    assert limiter.get_wait_duration() == 0.0


def test_get_wait_duration_returns_zero_without_reset_time():
    """get_wait_duration should return 0.0 if reset_time is not set."""
    limiter = RateLimiter()
    limiter.remaining = 0
    limiter.reset_time = None
    
    assert limiter.get_wait_duration() == 0.0
