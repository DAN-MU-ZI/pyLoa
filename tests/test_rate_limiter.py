"""Tests for RateLimiter."""
import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
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


def test_wait_if_needed_does_not_wait_when_remaining():
    """wait_if_needed should not wait when requests remain."""
    limiter = RateLimiter()
    limiter.remaining = 50
    
    # Should return immediately without sleeping
    with patch('time.sleep') as mock_sleep:
        limiter.wait_if_needed()
        mock_sleep.assert_not_called()


def test_wait_if_needed_waits_when_limit_exceeded():
    """wait_if_needed should wait when rate limit is exceeded."""
    limiter = RateLimiter()
    limiter.remaining = 0
    limiter.reset_time = datetime.now() + timedelta(seconds=2)
    
    with patch('pyloa.rate_limiter.sleep') as mock_sleep:
        limiter.wait_if_needed()
        # Should have called sleep with a positive duration
        assert mock_sleep.called
        sleep_duration = mock_sleep.call_args[0][0]
        assert sleep_duration > 0


def test_wait_if_needed_does_not_wait_after_reset():
    """wait_if_needed should not wait if reset time has passed."""
    limiter = RateLimiter()
    limiter.remaining = 0
    limiter.reset_time = datetime.now() - timedelta(seconds=10)  # Past time
    
    with patch('time.sleep') as mock_sleep:
        limiter.wait_if_needed()
        mock_sleep.assert_not_called()


def test_partial_header_update():
    """RateLimiter should handle partial headers gracefully."""
    limiter = RateLimiter()
    
    # Only some headers present
    headers = {
        'X-RateLimit-Remaining': '42'
    }
    
    limiter.update(headers)
    assert limiter.remaining == 42
    assert limiter.limit == 100  # Should remain default
