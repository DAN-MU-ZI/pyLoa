"""거래소 관련 엔드포인트."""
from typing import List, Dict, Any
from pyloa.endpoints.base import BaseEndpoint
from pyloa.models.market import MarketItem, Market, TradeMarket, MarketItemStats


class MarketsEndpoint(BaseEndpoint):
    """거래소 endpoint."""
    
    def __init__(self, client):
        """MarketsEndpoint를 초기화합니다.
        
        Args:
            client: LostArkAPI 인스턴스
        """
        super().__init__(client)
        self.base_path = "/markets"
    
    def get_options(self) -> Dict[str, Any]:
        """거래소 검색 옵션 조회.
        
        Returns:
            Dict with Categories and ItemGrades
        """
        return self._request('GET', '/options')
    
    def get_item(self, item_id: int) -> List[MarketItemStats]:
        """특정 아이템의 거래소 정보 조회.
        
        Args:
            item_id: 아이템 ID
            
        Returns:
            List of MarketItemStats objects
        """
        data = self._request('GET', f'/items/{item_id}')
        if not isinstance(data, list):
            return []
        return [MarketItemStats.from_dict(item) for item in data]

    
    def search_items(self, **kwargs) -> Market:
        """거래소 아이템 검색.
        
        Args:
            **kwargs: 검색 파라미터
                CategoryCode, CharacterClass, ItemTier,
                ItemGrade, ItemName, PageNo, SortCondition
                
        Returns:
            Market object
        """
        data = self._request('POST', '/items', json=kwargs)
        return Market.from_dict(data)
    
    def get_trades(self, **kwargs) -> TradeMarket:
        """최근 거래 내역 조회.
        
        Args:
            **kwargs: 검색 파라미터
                CategoryCode, CharacterClass, ItemTier,
                ItemGrade, ItemName, PageNo
                
        Returns:
            TradeMarket object
        """
        data = self._request('POST', '/trades', json=kwargs)
        return TradeMarket.from_dict(data)
