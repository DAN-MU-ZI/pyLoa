"""Tests for BaseEndpoint."""
import pytest
from unittest.mock import Mock, MagicMock, patch
from requests import Response, HTTPError
from pyloa.client import LostArkAPI
from pyloa.endpoints.base import BaseEndpoint
from pyloa.exceptions import APIError, RateLimitError, AuthenticationError


class ConcreteEndpoint(BaseEndpoint):
    """Concrete endpoint for testing."""
    def __init__(self, client):
        super().__init__(client)
        self.base_path = "/test"


def test_endpoint_initialization():
    """BaseEndpoint should store client reference."""
    client = Mock(spec=LostArkAPI)
    endpoint = ConcreteEndpoint(client)
    
    assert endpoint.client == client
    assert endpoint.base_path == "/test"


def test_request_calls_rate_limiter():
    """_request should check rate limiter before making request."""
    client = Mock(spec=LostArkAPI)
    client.base_url = "https://test.com"
    client.rate_limiter = Mock()
    client.session = Mock()
    
    # Mock successful response
    mock_response = Mock(spec=Response)
    mock_response.status_code = 200
    mock_response.headers = {}
    mock_response.json.return_value = {"data": "test"}
    client.session.request.return_value = mock_response
    
    endpoint = ConcreteEndpoint(client)
    endpoint._request('GET', '/path')
    
    # Should call wait_if_needed
    client.rate_limiter.wait_if_needed.assert_called_once()


def test_request_makes_http_call():
    """_request should make HTTP request with correct URL."""
    client = Mock(spec=LostArkAPI)
    client.base_url = "https://test.com"
    client.rate_limiter = Mock()
    client.session = Mock()
    
    mock_response = Mock(spec=Response)
    mock_response.status_code = 200
    mock_response.headers = {}
    mock_response.json.return_value = {"data": "test"}
    client.session.request.return_value = mock_response
    
    endpoint = ConcreteEndpoint(client)
    result = endpoint._request('GET', '/path', params={'q': 'value'})
    
    # Should call session.request with correct params
    client.session.request.assert_called_once_with(
        'GET',
        'https://test.com/test/path',
        params={'q': 'value'}
    )
    assert result == {"data": "test"}


def test_request_updates_rate_limiter():
    """_request should update rate limiter from response headers."""
    client = Mock(spec=LostArkAPI)
    client.base_url = "https://test.com"
    client.rate_limiter = Mock()
    client.session = Mock()
    
    mock_response = Mock(spec=Response)
    mock_response.status_code = 200
    mock_response.headers = {
        'X-RateLimit-Remaining': '95'
    }
    mock_response.json.return_value = {"data": "test"}
    client.session.request.return_value = mock_response
    
    endpoint = ConcreteEndpoint(client)
    endpoint._request('GET', '/path')
    
    # Should update rate limiter
    client.rate_limiter.update.assert_called_once_with(mock_response.headers)


def test_request_raises_authentication_error_on_401():
    """_request should raise AuthenticationError on 401."""
    client = Mock(spec=LostArkAPI)
    client.base_url = "https://test.com"
    client.rate_limiter = Mock()
    client.session = Mock()
    
    mock_response = Mock(spec=Response)
    mock_response.status_code = 401
    mock_response.headers = {}  # Add headers
    mock_response.text = "Unauthorized"
    mock_response.raise_for_status.side_effect = HTTPError()
    client.session.request.return_value = mock_response
    
    endpoint = ConcreteEndpoint(client)
    
    with pytest.raises(AuthenticationError):
        endpoint._request('GET', '/path')


def test_request_raises_rate_limit_error_on_429():
    """_request should raise RateLimitError on 429."""
    client = Mock(spec=LostArkAPI)
    client.base_url = "https://test.com"
    client.rate_limiter = Mock()
    client.session = Mock()
    
    mock_response = Mock(spec=Response)
    mock_response.status_code = 429
    mock_response.headers = {}  # Add headers
    mock_response.text = "Too Many Requests"
    mock_response.raise_for_status.side_effect = HTTPError()
    client.session.request.return_value = mock_response
    
    endpoint = ConcreteEndpoint(client)
    
    with pytest.raises(RateLimitError):
        endpoint._request('GET', '/path')


def test_request_raises_api_error_on_4xx_5xx():
    """_request should raise APIError on other errors."""
    client = Mock(spec=LostArkAPI)
    client.base_url = "https://test.com"
    client.rate_limiter = Mock()
    client.session = Mock()
    
    mock_response = Mock(spec=Response)
    mock_response.status_code = 500
    mock_response.headers = {}  # Add headers
    mock_response.text = "Internal Server Error"
    mock_response.raise_for_status.side_effect = HTTPError()
    client.session.request.return_value = mock_response
    
    endpoint = ConcreteEndpoint(client)
    
    with pytest.raises(APIError):
        endpoint._request('GET', '/path')
