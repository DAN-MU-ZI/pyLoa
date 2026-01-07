"""Tests for ArmoriesEndpoint."""
import pytest
from unittest.mock import Mock
from pyloa.client import LostArkAPI
from pyloa.endpoints.armories import ArmoriesEndpoint
from pyloa.models.armory import ArmoryProfile, ArmoryEquipment


def test_armories_endpoint_initialization():
    """Endpoint should have correct base_path."""
    client = Mock(spec=LostArkAPI)
    endpoint = ArmoriesEndpoint(client)
    
    assert endpoint.base_path == "/armories/characters"
    assert endpoint.client == client


def test_get_profile():
    """get_profile should call GET /profiles."""
    client = Mock(spec=LostArkAPI)
    endpoint = ArmoriesEndpoint(client)
    endpoint._request = Mock(return_value={
        'CharacterImage': '...',
        'ExpeditionLevel': 300,
        'CharacterName': '테스트',
        # ... minimal fields for test
    })
    
    # Mock return value needs to satisfy from_dict if we test full object
    # But here we just want to verify the call
    # Let's mock the return to be a simpler dict and mock from_dict if needed
    # Or just use minimal satisfying data
    endpoint._request = Mock(return_value={
        'CharacterImage': 'img',
        'ExpeditionLevel': 100,
        'PvpGradeName': '1급',
        'TownLevel': 50,
        'TownName': '영지',
        'Title': '타이틀',
        'GuildMemberGrade': '길드장',
        'GuildName': '길드',
        'Stats': [],
        'Tendencies': [],
        'ServerName': '서버',
        'CharacterName': '캐릭',
        'CharacterLevel': 60,
        'CharacterClassName': '클래스',
        'ItemAvgLevel': '1600.00',
        'ItemMaxLevel': '1600.00'
    })
    
    profile = endpoint.get_profile("테스트캐릭")
    
    endpoint._request.assert_called_once_with('GET', '/테스트캐릭/profiles')
    assert isinstance(profile, ArmoryProfile)
    assert profile.character_name == '캐릭'


def test_get_equipment():
    """get_equipment should call GET /equipment and return list."""
    client = Mock(spec=LostArkAPI)
    endpoint = ArmoriesEndpoint(client)
    endpoint._request = Mock(return_value=[{
        'Type': '무기',
        'Name': '무기',
        'Icon': 'icon',
        'Grade': '고대',
        'Tooltip': '{}'
    }])
    
    eqs = endpoint.get_equipment("테스트캐릭")
    
    endpoint._request.assert_called_once_with('GET', '/테스트캐릭/equipment')
    assert len(eqs) == 1
    assert isinstance(eqs[0], ArmoryEquipment)


def test_get_avatars():
    """get_avatars should call GET /avatars."""
    client = Mock(spec=LostArkAPI)
    endpoint = ArmoriesEndpoint(client)
    endpoint._request = Mock(return_value=[{'Type': '무기 아바타', 'Name': '아바타', 'Icon': '...', 'Grade': '전설', 'IsSet': False, 'IsInner': False, 'Tooltip': '...'}])
    
    avatars = endpoint.get_avatars("테스트캐릭")
    
    endpoint._request.assert_called_once_with('GET', '/테스트캐릭/avatars')
    assert len(avatars) == 1
    assert avatars[0].type == '무기 아바타'


def test_get_combat_skills():
    """get_combat_skills should call GET /combat-skills."""
    client = Mock(spec=LostArkAPI)
    endpoint = ArmoriesEndpoint(client)
    endpoint._request = Mock(return_value=[{'Name': '스킬', 'Icon': '...', 'Level': 12, 'Type': '일반', 'IsAwake': False, 'Tooltip': '...'}])
    
    skills = endpoint.get_combat_skills("테스트캐릭")
    
    endpoint._request.assert_called_once_with('GET', '/테스트캐릭/combat-skills')
    assert len(skills) == 1
    assert skills[0].name == '스킬'


def test_get_engravings():
    """get_engravings should call GET /engravings."""
    client = Mock(spec=LostArkAPI)
    endpoint = ArmoriesEndpoint(client)
    endpoint._request = Mock(return_value={'Engravings': [], 'Effects': []})
    
    engravings = endpoint.get_engravings("테스트캐릭")
    
    endpoint._request.assert_called_once_with('GET', '/테스트캐릭/engravings')
    assert engravings is not None


def test_get_cards():
    """get_cards should call GET /cards."""
    client = Mock(spec=LostArkAPI)
    endpoint = ArmoriesEndpoint(client)
    endpoint._request = Mock(return_value={'Cards': [], 'Effects': []})
    
    cards = endpoint.get_cards("테스트캐릭")
    
    endpoint._request.assert_called_once_with('GET', '/테스트캐릭/cards')
    assert cards is not None


def test_get_gems():
    """get_gems should call GET /gems."""
    client = Mock(spec=LostArkAPI)
    endpoint = ArmoriesEndpoint(client)
    endpoint._request = Mock(return_value={'Gems': [], 'Effects': []})
    
    gems = endpoint.get_gems("테스트캐릭")
    
    endpoint._request.assert_called_once_with('GET', '/테스트캐릭/gems')
    assert gems is not None


def test_get_colosseums():
    """get_colosseums should call GET /colosseums."""
    client = Mock(spec=LostArkAPI)
    endpoint = ArmoriesEndpoint(client)
    endpoint._request = Mock(return_value={'Rank': 1, 'PreRank': 1, 'Exp': 100, 'Colosseums': []})
    
    colosseums = endpoint.get_colosseums("테스트캐릭")
    
    endpoint._request.assert_called_once_with('GET', '/테스트캐릭/colosseums')
    assert colosseums is not None


def test_get_collectibles():
    """get_collectibles should call GET /collectibles."""
    client = Mock(spec=LostArkAPI)
    endpoint = ArmoriesEndpoint(client)
    endpoint._request = Mock(return_value=[{'Type': '모코코', 'Icon': '...', 'Point': 10, 'MaxPoint': 100, 'CollectiblePoints': []}])
    
    collectibles = endpoint.get_collectibles("테스트캐릭")
    
    endpoint._request.assert_called_once_with('GET', '/테스트캐릭/collectibles')
    assert len(collectibles) == 1
    assert collectibles[0].type == '모코코'


def test_get_ark_passive():
    """get_ark_passive should call GET /arkpassive."""
    client = Mock(spec=LostArkAPI)
    endpoint = ArmoriesEndpoint(client)
    endpoint._request = Mock(return_value={'IsOpen': True, 'Points': [], 'Effects': []})
    
    passive = endpoint.get_ark_passive("테스트캐릭")
    
    endpoint._request.assert_called_once_with('GET', '/테스트캐릭/arkpassive')
    assert passive is not None
    assert passive.is_open is True
