"""Armory 관련 모델."""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from pyloa.models.base import BaseModel


@dataclass
class ArmoryEquipment(BaseModel):
    """장비 정보 모델."""
    type: str
    name: str
    icon: str
    grade: str
    tooltip: str


@dataclass
class ArmoryProfile(BaseModel):
    """캐릭터 프로필 모델."""
    character_image: str
    expedition_level: int
    pvp_grade_name: str
    town_level: int
    town_name: str
    title: str
    guild_member_grade: str
    guild_name: str
    stats: List[Dict[str, Any]]
    tendencies: List[Dict[str, Any]]
    server_name: str
    character_name: str
    character_level: int
    character_class_name: str
    item_avg_level: str
    item_max_level: str


# Placeholders/Simple models for other endpoints
@dataclass
class ArmoryAvatar(BaseModel):
    """아바타 모델."""
    type: str
    name: str
    icon: str
    grade: str
    is_set: bool
    is_inner: bool
    tooltip: str

@dataclass
class ArmorySkill(BaseModel):
    """스킬 모델."""
    name: str
    icon: str
    level: int
    type: str
    is_awake: bool
    tooltip: str

@dataclass
class ArmoryEngraving(BaseModel):
    """각인 모델."""
    engravings: List[Dict[str, Any]]
    effects: List[Dict[str, Any]]

@dataclass
class ArmoryCard(BaseModel):
    """카드 모델."""
    cards: List[Dict[str, Any]]
    effects: List[Dict[str, Any]]

@dataclass
class ArmoryGem(BaseModel):
    """보석 모델."""
    gems: List[Dict[str, Any]]
    effects: List[Dict[str, Any]]

@dataclass
class ColosseumInfo(BaseModel):
    """투기장 모델."""
    rank: int
    pre_rank: int
    exp: int
    colosseums: List[Dict[str, Any]]

@dataclass
class Collectible(BaseModel):
    """수집품 모델."""
    type: str
    icon: str
    point: int
    max_point: int
    collectible_points: List[Dict[str, Any]]

@dataclass
class ArkPassive(BaseModel):
    """아크 패시브 모델."""
    is_open: bool
    points: List[Dict[str, Any]]
    effects: List[Dict[str, Any]]


@dataclass
class ArkGridGem(BaseModel):
    """아크 그리드 보석 모델."""
    index: int
    icon: str
    is_active: bool
    grade: str
    tooltip: str


@dataclass
class ArkGridEffect(BaseModel):
    """아크 그리드 효과 모델."""
    name: str
    level: int
    tooltip: str


@dataclass
class ArkGridSlot(BaseModel):
    """아크 그리드 슬롯 모델."""
    index: int
    icon: str
    name: str
    point: int
    grade: str
    tooltip: str
    gems: List[ArkGridGem]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ArkGridSlot':
        """딕셔너리에서 인스턴스를 생성합니다."""
        instance = super().from_dict(data)
        if 'Gems' in data:
            instance.gems = [ArkGridGem.from_dict(item) for item in data['Gems']]
        return instance


@dataclass
class ArkGrid(BaseModel):
    """아크 그리드 모델."""
    slots: List[ArkGridSlot]
    effects: List[ArkGridEffect]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ArkGrid':
        """딕셔너리에서 인스턴스를 생성합니다."""
        return cls(
            slots=[ArkGridSlot.from_dict(item) for item in data.get('Slots', [])],
            effects=[ArkGridEffect.from_dict(item) for item in data.get('Effects', [])]
        )


@dataclass
class ArmoryTotal(BaseModel):
    """Armory 종합 정보 모델."""
    armory_profile: Optional[ArmoryProfile] = None
    armory_equipment: Optional[List[ArmoryEquipment]] = None
    armory_avatars: Optional[List[ArmoryAvatar]] = None
    armory_skills: Optional[List[ArmorySkill]] = None
    armory_engraving: Optional[ArmoryEngraving] = None
    armory_card: Optional[ArmoryCard] = None
    armory_gem: Optional[ArmoryGem] = None
    colosseum_info: Optional[ColosseumInfo] = None
    collectibles: Optional[List[Collectible]] = None
    ark_passive: Optional[ArkPassive] = None
    ark_grid: Optional[ArkGrid] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ArmoryTotal':
        """딕셔너리에서 인스턴스를 생성합니다."""
        return cls(
            armory_profile=ArmoryProfile.from_dict(data['ArmoryProfile']) if data.get('ArmoryProfile') else None,
            armory_equipment=[ArmoryEquipment.from_dict(item) for item in data.get('ArmoryEquipment', [])] if data.get('ArmoryEquipment') else None,
            armory_avatars=[ArmoryAvatar.from_dict(item) for item in data.get('ArmoryAvatars', [])] if data.get('ArmoryAvatars') else None,
            armory_skills=[ArmorySkill.from_dict(item) for item in data.get('ArmorySkills', [])] if data.get('ArmorySkills') else None,
            armory_engraving=ArmoryEngraving.from_dict(data['ArmoryEngraving']) if data.get('ArmoryEngraving') else None,
            armory_card=ArmoryCard.from_dict(data['ArmoryCard']) if data.get('ArmoryCard') else None,
            armory_gem=ArmoryGem.from_dict(data['ArmoryGem']) if data.get('ArmoryGem') else None,
            colosseum_info=ColosseumInfo.from_dict(data['ColosseumInfo']) if data.get('ColosseumInfo') else None,
            collectibles=[Collectible.from_dict(item) for item in data.get('Collectibles', [])] if data.get('Collectibles') else None,
            ark_passive=ArkPassive.from_dict(data['ArkPassive']) if data.get('ArkPassive') else None,
            ark_grid=ArkGrid.from_dict(data['ArkGrid']) if data.get('ArkGrid') else None
        )
