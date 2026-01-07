"""Auctions endpoint."""
from typing import Dict, Any
from pyloa.endpoints.base import BaseEndpoint
from pyloa.models.auction import AuctionSearchResult


class AuctionsEndpoint(BaseEndpoint):
    """경매장 endpoint."""
    
    def __init__(self, client):
        """Initialize AuctionsEndpoint.
        
        Args:
            client: LostArkAPI instance
        """
        super().__init__(client)
        self.base_path = "/auctions"
    
    def get_options(self) -> Dict[str, Any]:
        """경매장 검색 옵션 조회.
        
        Returns:
            Dict with Categories, ItemGrades, etc.
        """
        return self._request('GET', '/options')
    
    def get_items(self, **kwargs) -> AuctionSearchResult:
        """경매장 아이템 검색.
        
        Args:
            **kwargs: 검색 파라미터
                ItemLevelMin, ItemLevelMax, ItemGradeQuality,
                SkillOptions, EtcOptions, Sort, CategoryCode,
                CharacterClass, ItemTier, ItemGrade, ItemName,
                PageNo, SortCondition
                
        Returns:
            AuctionSearchResult object
        """
        data = self._request('POST', '/items', json=kwargs)
        return AuctionSearchResult.from_dict(data)
