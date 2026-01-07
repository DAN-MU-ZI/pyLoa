"""Market-related models."""
from dataclasses import dataclass
from typing import Optional
from pyloa.models.base import BaseModel


@dataclass
class MarketItem(BaseModel):
    """거래소 아이템 정보 모델."""
    id: int
    name: str
    grade: str
    icon: str
    bundle_count: int
    trade_remain_count: int
    y_day_avg_price: Optional[float] = None
    recent_price: Optional[float] = None
    current_min_price: Optional[float] = None


@dataclass
class Trade(BaseModel):
    """거래 내역 모델."""
    date: str
    price: int
    quantity: int
