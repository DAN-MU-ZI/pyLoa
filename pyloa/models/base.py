"""Base model for API response objects."""
from dataclasses import asdict
from typing import Dict, TypeVar, Type
import re


T = TypeVar('T', bound='BaseModel')


class BaseModel:
    """Base class for all API response models."""
    
    @classmethod
    def _pascal_to_snake(cls, name: str) -> str:
        """Convert PascalCase to snake_case."""
        # Insert underscore before uppercase letters
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    
    @classmethod
    def _snake_to_pascal(cls, name: str) -> str:
        """Convert snake_case to PascalCase."""
        components = name.split('_')
        return ''.join(x.title() for x in components)
    
    @classmethod
    def from_dict(cls: Type[T], data: Dict) -> T:
        """Create model instance from dictionary.
        
        Supports both PascalCase (API format) and snake_case (Python format).
        """
        # Get field names from dataclass
        import dataclasses
        
        if not dataclasses.is_dataclass(cls):
            raise TypeError(f"{cls.__name__} must be a dataclass")
        
        fields = {f.name for f in dataclasses.fields(cls)}
        kwargs = {}
        
        for key, value in data.items():
            # Try snake_case first (direct match)
            snake_key = key if '_' in key else cls._pascal_to_snake(key)
            
            if snake_key in fields:
                kwargs[snake_key] = value
        
        return cls(**kwargs)
    
    def to_dict(self) -> Dict:
        """Convert model instance to dictionary."""
        return asdict(self)
