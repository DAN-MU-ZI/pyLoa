"""Rate limiter for API requests."""
from datetime import datetime
from typing import Dict, Optional


class RateLimiter:
    """Manages API rate limiting based on response headers."""
    
    def __init__(self):
        """Initialize rate limiter with default values."""
        self.limit: int = 100  # Default: 100 requests per minute
        self.remaining: int = 100
        self.reset_time: Optional[datetime] = None
    
    def get_wait_duration(self) -> float:
        """Return the number of seconds to wait before the next request.
        
        Returns:
            float: Seconds to wait. 0.0 if no wait is needed.
        """
        if self.remaining <= 0 and self.reset_time:
            now = datetime.now()
            if now < self.reset_time:
                return (self.reset_time - now).total_seconds()
        return 0.0
    
    def update(self, headers: Dict[str, str]) -> None:
        """Update rate limit info from response headers."""
        if 'X-RateLimit-Limit' in headers:
            self.limit = int(headers['X-RateLimit-Limit'])
        if 'X-RateLimit-Remaining' in headers:
            self.remaining = int(headers['X-RateLimit-Remaining'])
        if 'X-RateLimit-Reset' in headers:
            reset_epoch = int(headers['X-RateLimit-Reset'])
            self.reset_time = datetime.fromtimestamp(reset_epoch)
