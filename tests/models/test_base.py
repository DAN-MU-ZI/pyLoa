"""BaseModel 테스트."""
import pytest
from dataclasses import dataclass
from typing import Optional
from pyloa.models.base import BaseModel


@dataclass
class SampleModel(BaseModel):
    """테스트를 위한 샘플 모델."""
    server_name: str
    character_name: str
    item_avg_level: str
    character_level: Optional[int] = None


def test_from_dict_basic():
    """BaseModel은 딕셔너리를 객체로 변환해야 합니다."""
    data = {
        'ServerName': '아만',
        'CharacterName': '홍길동',
        'ItemAvgLevel': '1620.00'
    }
    
    model = SampleModel.from_dict(data)
    
    assert model.server_name == '아만'
    assert model.character_name == '홍길동'
    assert model.item_avg_level == '1620.00'


def test_from_dict_with_optional_field():
    """BaseModel은 선택적 필드를 처리해야 합니다."""
    data = {
        'ServerName': '아만',
        'CharacterName': '홍길동',
        'ItemAvgLevel': '1620.00',
        'CharacterLevel': 60
    }
    
    model = SampleModel.from_dict(data)
    
    assert model.character_level == 60


def test_from_dict_missing_optional_field():
    """BaseModel은 누락된 선택적 필드를 처리해야 합니다."""
    data = {
        'ServerName': '아만',
        'CharacterName': '홍길동',
        'ItemAvgLevel': '1620.00'
    }
    
    model = SampleModel.from_dict(data)
    
    assert model.character_level is None


def test_to_dict():
    """BaseModel은 객체를 딕셔너리로 변환해야 합니다."""
    model = SampleModel(
        server_name='아만',
        character_name='홍길동',
        item_avg_level='1620.00',
        character_level=60
    )
    
    data = model.to_dict()
    
    assert data['server_name'] == '아만'
    assert data['character_name'] == '홍길동'
    assert data['item_avg_level'] == '1620.00'
    assert data['character_level'] == 60


def test_from_dict_snake_case_input():
    """BaseModel은 snake_case 입력도 수락해야 합니다."""
    data = {
        'server_name': '아만',
        'character_name': '홍길동',
        'item_avg_level': '1620.00'
    }
    
    model = SampleModel.from_dict(data)
    
    assert model.server_name == '아만'
    assert model.character_name == '홍길동'


def test_roundtrip():
    """BaseModel은 왕복 변환(roundtrip)을 지원해야 합니다."""
    original_data = {
        'ServerName': '아만',
        'CharacterName': '홍길동',
        'ItemAvgLevel': '1620.00'
    }
    
    model = SampleModel.from_dict(original_data)
    converted_data = model.to_dict()
    
    # Should be able to recreate the model
    model2 = SampleModel.from_dict(converted_data)
    assert model2.server_name == model.server_name
    assert model2.character_name == model.character_name


# Negative test cases
def test_from_dict_with_non_dataclass():
    """BaseModel은 비-dataclass에 대해 TypeError를 발생시켜야 합니다."""
    class NonDataclass(BaseModel):
        pass
    
    with pytest.raises(TypeError, match="must be a dataclass"):
        NonDataclass.from_dict({'test': 'value'})


def test_from_dict_missing_required_field():
    """BaseModel은 필수 필드가 누락된 경우 TypeError를 발생시켜야 합니다."""
    data = {
        'ServerName': '아만',
        # CharacterName is missing
        'ItemAvgLevel': '1620.00'
    }
    
    with pytest.raises(TypeError):
        SampleModel.from_dict(data)


def test_from_dict_empty_data():
    """BaseModel은 빈 딕셔너리에 대해 TypeError를 발생시켜야 합니다."""
    with pytest.raises(TypeError):
        SampleModel.from_dict({})
