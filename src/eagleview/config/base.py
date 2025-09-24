"""
Enhanced configuration management for EagleView API client.
Handles credentials, settings, environment configuration, and validation.

This module provides a dataclass-based configuration system that supports
loading settings from environment variables or YAML configuration files.
"""

from dataclasses import dataclass
from typing import Optional
import os

@dataclass
class EagleViewSettings:
    """Configuration settings for EagleView API client.
    
    This dataclass encapsulates all configuration settings for the EagleView
    API client, including authentication credentials, rate limiting settings,
    and output options.
    """
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    requests_per_second: float = 3.0
    requests_per_minute: int = 50
    environment: str = 'sandbox'
    output_directory: str = "data"
    log_level: str = "INFO"
    validate_coordinates: bool = True
    
    def __post_init__(self):
        """Set environment-specific defaults after initialization."""
        self.is_sandbox = (self.environment == 'sandbox')
        self._set_environment_defaults()
    
    def _set_environment_defaults(self):
        """Set defaults based on environment."""
        if self.is_sandbox:
            self.base_url = 'https://sandbox.apicenter.eagleview.com'
            self.imagery_base_url = 'https://sandbox.apis.eagleview.com'
            self.validate_coordinates = getattr(self, 'validate_coordinates', True)
        else:
            self.base_url = 'https://apicenter.eagleview.com'
            self.imagery_base_url = 'https://apis.eagleview.com'
            self.validate_coordinates = getattr(self, 'validate_coordinates', False)
    
    @classmethod
    def from_environment(cls) -> 'EagleViewSettings':
        """Create settings from environment variables.
        
        This method reads configuration from environment variables, providing
        a fallback mechanism when configuration files are not available.
        
        Environment variables:
            EAGLEVIEW_CLIENT_ID: API client ID
            EAGLEVIEW_CLIENT_SECRET: API client secret
            EAGLEVIEW_REQUESTS_PER_SECOND: Requests per second limit (default: 3.0)
            EAGLEVIEW_REQUESTS_PER_MINUTE: Requests per minute limit (default: 50)
            EAGLEVIEW_ENVIRONMENT: Environment to use (sandbox or production, default: sandbox)
            EAGLEVIEW_OUTPUT_DIR: Output directory for files (default: data)
            EAGLEVIEW_LOG_LEVEL: Logging level (default: INFO)
            EAGLEVIEW_VALIDATE_COORDS: Whether to validate coordinates (default: true for sandbox, false for production)
            
        Returns:
            EagleViewSettings instance with values from environment variables
        """
        environment = os.getenv('EAGLEVIEW_ENVIRONMENT', 'sandbox')
        is_sandbox = environment == 'sandbox'
        validate_coords = os.getenv('EAGLEVIEW_VALIDATE_COORDS', str(is_sandbox).lower()) == 'true'
        
        return cls(
            client_id=os.getenv('EAGLEVIEW_CLIENT_ID'),
            client_secret=os.getenv('EAGLEVIEW_CLIENT_SECRET'),
            requests_per_second=float(os.getenv('EAGLEVIEW_REQUESTS_PER_SECOND', '3' if is_sandbox else '10')),
            requests_per_minute=int(os.getenv('EAGLEVIEW_REQUESTS_PER_MINUTE', '50' if is_sandbox else '200')),
            environment=environment,
            output_directory=os.getenv('EAGLEVIEW_OUTPUT_DIR', 'data'),
            log_level=os.getenv('EAGLEVIEW_LOG_LEVEL', 'INFO'),
            validate_coordinates=validate_coords
        )
    
    @classmethod
    def from_yaml(cls, filepath: str) -> 'EagleViewSettings':
        """Create settings from a YAML configuration file.
        
        This method reads configuration from a YAML file, allowing for more
        complex configuration scenarios than environment variables.
        
        YAML structure:
            eagleview:
              client_id: "your_client_id"
              client_secret: "your_client_secret"
              requests_per_second: 3.0
              requests_per_minute: 50
              environment: "sandbox"  # or "production"
              output_directory: "data"
              log_level: "INFO"
              validate_coordinates: true  # or false
              
        Args:
            filepath: Path to the YAML configuration file
            
        Returns:
            EagleViewSettings instance with values from the YAML file
            
        Raises:
            ValueError: If there's an error loading or parsing the YAML file
        """
        try:
            import yaml
            with open(filepath, 'r') as f:
                config_data = yaml.safe_load(f)
            
            # Extract eagleview settings
            eagleview_config = config_data.get('eagleview', {})
            
            return cls(
                client_id=eagleview_config.get('client_id'),
                client_secret=eagleview_config.get('client_secret'),
                requests_per_second=eagleview_config.get('requests_per_second', 3.0),
                requests_per_minute=eagleview_config.get('requests_per_minute', 50),
                environment=eagleview_config.get('environment', 'sandbox'),
                output_directory=eagleview_config.get('output_directory', 'data'),
                log_level=eagleview_config.get('log_level', 'INFO'),
                validate_coordinates=eagleview_config.get('validate_coordinates', None)
            )
        except Exception as e:
            raise ValueError(f"Error loading YAML configuration: {e}")
    
    @classmethod
    def from_config(cls, config_source: Optional[str] = None) -> 'EagleViewSettings':
        """Create settings from a configuration source (YAML file or environment).
        
        This method provides a unified interface for loading configuration from
        either a YAML file or environment variables, with YAML taking precedence
        when a valid file is provided.
        
        Args:
            config_source: Path to YAML configuration file (optional)
            
        Returns:
            EagleViewSettings instance with configuration values
        """
        if config_source and os.path.exists(config_source):
            if config_source.endswith(('.yaml', '.yml')):
                return cls.from_yaml(config_source)
        
        # Fallback to environment variables
        return cls.from_environment()
    
    def validate(self) -> bool:
        """Validate that required configuration is present.
        
        This method checks that the minimum required configuration values
        (client_id and client_secret) are present.
        
        Returns:
            True if validation passes, False otherwise
        """
        return bool(self.client_id and self.client_secret)
    
    def get_api_urls(self) -> dict:
        """Get API URLs based on environment setting.
        
        Returns:
            Dictionary containing base_url and imagery_base_url
        """
        return {
            'base_url': self.base_url,
            'imagery_base_url': self.imagery_base_url
        }
    
    def get_environment_info(self) -> dict:
        """Get information about the current environment.
        
        Returns:
            Dictionary with environment-specific information
        """
        return {
            'environment': self.environment,
            'is_sandbox': self.is_sandbox,
            'base_url': self.base_url,
            'imagery_base_url': self.imagery_base_url,
            'requests_per_second': self.requests_per_second,
            'requests_per_minute': self.requests_per_minute,
            'validate_coordinates': self.validate_coordinates
        }