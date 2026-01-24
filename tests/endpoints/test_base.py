"""BaseEndpoint 테스트."""

import pytest
from unittest.mock import Mock, MagicMock, patch
from requests import Response, HTTPError
from pyloa.client import LostArkAPI
from pyloa.endpoints.base import BaseEndpoint
from pyloa.exceptions import APIError, RateLimitError, AuthenticationError


class ConcreteEndpoint(BaseEndpoint):
    """테스트를 위한 구체적인 엔드포인트."""

    def __init__(self, client):
        super().__init__(client)
        self.base_path = "/test"


def test_endpoint_initialization():
    """BaseEndpoint는 클라이언트 참조를 저장해야 합니다."""
    client = Mock(spec=LostArkAPI)
    endpoint = ConcreteEndpoint(client)

    assert endpoint.client == client
    assert endpoint.base_path == "/test"


def test_request_makes_http_call():
    """_request는 올바른 URL로 HTTP 요청을 수행해야 합니다."""
    client = Mock(spec=LostArkAPI)
    client.base_url = "https://test.com"
    client.session = Mock()

    mock_response = Mock(spec=Response)
    mock_response.status_code = 200
    mock_response.headers = {}
    mock_response.json.return_value = {"data": "test"}
    client.session.request.return_value = mock_response

    endpoint = ConcreteEndpoint(client)
    result = endpoint._request("GET", "/path", params={"q": "value"})

    # Should call session.request with correct params
    client.session.request.assert_called_once_with(
        "GET", "https://test.com/test/path", params={"q": "value"}
    )
    assert result == {"data": "test"}


def test_request_raises_authentication_error_on_401():
    """_request는 401 발생 시 AuthenticationError를 발생시켜야 합니다."""
    client = Mock(spec=LostArkAPI)
    client.base_url = "https://test.com"
    client.session = Mock()

    mock_response = Mock(spec=Response)
    mock_response.status_code = 401
    mock_response.headers = {}
    mock_response.text = "Unauthorized"
    mock_response.raise_for_status.side_effect = HTTPError()
    client.session.request.return_value = mock_response

    endpoint = ConcreteEndpoint(client)

    with pytest.raises(AuthenticationError):
        endpoint._request("GET", "/path")


def test_request_raises_rate_limit_error_on_429():
    """_request는 429 발생 시 RateLimitError를 발생시켜야 합니다."""
    client = Mock(spec=LostArkAPI)
    client.base_url = "https://test.com"
    client.session = Mock()

    mock_response = Mock(spec=Response)
    mock_response.status_code = 429
    mock_response.headers = {}
    mock_response.text = "Too Many Requests"
    mock_response.raise_for_status.side_effect = HTTPError()
    client.session.request.return_value = mock_response

    endpoint = ConcreteEndpoint(client)

    with pytest.raises(RateLimitError):
        endpoint._request("GET", "/path")


def test_request_raises_api_error_on_4xx_5xx():
    """_request는 기타 오류 발생 시 APIError를 발생시켜야 합니다."""
    client = Mock(spec=LostArkAPI)
    client.base_url = "https://test.com"
    client.session = Mock()

    mock_response = Mock(spec=Response)
    mock_response.status_code = 500
    mock_response.headers = {}
    mock_response.text = "Internal Server Error"
    mock_response.raise_for_status.side_effect = HTTPError()
    client.session.request.return_value = mock_response

    endpoint = ConcreteEndpoint(client)

    with pytest.raises(APIError):
        endpoint._request("GET", "/path")
