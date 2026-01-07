"""LostArkAPI client."""
import requests
from pyloa.rate_limiter import RateLimiter


class LostArkAPI:
    """Main client for Lost Ark API."""
    
    def __init__(self, api_key: str):
        """Initialize API client.
        
        Args:
            api_key: JWT token for authorization
        """
        self._api_key = api_key
        self.base_url = "https://developer-lostark.game.onstove.com"
        
        # Create session with headers
        self.session = requests.Session()
        self.session.headers.update({
            "authorization": f"bearer {api_key}",
            "accept": "application/json"
        })
        
        # Initialize rate limiter
        self.rate_limiter = RateLimiter()
    
    @property
    def api_key(self) -> str:
        """Get API key (read-only)."""
        return self._api_key
    
    @property
    def news(self):
        """Access News endpoint."""
        if not hasattr(self, '_news'):
            from pyloa.endpoints.news import NewsEndpoint
            self._news = NewsEndpoint(self)
        return self._news
    
    @property
    def characters(self):
        """Access Characters endpoint."""
        if not hasattr(self, '_characters'):
            from pyloa.endpoints.characters import CharactersEndpoint
            self._characters = CharactersEndpoint(self)
        return self._characters
    
    @property
    def markets(self):
        """Access Markets endpoint."""
        if not hasattr(self, '_markets'):
            from pyloa.endpoints.markets import MarketsEndpoint
            self._markets = MarketsEndpoint(self)
        return self._markets
    
    @property
    def auctions(self):
        """Access Auctions endpoint."""
        if not hasattr(self, '_auctions'):
            from pyloa.endpoints.auctions import AuctionsEndpoint
            self._auctions = AuctionsEndpoint(self)
        return self._auctions
    
    @property
    def game_contents(self):
        """Access Game Contents endpoint."""
        if not hasattr(self, '_game_contents'):
            from pyloa.endpoints.game_contents import GameContentsEndpoint
            self._game_contents = GameContentsEndpoint(self)
        return self._game_contents
