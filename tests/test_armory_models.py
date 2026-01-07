"""Tests for Armory models."""
import pytest
from pyloa.models.armory import ArmoryProfile, ArmoryEquipment


def test_armory_profile_from_dict():
    """ArmoryProfile should convert from API response."""
    data = {
        'CharacterImage': 'https://...',
        'ExpeditionLevel': 300,
        'PvpGradeName': '1급',
        'TownLevel': 70,
        'TownName': '영지',
        'Title': '군단장 슬레이어',
        'GuildMemberGrade': '길드장',
        'GuildName': '테스트길드',
        'Stats': [{'Type': '치명', 'Value': '1500'}],
        'Tendencies': [{'Type': '지성', 'Point': 300}],
        'ServerName': '루페온',
        'CharacterName': '테스트캐릭',
        'CharacterLevel': 60,
        'CharacterClassName': '바드',
        'ItemAvgLevel': '1620.00',
        'ItemMaxLevel': '1620.00'
    }
    
    profile = ArmoryProfile.from_dict(data)
    
    assert profile.character_image == 'https://...'
    assert profile.expedition_level == 300
    assert profile.guild_name == '테스트길드'
    assert len(profile.stats) == 1
    assert profile.stats[0]['Type'] == '치명'


def test_armory_equipment_from_dict():
    """ArmoryEquipment should convert from API response."""
    data = {
        'Type': '무기',
        'Name': '고대 무기',
        'Icon': 'https://...',
        'Grade': '고대',
        'Tooltip': '{}'
    }
    
    eq = ArmoryEquipment.from_dict(data)
    
    assert eq.type == '무기'
    assert eq.name == '고대 무기'
    assert eq.grade == '고대'
    assert eq.tooltip == '{}'
