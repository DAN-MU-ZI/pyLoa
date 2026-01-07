"""게임 콘텐츠 모델 (캘린더 등)."""
from dataclasses import dataclass
from typing import List, Dict, Any
from pyloa.models.base import BaseModel


@dataclass
class GameContentRewardItem(BaseModel):
    """컨텐츠 보상 아이템 모델."""
    name: str
    icon: str
    grade: str


@dataclass
class GameContent(BaseModel):
    """게임 컨텐츠 (캘린더) 모델."""
    category_name: str
    contents_name: str
    contents_icon: str
    min_item_level: int
    start_times: List[str]
    location: str
    reward_items: List[GameContentRewardItem]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GameContent':
        """딕셔너리에서 객체 생성 (중첩 객체 처리)."""
        instance = super().from_dict(data)
        
        if 'RewardItems' in data and data['RewardItems']:
            instance.reward_items = [
                GameContentRewardItem.from_dict(item) 
                for item in data['RewardItems']
            ]
        elif not hasattr(instance, 'reward_items'):
             instance.reward_items = []
             
        return instance

    def to_dict(self) -> Dict[str, Any]:
        """객체를 딕셔너리로 변환 (중첩 객체 처리)."""
        data = super().to_dict()
        
        if self.reward_items:
            data['reward_items'] = [
                item.to_dict() for item in self.reward_items
            ]
            
        return data
