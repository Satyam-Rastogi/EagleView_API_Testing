# Code Refactoring Plan

## Overview
This document outlines a comprehensive refactoring plan to improve the code quality, reduce redundancies, and enhance maintainability of the EagleView API client.

## Current Issues Identified

### 1. Hardcoded Credentials
Credentials are hardcoded in multiple files, creating security risks and maintenance challenges.

### 2. Code Duplication
Repeated configuration code, client initialization, and similar structures across multiple scripts.

### 3. Inconsistent Error Handling
Variable error handling approaches and logging practices across the codebase.

### 4. Hardcoded File Dependencies
Scripts depend on specific output files from previous runs with no fallback mechanisms.

## Refactoring Goals

1. **Eliminate Redundancy**: Centralize configuration and common functionality
2. **Improve Security**: Remove hardcoded credentials
3. **Enhance Maintainability**: Create modular, reusable components
4. **Standardize Error Handling**: Implement consistent error handling and logging
5. **Add Graceful Fallbacks**: Handle missing files and dependencies gracefully
6. **Improve Type Safety**: Add comprehensive type hints
7. **Enhance Documentation**: Add clear docstrings and usage examples

## Proposed Refactoring Steps

### 1. Configuration Management

#### Create `config.py`
```python
"""
Configuration module for EagleView API client.
Handles credentials, settings, and environment configuration.
"""

import os
from typing import Optional

# API Credentials (from environment variables)
CLIENT_ID: Optional[str] = os.getenv('EAGLEVIEW_CLIENT_ID')
CLIENT_SECRET: Optional[str] = os.getenv('EAGLEVIEW_CLIENT_SECRET')

# API Settings
REQUESTS_PER_SECOND: float = float(os.getenv('EAGLEVIEW_REQUESTS_PER_SECOND', '3'))
REQUESTS_PER_MINUTE: int = int(os.getenv('EAGLEVIEW_REQUESTS_PER_MINUTE', '50'))
IS_SANDBOX: bool = os.getenv('EAGLEVIEW_IS_SANDBOX', 'true').lower() == 'true'

# File Settings
DEFAULT_OUTPUT_DIR: str = os.getenv('EAGLEVIEW_OUTPUT_DIR', 'output')
DEFAULT_LOG_LEVEL: str = os.getenv('EAGLEVIEW_LOG_LEVEL', 'INFO')

def validate_config() -> bool:
    """Validate that required configuration is present."""
    return bool(CLIENT_ID and CLIENT_SECRET)

def get_sandbox_bounds() -> dict:
    """Return sandbox bounding box coordinates."""
    return {
        'min_lat': 41.24140396772262,
        'max_lat': 41.25672882015283,
        'min_lon': -96.00532698173473,
        'max_lon': -95.97589954958912
    }
```

### 2. Utility Functions

#### Create `utils.py`
```python
"""
Utility functions for EagleView API client.
Contains common operations and helper functions.
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
from glob import glob
from datetime import datetime

from client_credentials_eagleview import ClientCredentialsEagleViewClient, EagleViewConfig
import config

def setup_logging(name: str, level: str = config.DEFAULT_LOG_LEVEL) -> logging.Logger:
    """Set up standardized logging for a module."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Prevent adding multiple handlers
    if not logger.handlers:
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File handler
        log_file = f"{name.lower()}_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def create_client() -> ClientCredentialsEagleViewClient:
    """Create and return configured EagleView client."""
    if not config.validate_config():
        raise ValueError("Missing required configuration. Check environment variables.")
    
    client_config = EagleViewConfig(
        client_id=config.CLIENT_ID,
        client_secret=config.CLIENT_SECRET,
        requests_per_second=config.REQUESTS_PER_SECOND,
        requests_per_minute=config.REQUESTS_PER_MINUTE,
        is_sandbox=config.IS_SANDBOX
    )
    
    return ClientCredentialsEagleViewClient(client_config)

def find_latest_file(pattern: str, directory: str = '.') -> Optional[str]:
    """Find the most recent file matching a pattern."""
    files = glob(os.path.join(directory, pattern))
    if not files:
        return None
    
    # Sort by modification time, newest first
    files.sort(key=os.path.getmtime, reverse=True)
    return files[0]

def load_json_file(filepath: str) -> Optional[Dict[Any, Any]]:
    """Safely load a JSON file with error handling."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.warning(f"File not found: {filepath}")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON in {filepath}: {e}")
        return None
    except Exception as e:
        logging.error(f"Error loading {filepath}: {e}")
        return None

def save_json_file(data: Dict[Any, Any], filepath: str) -> bool:
    """Safely save data to a JSON file."""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        return True
    except Exception as e:
        logging.error(f"Error saving to {filepath}: {e}")
        return False

def create_output_directory(directory: str) -> bool:
    """Create output directory if it doesn't exist."""
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except Exception as e:
        logging.error(f"Error creating directory {directory}: {e}")
        return False
```

