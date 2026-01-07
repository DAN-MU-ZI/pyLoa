"""뉴스/공지 관련 모델."""
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


@dataclass
class UserAlarmContent(BaseModel):
    """유저 알람 내용 모델."""
    alarm_type: str
    contents: str
    start_date: str
    end_date: str

    @classmethod
    def from_dict(cls, data: dict) -> 'UserAlarmContent':
        return cls(
            alarm_type=data.get('AlarmType', ''),
            contents=data.get('Contents', ''),
            start_date=data.get('StartDate', ''),
            end_date=data.get('EndDate', '')
        )


@dataclass
class UserAlarm(BaseModel):
    """유저 알람 모델."""
    require_polling: bool
    alarms: list[UserAlarmContent]

    @classmethod
    def from_dict(cls, data: dict) -> 'UserAlarm':
        return cls(
            require_polling=data.get('RequirePolling', False),
            alarms=[UserAlarmContent.from_dict(item) for item in data.get('Alarms', [])]
        )
