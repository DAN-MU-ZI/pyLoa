"""Tests for custom exceptions."""
import pytest
from pyloa.exceptions import (
    PyLoaException,
    APIError,
    RateLimitError,
    AuthenticationError,
)


def test_pyloa_exception_is_exception():
    """PyLoaException should inherit from Exception."""
    assert issubclass(PyLoaException, Exception)


def test_pyloa_exception_instantiation():
    """PyLoaException should be instantiable with a message."""
    exc = PyLoaException("Test error")
    assert str(exc) == "Test error"


def test_api_error_inheritance():
    """APIError should inherit from PyLoaException."""
    assert issubclass(APIError, PyLoaException)


def test_rate_limit_error_inheritance():
    """RateLimitError should inherit from PyLoaException."""
    assert issubclass(RateLimitError, PyLoaException)


def test_authentication_error_inheritance():
    """AuthenticationError should inherit from PyLoaException."""
    assert issubclass(AuthenticationError, PyLoaException)


def test_exceptions_can_be_raised():
    """All custom exceptions should be raisable."""
    with pytest.raises(PyLoaException):
        raise PyLoaException("base error")
    
    with pytest.raises(APIError):
        raise APIError("api error")
    
    with pytest.raises(RateLimitError):
        raise RateLimitError("rate limit error")
    
    with pytest.raises(AuthenticationError):
        raise AuthenticationError("auth error")
