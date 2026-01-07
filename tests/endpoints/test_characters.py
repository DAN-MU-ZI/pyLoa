"""CharactersEndpoint 테스트."""
import pytest
from unittest.mock import Mock
from pyloa.client import LostArkAPI
from pyloa.endpoints.characters import CharactersEndpoint
from pyloa.models.character import Character


def test_characters_endpoint_initialization():
    """CharactersEndpoint는 올바른 base_path를 가져야 합니다."""
    client = Mock(spec=LostArkAPI)
    endpoint = CharactersEndpoint(client)
    
    assert endpoint.base_path == "/characters"
    assert endpoint.client == client


def test_get_siblings():
    """get_siblings는 올바른 경로로 _request를 호출해야 합니다."""
    client = Mock(spec=LostArkAPI)
    endpoint = CharactersEndpoint(client)
    
    # Mock _request to return sample data
    endpoint._request = Mock(return_value=[
        {
            'ServerName': '아만',
            'CharacterName': '홍길동',
            'CharacterLevel': 60,
            'CharacterClassName': '버서커',
            'ItemAvgLevel': '1620.00',
            'ItemMaxLevel': '1625.00'
        },
        {
            'ServerName': '아만',
            'CharacterName': '김철수',
            'CharacterLevel': 60,
            'CharacterClassName': '소서리스',
            'ItemAvgLevel': '1615.83',
            'ItemMaxLevel': '1620.00'
        }
    ])
    
    siblings = endpoint.get_siblings("홍길동")
    
    # Should call _request with GET /홍길동/siblings
    endpoint._request.assert_called_once_with('GET', '/홍길동/siblings')
    
    # Should return list of Character objects
    assert len(siblings) == 2
    assert isinstance(siblings[0], Character)
    assert siblings[0].character_name == '홍길동'
    assert siblings[1].character_name == '김철수'


def test_get_siblings_url_encoding():
    """get_siblings는 공백이나 특수 문자가 포함된 캐릭터 이름을 처리해야 합니다."""
    client = Mock(spec=LostArkAPI)
    endpoint = CharactersEndpoint(client)
    endpoint._request = Mock(return_value=[])
    
    endpoint.get_siblings("테스트 캐릭터")
    
    # Path should include the name as-is (encoding handled by requests)
    endpoint._request.assert_called_once_with('GET', '/테스트 캐릭터/siblings')
