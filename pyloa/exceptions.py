"""Custom exceptions for pyLoa library."""


class PyLoaException(Exception):
    """Base exception for pyLoa library."""
    pass


class APIError(PyLoaException):
    """General API error."""
    pass


class RateLimitError(PyLoaException):
    """Rate limit exceeded error."""
    pass


class AuthenticationError(PyLoaException):
    """Authentication error (401 Unauthorized)."""
    pass
