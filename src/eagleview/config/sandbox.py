"""
Sandbox-specific configuration for EagleView API client.
Contains sandbox-specific settings and constraints.
"""

from .base import EagleViewSettings
from typing import Optional

class SandboxConfig(EagleViewSettings):
    """Configuration settings for EagleView API sandbox environment.
    
    This class extends the base configuration with sandbox-specific
    settings and constraints.
    """
    
    def __init__(self, **kwargs):
        """Initialize sandbox configuration with default values.
        
        Args:
            **kwargs: Configuration values that override defaults
        """
        # Set default values for sandbox environment
        kwargs.setdefault('environment', 'sandbox')
        kwargs.setdefault('requests_per_second', 3.0)
        kwargs.setdefault('requests_per_minute', 50)
        kwargs.setdefault('validate_coordinates', True)
        
        # Initialize the base class
        super().__init__(**kwargs)
        
        # Additional sandbox-specific setup
        self._setup_sandbox_constraints()
    
    def _setup_sandbox_constraints(self):
        """Set up additional sandbox-specific constraints."""
        # Define sandbox bounding box coordinates
        self.sandbox_bounds = {
            'min_lat': 41.24140396772262,
            'max_lat': 41.25672882015283,
            'min_lon': -96.00532698173473,
            'max_lon': -95.97589954958912
        }
    
    def get_sandbox_bounds(self):
        """Get the sandbox coordinate bounds.
        
        Returns:
            Dictionary containing the bounding box for valid sandbox coordinates
        """
        return self.sandbox_bounds
    
    def validate_sandbox_coordinates(self, lat: float, lon: float) -> bool:
        """Validate that coordinates are within the sandbox area.
        
        Args:
            lat: Latitude to validate
            lon: Longitude to validate
            
        Returns:
            True if coordinates are valid for sandbox, False otherwise
        """
        bounds = self.sandbox_bounds
        return (
            bounds['min_lat'] <= lat <= bounds['max_lat'] and
            bounds['min_lon'] <= lon <= bounds['max_lon']
        )