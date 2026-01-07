"""게임 콘텐츠 관련 엔드포인트."""
from typing import List
from pyloa.endpoints.base import BaseEndpoint
from pyloa.models.game_content import GameContent


class GameContentsEndpoint(BaseEndpoint):
    """게임 컨텐츠 endpoint."""
    
    def __init__(self, client):
        """GameContentsEndpoint를 초기화합니다.
        
        Args:
            client: LostArkAPI 인스턴스
        """
        super().__init__(client)
        self.base_path = "/gamecontents"
    
    def get_calendar(self) -> List[GameContent]:
        """주간 캘린더 조회 (도전 가디언 등).
        
        Returns:
            List of GameContent objects
        """
        data = self._request('GET', '/calendar')
        return [GameContent.from_dict(item) for item in data]
