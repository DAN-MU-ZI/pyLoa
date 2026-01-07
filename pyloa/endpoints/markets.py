"""Markets endpoint."""
from typing import List, Dict, Any
from pyloa.endpoints.base import BaseEndpoint
from pyloa.models.market import MarketItem, Trade


class MarketsEndpoint(BaseEndpoint):
    """거래소 endpoint."""
    
    def __init__(self, client):
        """Initialize MarketsEndpoint.
        
        Args:
            client: LostArkAPI instance
        """
        super().__init__(client)
        self.base_path = "/markets"
    
    def get_options(self) -> Dict[str, Any]:
        """거래소 검색 옵션 조회.
        
        Returns:
            Dict with Categories and ItemGrades
        """
        return self._request('GET', '/options')
    
    def get_item(self, item_id: int) -> MarketItem:
        """특정 아이템의 거래소 정보 조회.
        
        Args:
            item_id: 아이템 ID
            
        Returns:
            MarketItem object
        """
        data = self._request('GET', f'/items/{item_id}')
        return MarketItem.from_dict(data)
    
    def search_items(self, **kwargs) -> Dict[str, Any]:
        """거래소 아이템 검색.
        
        Args:
            **kwargs: 검색 파라미터
                CategoryCode, CharacterClass, ItemTier,
                ItemGrade, ItemName, PageNo, SortCondition
                
        Returns:
            Dict with PageNo, PageSize, TotalCount, Items
        """
        return self._request('POST', '/items', json=kwargs)
    
    def get_trades(self, **kwargs) -> List[Trade]:
        """최근 거래 내역 조회.
        
        Args:
            **kwargs: 검색 파라미터
                CategoryCode, CharacterClass, ItemTier,
                ItemGrade, ItemName, PageNo
                
        Returns:
            List of Trade objects
        """
        data = self._request('POST', '/trades', json=kwargs)
        return [Trade.from_dict(item) for item in data]
