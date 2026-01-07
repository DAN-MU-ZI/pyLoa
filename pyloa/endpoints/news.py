"""뉴스/공지 관련 엔드포인트."""
from typing import List, Optional
from pyloa.endpoints.base import BaseEndpoint
from pyloa.models.news import Notice, Event


class NewsEndpoint(BaseEndpoint):
    """뉴스/공지 endpoint."""
    
    def __init__(self, client):
        """NewsEndpoint를 초기화합니다.
        
        Args:
            client: LostArkAPI 인스턴스
        """
        super().__init__(client)
        self.base_path = "/news"
    
    def get_notices(
        self,
        searchText: Optional[str] = None,
        type: Optional[str] = None
    ) -> List[Notice]:
        """공지사항 목록 조회.
        
        Args:
            searchText: 제목 검색 키워드 (optional)
            type: 공지 타입 - 공지/점검/상점/이벤트 (optional)
            
        Returns:
            List of Notice objects
        """
        params = {}
        if searchText is not None:
            params['searchText'] = searchText
        if type is not None:
            params['type'] = type
        
        data = self._request('GET', '/notices', params=params)
        return [Notice.from_dict(item) for item in data]
    
    def get_events(self) -> List[Event]:
        """진행 중인 이벤트 목록 조회.
        
        Returns:
            List of Event objects
        """
        data = self._request('GET', '/events')
        return [Event.from_dict(item) for item in data]
    
    def get_alarms(self) -> 'UserAlarm':
        """알람 목록 조회.
        
        Returns:
            UserAlarm object
        """
        from pyloa.models.news import UserAlarm
        data = self._request('GET', '/alarms')
        return UserAlarm.from_dict(data)
