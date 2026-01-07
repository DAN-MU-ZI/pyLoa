"""Character 모델 테스트."""
import pytest
from pyloa.models.character import Character


def test_character_from_dict_basic():
    """Character는 API 응답 형식에서 변환되어야 합니다."""
    data = {
        'ServerName': '아만',
        'CharacterName': '홍길동',
        'CharacterLevel': 60,
        'CharacterClassName': '버서커',
        'ItemAvgLevel': '1620.00',
        'ItemMaxLevel': '1625.00'
    }
    
    character = Character.from_dict(data)
    
    assert character.server_name == '아만'
    assert character.character_name == '홍길동'
    assert character.character_level == 60
    assert character.character_class_name == '버서커'
    assert character.item_avg_level == '1620.00'
    assert character.item_max_level == '1625.00'


def test_character_to_dict():
    """Character는 딕셔너리로 변환되어야 합니다."""
    character = Character(
        server_name='아만',
        character_name='홍길동',
        character_level=60,
        character_class_name='버서커',
        item_avg_level='1620.00',
        item_max_level='1625.00'
    )
    
    data = character.to_dict()
    
    assert data['server_name'] == '아만'
    assert data['character_name'] == '홍길동'
    assert data['character_level'] == 60
    assert data['character_class_name'] == '버서커'
    assert data['item_avg_level'] == '1620.00'
    assert data['item_max_level'] == '1625.00'
