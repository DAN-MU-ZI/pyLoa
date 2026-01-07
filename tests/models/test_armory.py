"""Armory 모델 테스트."""
import pytest
from pyloa.models.armory import (
    ArmoryProfile, ArmoryEquipment, ArmoryAvatar, ArmorySkill,
    ArmoryEngraving, ArmoryCard, ArmoryGem, ColosseumInfo,
    Collectible, ArkPassive
)


def test_armory_profile_from_dict():
    """ArmoryProfile은 API 응답에서 변환되어야 합니다."""
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
    """ArmoryEquipment는 API 응답에서 변환되어야 합니다."""
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


def test_armory_avatar_from_dict():
    """ArmoryAvatar는 API 응답에서 변환되어야 합니다."""
    data = {
        'Type': '무기 아바타',
        'Name': '아바타',
        'Icon': 'icon',
        'Grade': '전설',
        'IsSet': False,
        'IsInner': False,
        'Tooltip': '{}'
    }
    
    avatar = ArmoryAvatar.from_dict(data)
    assert avatar.type == '무기 아바타'
    assert avatar.is_set is False


def test_armory_skill_from_dict():
    """ArmorySkill은 API 응답에서 변환되어야 합니다."""
    data = {
        'Name': '스킬',
        'Icon': 'icon',
        'Level': 12,
        'Type': '지점',
        'IsAwake': False,
        'Tooltip': '{}'
    }
    
    skill = ArmorySkill.from_dict(data)
    assert skill.level == 12
    assert skill.is_awake is False


def test_armory_engraving_from_dict():
    """ArmoryEngraving은 API 응답에서 변환되어야 합니다."""
    data = {
        'Engravings': [{'Name': '원한'}],
        'Effects': [{'Name': '원한 3'}]
    }
    
    engraving = ArmoryEngraving.from_dict(data)
    assert len(engraving.engravings) == 1
    assert engraving.engravings[0]['Name'] == '원한'


def test_armory_card_from_dict():
    """ArmoryCard는 API 응답에서 변환되어야 합니다."""
    data = {'Cards': [], 'Effects': []}
    card = ArmoryCard.from_dict(data)
    assert isinstance(card.cards, list)


def test_armory_gem_from_dict():
    """ArmoryGem은 API 응답에서 변환되어야 합니다."""
    data = {'Gems': [], 'Effects': []}
    gem = ArmoryGem.from_dict(data)
    assert isinstance(gem.gems, list)


def test_colosseum_info_from_dict():
    """ColosseumInfo는 API 응답에서 변환되어야 합니다."""
    data = {'Rank': 1, 'PreRank': 1, 'Exp': 100, 'Colosseums': []}
    info = ColosseumInfo.from_dict(data)
    assert info.rank == 1


def test_collectible_from_dict():
    """Collectible은 API 응답에서 변환되어야 합니다."""
    data = {
        'Type': '모코코',
        'Icon': 'icon',
        'Point': 10,
        'MaxPoint': 100,
        'CollectiblePoints': []
    }
    col = Collectible.from_dict(data)
    assert col.type == '모코코'


def test_ark_passive_from_dict():
    """ArkPassive는 API 응답에서 변환되어야 합니다."""
    data = {
        'IsOpen': True,
        'Points': [],
        'Effects': []
    }
    passive = ArkPassive.from_dict(data)
    assert passive.is_open is True
