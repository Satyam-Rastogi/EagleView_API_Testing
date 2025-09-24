"""
Production-specific configuration for EagleView API client.
Contains production-specific settings and optimizations.
"""

from .base import EagleViewSettings
from typing import Optional

class ProductionConfig(EagleViewSettings):
    """Configuration settings for EagleView API production environment.
    
    This class extends the base configuration with production-specific
    settings and optimizations.
    """
    
    def __init__(self, **kwargs):
        """Initialize production configuration with default values.
        
        Args:
            **kwargs: Configuration values that override defaults
        """
        # Set default values for production environment
        kwargs.setdefault('environment', 'production')
        kwargs.setdefault('requests_per_second', 10.0)
        kwargs.setdefault('requests_per_minute', 200)
        kwargs.setdefault('validate_coordinates', False)
        
        # Initialize the base class
        super().__init__(**kwargs)
        
        # Additional production-specific setup
        self._setup_production_optimizations()
    
    def _setup_production_optimizations(self):
        """Set up additional production-specific optimizations."""
        # Production-specific settings
        self.timeout = 10  # Shorter timeout for production
        self.retry_attempts = 3  # Default retry attempts
        
    def get_production_settings(self) -> dict:
        """Get production-specific settings.
        
        Returns:
            Dictionary containing production-specific configuration
        """
        return {
            'timeout': self.timeout,
            'retry_attempts': self.retry_attempts,
            'validate_coordinates': self.validate_coordinates
        }