### 3. Enhanced Client with Better Error Handling

#### Update `client_credentials_eagleview.py`
```python
# Add better type hints and error handling
from typing import Dict, List, Optional, Union, Any

class EagleViewAPIException(Exception):
    """Custom exception for EagleView API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response
    
    def __str__(self) -> str:
        base_msg = super().__str__()
        if self.status_code:
            return f"{base_msg} (Status: {self.status_code})"
        return base_msg

# Enhanced method signatures with better type hints
def get_property_data_result(self, request_id: str) -> Dict[str, Any]:
    """Get the result of a property data request.
    
    Args:
        request_id: Request ID returned from request_property_data
        
    Returns:
        Property data result or status information
        
    Raises:
        EagleViewAPIException: If API request fails
    """
    # Implementation with better error handling
```

### 4. Refactored Main Scripts

#### Refactored `fetch_reports_client_credentials.py`
```python
"""
Fetch Full Reports using Client Credentials Authentication.
Refactored version with improved structure and error handling.
"""

import sys
import os
from typing import List, Dict, Optional

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils import setup_logging, create_client, save_json_file
from config import get_sandbox_bounds
import config

# Setup logging
logger = setup_logging(__name__)

def fetch_property_data_requests(coordinates: Optional[List[Dict[str, float]]] = None) -> List[Dict]:
    """Fetch property data using Client Credentials authentication.
    
    Args:
        coordinates: List of coordinate dictionaries with 'lat' and 'lon' keys.
                    If None, uses default sandbox coordinates.
        
    Returns:
        List of property data request responses
    """
    try:
        # Validate configuration
        if not config.validate_config():
            logger.error("Invalid configuration. Check environment variables.")
            return []
        
        # Create client
        logger.info("Initializing Client Credentials client...")
        client = create_client()
        
        # Test authentication
        logger.info("Testing authentication...")
        token = client._get_access_token()
        logger.info("Authentication successful!")
        
        # Use provided coordinates or default sandbox coordinates
        if coordinates is None:
            bounds = get_sandbox_bounds()
            coordinates = [
                {"lat": (bounds['min_lat'] + bounds['max_lat']) / 2, 
                 "lon": (bounds['min_lon'] + bounds['max_lon']) / 2},
                {"lat": bounds['min_lat'] + 0.005, "lon": bounds['min_lon'] + 0.005},
                {"lat": bounds['max_lat'] - 0.005, "lon": bounds['max_lon'] - 0.005}
            ]
        
        # Submit property data requests
        logger.info("Submitting property data requests...")
        requests_data = []
        
        for i, coord in enumerate(coordinates):
            logger.info(f"Submitting request {i+1}/{len(coordinates)} for coordinates {coord}")
            try:
                response = client.request_property_data_by_coordinates(coord["lat"], coord["lon"])
                if response and 'request' in response:
                    requests_data.append(response)
                    logger.info(f"  Request ID: {response['request']['id']}")
                else:
                    logger.warning(f"  Failed to submit request for coordinates {coord}")
            except Exception as e:
                logger.error(f"  Error submitting request for coordinates {coord}: {e}")
        
        # Save to JSON
        if requests_data:
            from datetime import datetime
            json_filename = f"eagleview_property_data_requests_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            if save_json_file(requests_data, json_filename):
                logger.info(f"Property data requests saved to: {json_filename}")
            else:
                logger.error(f"Failed to save property data requests to: {json_filename}")
        
        return requests_data
        
    except Exception as e:
        logger.error(f"Unexpected error in fetch_property_data_requests: {e}")
        return []

def main():
    """Main function."""
    print("EagleView Property Data Requests (Client Credentials)")
    print("=" * 60)
    print("NO BROWSER REQUIRED - Fully Automated!")
    print("Using OAuth 2.0 Client Credentials Flow")
    print("Perfect for server-to-server communication")
    print()
    
    # Validate configuration
    if not config.validate_config():
        print("❌ Please set the following environment variables:")
        print("   EAGLEVIEW_CLIENT_ID")
        print("   EAGLEVIEW_CLIENT_SECRET")
        return
    
    requests_data = fetch_property_data_requests()
    
    if requests_data:
        print("\n" + "="*60)
        print("PROCESS COMPLETED SUCCESSFULLY!")
        print(f"Submitted {len(requests_data)} property data requests")
        print("Requests saved to JSON file")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("PROCESS COMPLETED WITH NO REQUESTS")
        print("Check the log file for details")
        print("="*60)

if __name__ == "__main__":
    main()
```

