"""GameContentsEndpoint 테스트."""
import pytest
from unittest.mock import Mock
from pyloa.client import LostArkAPI
from pyloa.endpoints.game_contents import GameContentsEndpoint
from pyloa.models.game_content import ContentsCalendar


def test_game_contents_endpoint_initialization():
    """Endpoint는 올바른 base_path를 가져야 합니다."""
    client = Mock(spec=LostArkAPI)
    endpoint = GameContentsEndpoint(client)
    
    assert endpoint.base_path == "/gamecontents"
    assert endpoint.client == client


def test_get_calendar():
    """get_calendar는 GET /calendar를 호출해야 합니다."""
    client = Mock(spec=LostArkAPI)
    endpoint = GameContentsEndpoint(client)
    endpoint._request = Mock(return_value=[{
        'CategoryName': '필드 보스',
        'ContentsName': '모아케',
        'ContentsIcon': '...',
        'MinItemLevel': 1415,
        'StartTimes': [],
        'Location': '파푸니카',
        'RewardItems': []
    }])
    
    result = endpoint.get_calendar()
    
    endpoint._request.assert_called_once_with('GET', '/calendar')
    assert len(result) == 1
    assert isinstance(result[0], ContentsCalendar)
    assert result[0].contents_name == '모아케'
