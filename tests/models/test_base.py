"""Tests for BaseModel."""
import pytest
from dataclasses import dataclass
from typing import Optional
from pyloa.models.base import BaseModel


@dataclass
class SampleModel(BaseModel):
    """Sample model for testing."""
    server_name: str
    character_name: str
    item_avg_level: str
    character_level: Optional[int] = None


def test_from_dict_basic():
    """BaseModel should convert dict to object."""
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
    """BaseModel should handle optional fields."""
    data = {
        'ServerName': '아만',
        'CharacterName': '홍길동',
        'ItemAvgLevel': '1620.00',
        'CharacterLevel': 60
    }
    
    model = SampleModel.from_dict(data)
    
    assert model.character_level == 60


def test_from_dict_missing_optional_field():
    """BaseModel should handle missing optional fields."""
    data = {
        'ServerName': '아만',
        'CharacterName': '홍길동',
        'ItemAvgLevel': '1620.00'
    }
    
    model = SampleModel.from_dict(data)
    
    assert model.character_level is None


def test_to_dict():
    """BaseModel should convert object to dict."""
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
    """BaseModel should also accept snake_case input."""
    data = {
        'server_name': '아만',
        'character_name': '홍길동',
        'item_avg_level': '1620.00'
    }
    
    model = SampleModel.from_dict(data)
    
    assert model.server_name == '아만'
    assert model.character_name == '홍길동'


def test_roundtrip():
    """BaseModel should support roundtrip conversion."""
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
    """BaseModel should raise TypeError for non-dataclass."""
    class NonDataclass(BaseModel):
        pass
    
    with pytest.raises(TypeError, match="must be a dataclass"):
        NonDataclass.from_dict({'test': 'value'})


def test_from_dict_missing_required_field():
    """BaseModel should raise TypeError when required field is missing."""
    data = {
        'ServerName': '아만',
        # CharacterName is missing
        'ItemAvgLevel': '1620.00'
    }
    
    with pytest.raises(TypeError):
        SampleModel.from_dict(data)


def test_from_dict_empty_data():
    """BaseModel should raise TypeError for empty dict."""
    with pytest.raises(TypeError):
        SampleModel.from_dict({})
