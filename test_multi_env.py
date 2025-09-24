#!/usr/bin/env python3
"""
Multi-environment architecture test script
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, '.')

from src.eagleview.config import create_config
from src.eagleview.client import create_client
from src.eagleview.services import PropertyDataService


def test_multi_environment():
    """Test the multi-environment functionality."""
    print("Testing Multi-Environment Architecture")
    print("="*50)
    
    # Test Sandbox Configuration
    print("\n1. Testing Sandbox Configuration:")
    sandbox_config = create_config('sandbox')
    print("   Environment: {}".format(sandbox_config.environment))
    print("   Is Sandbox: {}".format(sandbox_config.is_sandbox))
    print("   Base URL: {}".format(sandbox_config.base_url))
    print("   Imagery URL: {}".format(sandbox_config.imagery_base_url))
    print("   Requests per sec: {}".format(sandbox_config.requests_per_second))
    print("   Validate coordinates: {}".format(sandbox_config.validate_coordinates))
    
    # Test Production Configuration
    print("\n2. Testing Production Configuration:")
    prod_config = create_config('production')
    print("   Environment: {}".format(prod_config.environment))
    print("   Is Sandbox: {}".format(prod_config.is_sandbox))
    print("   Base URL: {}".format(prod_config.base_url))
    print("   Imagery URL: {}".format(prod_config.imagery_base_url))
    print("   Requests per sec: {}".format(prod_config.requests_per_second))
    print("   Validate coordinates: {}".format(prod_config.validate_coordinates))
    
    # Test Client Creation
    print("\n3. Testing Client Creation:")
    sandbox_client = create_client(sandbox_config)
    print("   Client environment: {}".format(sandbox_client.environment))
    print("   Client is_sandbox: {}".format(sandbox_client.is_sandbox))
    print("   Client base URL: {}".format(sandbox_client.base_url))
    
    prod_client = create_client(prod_config)
    print("   Client environment: {}".format(prod_client.environment))
    print("   Client is_sandbox: {}".format(prod_client.is_sandbox))
    print("   Client base URL: {}".format(prod_client.base_url))
    
    # Test Service Creation
    print("\n4. Testing Service Creation:")
    sandbox_service = PropertyDataService(sandbox_client)
    print("   Service environment: {}".format(sandbox_service.environment))
    print("   Service is_sandbox: {}".format(sandbox_service.is_sandbox))
    
    prod_service = PropertyDataService(prod_client)
    print("   Service environment: {}".format(prod_service.environment))
    print("   Service is_sandbox: {}".format(prod_service.is_sandbox))
    
    # Test sandbox coordinates
    print("\n5. Testing Sandbox Coordinates:")
    sandbox_coords = sandbox_service.get_sandbox_coordinates()
    print("   Sample coordinates: {}".format(sandbox_coords))
    
    print("\nMulti-Environment Architecture Test Complete!")
    print("="*50)


if __name__ == "__main__":
    test_multi_environment()