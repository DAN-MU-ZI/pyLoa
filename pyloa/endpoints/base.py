"""Base endpoint for all API endpoints."""
from typing import Dict, TYPE_CHECKING
from requests import HTTPError
from pyloa.exceptions import APIError, RateLimitError, AuthenticationError

if TYPE_CHECKING:
    from pyloa.client import LostArkAPI


class BaseEndpoint:
    """Base class for all API endpoints."""
    
    def __init__(self, client: 'LostArkAPI'):
        """Initialize endpoint with client.
        
        Args:
            client: LostArkAPI instance
        """
        self.client = client
        self.base_path = ""  # Subclasses should override
    
    def _request(self, method: str, path: str, **kwargs) -> Dict:
        """Make HTTP request with rate limiting and error handling.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            path: Endpoint path
            **kwargs: Additional arguments for requests
            
        Returns:
            JSON response as dictionary
            
        Raises:
            AuthenticationError: On 401 Unauthorized
            RateLimitError: On 429 Too Many Requests
            APIError: On other HTTP errors
        """
        # Wait if rate limit exceeded
        self.client.rate_limiter.wait_if_needed()
        
        # Build full URL
        url = f"{self.client.base_url}{self.base_path}{path}"
        
        # Make request
        response = self.client.session.request(method, url, **kwargs)
        
        # Update rate limiter from headers
        self.client.rate_limiter.update(response.headers)
        
        # Handle errors
        try:
            response.raise_for_status()
        except HTTPError:
            if response.status_code == 401:
                raise AuthenticationError(f"Unauthorized: {response.text}")
            elif response.status_code == 429:
                raise RateLimitError(f"Rate limit exceeded: {response.text}")
            else:
                raise APIError(f"API error ({response.status_code}): {response.text}")
        
        return response.json()
