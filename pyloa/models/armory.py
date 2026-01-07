"""Armory models."""
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
