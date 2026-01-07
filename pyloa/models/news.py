"""News-related models."""
from dataclasses import dataclass
from typing import Optional
from pyloa.models.base import BaseModel


@dataclass
class Notice(BaseModel):
    """공지사항 모델."""
    title: str
    date: str
    link: str
    type: str


@dataclass
class Event(BaseModel):
    """이벤트 모델."""
    title: str
    thumbnail: str
    link: str
    start_date: str
    end_date: str
    reward_date: Optional[str] = None
