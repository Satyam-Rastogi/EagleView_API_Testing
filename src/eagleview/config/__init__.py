"""Configuration factory for EagleView API Client - Multi-Environment Support"""

from .base import EagleViewSettings
from .sandbox import SandboxConfig
from .production import ProductionConfig

def create_config(environment='sandbox', **kwargs):
    """Factory function to create environment-appropriate configuration.
    
    Args:
        environment: The environment to create configuration for ('sandbox' or 'production')
        **kwargs: Additional configuration options that override defaults
        
    Returns:
        An instance of the appropriate configuration class
    """
    if environment == 'sandbox':
        return SandboxConfig(**kwargs)
    elif environment == 'production':
        return ProductionConfig(**kwargs)
    else:
        return EagleViewSettings(environment=environment, **kwargs)


__all__ = ['EagleViewSettings', 'SandboxConfig', 'ProductionConfig', 'create_config']