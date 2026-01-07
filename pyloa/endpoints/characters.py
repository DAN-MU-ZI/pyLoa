"""Characters endpoint."""
from typing import List
from pyloa.endpoints.base import BaseEndpoint
from pyloa.models.character import Character


class CharactersEndpoint(BaseEndpoint):
    """캐릭터 정보 endpoint."""
    
    def __init__(self, client):
        """Initialize CharactersEndpoint.
        
        Args:
            client: LostArkAPI instance
        """
        super().__init__(client)
        self.base_path = "/characters"
    
    def get_siblings(self, character_name: str) -> List[Character]:
        """계정의 모든 캐릭터 목록 조회.
        
        Args:
            character_name: 조회할 캐릭터 이름
            
        Returns:
            List of Character objects
        """
        data = self._request('GET', f'/{character_name}/siblings')
        return [Character.from_dict(item) for item in data]
