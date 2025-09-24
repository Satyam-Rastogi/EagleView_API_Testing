"""Client factory for EagleView API Client - Multi-Environment Support"""

from .base import EagleViewClient

def create_client(config):
    """Factory function to create an environment-appropriate client.
    
    Args:
        config: Configuration instance to use for the client
        
    Returns:
        An instance of the EagleViewClient configured for the specified environment
    """
    return EagleViewClient(config)


__all__ = ['EagleViewClient', 'create_client']