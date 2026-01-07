"""Armories endpoint."""
from typing import List, Optional, Dict, Any
from pyloa.endpoints.base import BaseEndpoint
from pyloa.models.armory import (
    ArmoryProfile, ArmoryEquipment, ArmoryAvatar, ArmorySkill,
    ArmoryEngraving, ArmoryCard, ArmoryGem, ColosseumInfo,
    Collectible, ArkPassive
)


class ArmoriesEndpoint(BaseEndpoint):
    """캐릭터 정보(Armories) endpoint."""
    
    def __init__(self, client):
        """Initialize ArmoriesEndpoint.
        
        Args:
            client: LostArkAPI instance
        """
        super().__init__(client)
        self.base_path = "/armories/characters"
    
    def get_profile(self, character_name: str) -> ArmoryProfile:
        """캐릭터 프로필 조회."""
        data = self._request('GET', f'/{character_name}/profiles')
        return ArmoryProfile.from_dict(data)
    
    def get_equipment(self, character_name: str) -> List[ArmoryEquipment]:
        """장비 정보 조회."""
        data = self._request('GET', f'/{character_name}/equipment')
        return [ArmoryEquipment.from_dict(item) for item in data]
    
    def get_avatars(self, character_name: str) -> List[ArmoryAvatar]:
        """아바타 정보 조회."""
        data = self._request('GET', f'/{character_name}/avatars')
        if not data:
            return []
        return [ArmoryAvatar.from_dict(item) for item in data]
    
    def get_combat_skills(self, character_name: str) -> List[ArmorySkill]:
        """전투 스킬 정보 조회."""
        data = self._request('GET', f'/{character_name}/combat-skills')
        if not data:
            return []
        return [ArmorySkill.from_dict(item) for item in data]
    
    def get_engravings(self, character_name: str) -> Optional[ArmoryEngraving]:
        """각인 정보 조회."""
        data = self._request('GET', f'/{character_name}/engravings')
        if not data:
             return None
        return ArmoryEngraving.from_dict(data)
    
    def get_cards(self, character_name: str) -> Optional[ArmoryCard]:
        """카드 정보 조회."""
        data = self._request('GET', f'/{character_name}/cards')
        if not data:
            return None
        return ArmoryCard.from_dict(data)
    
    def get_gems(self, character_name: str) -> Optional[ArmoryGem]:
        """보석 정보 조회."""
        data = self._request('GET', f'/{character_name}/gems')
        if not data:
            return None
        return ArmoryGem.from_dict(data)
    
    def get_colosseums(self, character_name: str) -> Optional[ColosseumInfo]:
        """투기장 정보 조회."""
        data = self._request('GET', f'/{character_name}/colosseums')
        if not data:
            return None
        return ColosseumInfo.from_dict(data)
    
    def get_collectibles(self, character_name: str) -> List[Collectible]:
        """수집품 정보 조회."""
        data = self._request('GET', f'/{character_name}/collectibles')
        if not data:
            return []
        return [Collectible.from_dict(item) for item in data]

    def get_ark_passive(self, character_name: str) -> Optional[ArkPassive]:
        """아크 패시브 정보 조회."""
        data = self._request('GET', f'/{character_name}/arkpassive')
        if not data:
            return None
        return ArkPassive.from_dict(data)