### 5. Command-Line Interface

#### Create `cli.py`
```python
"""
Command-line interface for EagleView API client.
Provides a unified interface for all client operations.
"""

import argparse
import sys
import os
from typing import List

from utils import setup_logging
from config import validate_config
import config

logger = setup_logging(__name__)

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="EagleView API Client")
    parser.add_argument(
        '--operation', 
        choices=['property-data', 'imagery', 'download-images', 'demo'],
        required=True,
        help='Operation to perform'
    )
    parser.add_argument(
        '--coordinates',
        nargs='+',
        help='Coordinates in format "lat,lon" (e.g., "41.25,-95.99")'
    )
    parser.add_argument(
        '--addresses',
        nargs='+',
        help='Addresses to process'
    )
    parser.add_argument(
        '--output-dir',
        default='output',
        help='Output directory for files'
    )
    parser.add_argument(
        '--log-level',
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Logging level'
    )
    
    args = parser.parse_args()
    
    # Setup logging with specified level
    logger = setup_logging(__name__, args.log_level)
    
    # Validate configuration
    if not validate_config():
        logger.error("Missing required configuration. Set EAGLEVIEW_CLIENT_ID and EAGLEVIEW_CLIENT_SECRET environment variables.")
        sys.exit(1)
    
    # Process based on operation
    if args.operation == 'property-data':
        from fetch_reports_client_credentials import fetch_property_data_requests
        coordinates = parse_coordinates(args.coordinates) if args.coordinates else None
        fetch_property_data_requests(coordinates)
    elif args.operation == 'imagery':
        from fetch_images_client_credentials import fetch_imagery
        fetch_imagery()
    elif args.operation == 'download-images':
        from download_images import download_property_images
        download_property_images()
    elif args.operation == 'demo':
        print("EagleView API Client Demo")
        print("=" * 40)
        # Run complete workflow
        run_demo()

def parse_coordinates(coord_strings: List[str]) -> List[dict]:
    """Parse coordinate strings into coordinate dictionaries."""
    coordinates = []
    for coord_str in coord_strings:
        try:
            lat, lon = map(float, coord_str.split(','))
            coordinates.append({"lat": lat, "lon": lon})
        except ValueError:
            logger.warning(f"Invalid coordinate format: {coord_str}")
    return coordinates

def run_demo():
    """Run the complete demo workflow."""
    logger.info("Starting demo workflow...")
    # Implementation here
    pass

if __name__ == "__main__":
    main()
```

## Implementation Priority

### Phase 1: Foundation (High Priority)
1. Create `config.py` with environment variable support
2. Create `utils.py` with common utility functions
3. Update `.gitignore` to exclude environment files
4. Add environment variable documentation

### Phase 2: Core Refactoring (Medium Priority)
1. Refactor main scripts to use new utilities
2. Improve type hints and docstrings
3. Enhance error handling and logging
4. Add graceful fallbacks for missing files

### Phase 3: Advanced Features (Low Priority)
1. Create CLI interface
2. Add configuration validation
3. Implement retry mechanisms
4. Add comprehensive unit tests

## Benefits of Refactoring

1. **Security**: Eliminate hardcoded credentials
2. **Maintainability**: Reduce code duplication
3. **Flexibility**: Environment-based configuration
4. **Reliability**: Better error handling and logging
5. **Usability**: Unified CLI interface
6. **Scalability**: Modular design for future enhancements

## Testing Strategy

1. **Unit Tests**: Test individual functions and utilities
2. **Integration Tests**: Test API interactions
3. **Regression Tests**: Ensure existing functionality remains intact
4. **Edge Case Tests**: Test error conditions and fallbacks

## Migration Guide

For existing users:
1. Set environment variables instead of modifying code
2. Update import paths if necessary
3. Review new configuration options
4. Test with sample data before production use