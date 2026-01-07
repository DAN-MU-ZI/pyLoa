"""Auction-related models."""
from dataclasses import dataclass
from typing import List, Optional, Any, Dict
from pyloa.models.base import BaseModel


@dataclass
class AuctionOption(BaseModel):
    """경매장 아이템 옵션 모델."""
    type: str
    option_name: str
    value: Optional[int] = None
    first_option: Optional[int] = None
    second_option: Optional[int] = None
    min_value: Optional[int] = None
    max_value: Optional[int] = None
    class_name: Optional[str] = None


@dataclass
class AuctionInfo(BaseModel):
    """경매 정보 모델."""
    start_price: int
    end_date: str
    bid_count: int
    bid_start_price: int
    is_competitive: bool
    trade_allow_count: int
    buy_price: Optional[int] = None
    bid_price: Optional[int] = None


@dataclass
class AuctionItem(BaseModel):
    """경매장 아이템 모델."""
    name: str
    grade: str
    tier: int
    level: int
    icon: str
    grade_quality: int
    auction_info: AuctionInfo
    options: List[AuctionOption]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AuctionItem':
        """딕셔너리에서 객체 생성 (중첩 객체 처리)."""
        # 기본 변환
        instance = super().from_dict(data)
        
        # 중첩 객체 수동 변환
        if 'AuctionInfo' in data:
            instance.auction_info = AuctionInfo.from_dict(data['AuctionInfo'])
            
        if 'Options' in data and data['Options']:
            instance.options = [
                AuctionOption.from_dict(opt) for opt in data['Options']
            ]
        elif not hasattr(instance, 'options'):
             instance.options = []
             
        return instance

    def to_dict(self) -> Dict[str, Any]:
        """객체를 딕셔너리로 변환 (중첩 객체 처리)."""
        data = super().to_dict()
        
        # 중첩 객체 변환
        if self.auction_info:
            data['auction_info'] = self.auction_info.to_dict()
            
        if self.options:
            data['options'] = [opt.to_dict() for opt in self.options]
            
        return data


@dataclass
class AuctionSearchResult(BaseModel):
    """경매장 검색 결과 모델."""
    page_no: int
    page_size: int
    total_count: int
    items: List[AuctionItem]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AuctionSearchResult':
        """딕셔너리에서 객체 생성."""
        instance = super().from_dict(data)
        
        if 'Items' in data and data['Items']:
            instance.items = [
                AuctionItem.from_dict(item) for item in data['Items']
            ]
        elif not hasattr(instance, 'items'):
            instance.items = []
            
        return instance
