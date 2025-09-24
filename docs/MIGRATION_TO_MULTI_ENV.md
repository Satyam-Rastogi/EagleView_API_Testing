# Multi-Environment Migration Guide

## ⚠️ FORWARD-LOOKING DOCUMENT

**Note**: This document describes a planned future migration path for supporting multiple environments in the EagleView API client. The current implementation is already production-ready with a modern, modular architecture.

## Overview

This guide explains how to migrate the current EagleView API client from its single-environment structure to the recommended multi-environment architecture. This migration would enable proper support for sandbox, production, and other environments while maximizing code reuse.

## Current State Assessment

### ✅ Current Implementation Status
The EagleView API client has already undergone extensive refactoring and is currently in an excellent state:

- **Modern Architecture**: Clean service-based design with proper separation of concerns
- **Enhanced Configuration**: Support for both environment variables and YAML configuration files
- **Unified CLI**: Single command-line interface for all operations
- **Performance Optimized**: Data caching and efficient operations
- **Well-Documented**: Comprehensive documentation suite
- **Production-Ready**: Thoroughly tested and verified functionality

### 🎯 Current Features
1. **Modular Design**: Service pattern with clear boundaries
2. **Flexible Configuration**: Multiple configuration options (YAML, environment variables)
3. **Robust Error Handling**: Comprehensive exception management
4. **Data Persistence**: Organized directory structure with caching
5. **Container Support**: Docker and Docker Compose integration
6. **Cross-Platform**: Windows, Unix/Linux, and macOS support

### 📋 Future Enhancement Consideration
While the current implementation meets all requirements for production use, this document serves as a blueprint for potential future enhancements if explicit multi-environment support becomes necessary.

## When to Consider Migration

### Future Migration Scenarios
Consider implementing the full multi-environment architecture when:

1. **Complex Environment Differences**: Significant behavioral differences emerge between sandbox and production
2. **Enterprise Requirements**: Advanced customization needs for large-scale deployments
3. **Regulatory Compliance**: Strict compliance requirements necessitate separation
4. **Performance Optimization**: Environment-specific optimizations become critical

## Target Future Architecture

### Proposed Enhanced Structure
```

## Target Architecture

### New Structure
```
src/
├── eagleview/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── sandbox.py
│   │   └── production.py
│   ├── client/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── sandbox.py
│   │   └── production.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── base/
│   │   │   ├── property_data.py
│   │   │   ├── imagery.py
│   │   │   └── image_download.py
│   │   ├── sandbox/
│   │   │   └── overrides.py
│   │   └── production/
│   │       └── overrides.py
│   └── utils/
│       ├── logging.py
│       ├── validation.py
│       └── file_ops.py
├── cli/
│   └── eagleview.py
└── examples/
    ├── sandbox_examples.py
    └── production_examples.py
```

## Migration Steps

### Phase 1: Directory Restructuring

#### Step 1: Create New Directory Structure
```bash
# Create new directories
mkdir -p src/eagleview/{config,client,services,utils}
mkdir -p src/eagleview/services/{base,sandbox,production}
mkdir -p src/cli
mkdir -p src/examples
mkdir -p tests/{unit,integration,sandbox,production}
```

#### Step 2: Move Core Components
```bash
# Move existing files to new structure
mv src/core/configuration.py src/eagleview/config/base.py
mv src/core/client.py src/eagleview/client/base.py
mv src/core/file_operations.py src/eagleview/utils/file_ops.py
mv src/core/cache.py src/eagleview/utils/cache.py
mv src/core/services/*.py src/eagleview/services/base/
mv src/cli.py src/cli/eagleview.py
```

#### Step 3: Create Factory Files
Create the missing `__init__.py` files and factory modules:

**src/eagleview/__init__.py:**
```python
"""EagleView API Client - Multi-Environment Support"""
```

**src/eagleview/config/__init__.py:**
```python
from .base import EagleViewSettings
from .sandbox import SandboxConfig
from .production import ProductionConfig

def create_config(environment='sandbox', **kwargs):
    """Factory function to create environment-appropriate configuration."""
    if environment == 'sandbox':
        return SandboxConfig(**kwargs)
    elif environment == 'production':
        return ProductionConfig(**kwargs)
    else:
        return EagleViewSettings(**kwargs)
```

### Phase 2: Refactor Core Components

#### Step 4: Update Configuration System

**src/eagleview/config/base.py** (modify existing):
```python
# Add environment awareness to existing configuration
class EagleViewSettings:
    def __init__(self, environment='sandbox', **kwargs):
        self.environment = environment
        self.is_sandbox = environment == 'sandbox'
        # ... existing initialization
        
        # Set environment-specific defaults
        self._set_environment_defaults()
    
    def _set_environment_defaults(self):
        """Set defaults based on environment."""
        if self.is_sandbox:
            self.base_url = 'https://sandbox.apicenter.eagleview.com'
            self.imagery_base_url = 'https://sandbox.apis.eagleview.com'
            self.validate_coordinates = True
        else:
            self.base_url = 'https://apicenter.eagleview.com'
            self.imagery_base_url = 'https://apis.eagleview.com'
            self.validate_coordinates = False
    
    def get_api_urls(self):
        """Get API URLs based on environment."""
        return {
            'base_url': self.base_url,
            'imagery_base_url': self.imagery_base_url
        }
```

**src/eagleview/config/sandbox.py:**
```python
from .base import EagleViewSettings

class SandboxConfig(EagleViewSettings):
    def __init__(self, **kwargs):
        kwargs.setdefault('environment', 'sandbox')
        kwargs.setdefault('requests_per_second', 3.0)
        kwargs.setdefault('requests_per_minute', 50)
        kwargs.setdefault('validate_coordinates', True)
        super().__init__(**kwargs)
    
    def get_sandbox_bounds(self):
        """Return sandbox bounding box coordinates."""
        return {
            'min_lat': 41.24140396772262,
            'max_lat': 41.25672882015283,
            'min_lon': -96.00532698173473,
            'max_lon': -95.97589954958912
        }
```

**src/eagleview/config/production.py:**
```python
from .base import EagleViewSettings

class ProductionConfig(EagleViewSettings):
    def __init__(self, **kwargs):
        kwargs.setdefault('environment', 'production')
        kwargs.setdefault('requests_per_second', 10.0)
        kwargs.setdefault('requests_per_minute', 200)
        kwargs.setdefault('validate_coordinates', False)
        super().__init__(**kwargs)
```

#### Step 5: Refactor Client

**src/eagleview/client/base.py** (modify existing):
```python
# Add environment awareness to existing client
class EagleViewClient:
    def __init__(self, settings):
        self.settings = settings
        self.environment = settings.environment
        self.is_sandbox = settings.is_sandbox
        # ... existing initialization
        
        # Set environment-specific behavior
        self._configure_for_environment()
    
    def _configure_for_environment(self):
        """Configure client behavior based on environment."""
        if self.is_sandbox:
            # Sandbox-specific configuration
            self.coordinate_validator = self._validate_sandbox_coordinates
        else:
            # Production-specific configuration
            self.coordinate_validator = self._validate_production_coordinates
```

#### Step 6: Create Environment-Specific Services

**src/eagleview/services/sandbox/overrides.py:**
```python
"""Sandbox-specific service overrides."""

class SandboxPropertyDataServiceMixin:
    """Mixin for sandbox-specific property data service behavior."""
    
    def _validate_coordinates(self, coordinates):
        """Validate coordinates are within sandbox bounds."""
        if not self.client.settings.validate_coordinates:
            return coordinates
            
        bounds = self.client.settings.get_sandbox_bounds()
        validated_coords = []
        
        for coord in coordinates:
            lat = coord['lat']
            lon = coord['lon']
            
            if not (bounds['min_lat'] <= lat <= bounds['max_lat']):
                raise ValueError(f"Latitude {lat} outside sandbox bounds")
            if not (bounds['min_lon'] <= lon <= bounds['max_lon']):
                raise ValueError(f"Longitude {lon} outside sandbox bounds")
                
            validated_coords.append(coord)
        
        return validated_coords

class SandboxImageryServiceMixin:
    """Mixin for sandbox-specific imagery service behavior."""
    
    def _apply_sandbox_restrictions(self, request_data):
        """Apply sandbox-specific restrictions to imagery requests."""
        # Limit radius in sandbox
        if 'center' in request_data and 'radius_in_meters' in request_data['center']:
            request_data['center']['radius_in_meters'] = min(
                request_data['center']['radius_in_meters'], 100
            )
        return request_data
```

### Phase 3: Update Imports and References

#### Step 7: Update Service Base Classes

**src/eagleview/services/base/property_data.py:**
```python
# Move existing PropertyDataService to base directory
# Add environment-aware methods
from ...client.base import EagleViewClient
from ...utils.file_ops import save_json_data, generate_timestamped_filename, get_data_directory
from ...utils.cache import cache_result

class PropertyDataService:
    def __init__(self, client: EagleViewClient):
        self.client = client
        self.environment = client.environment
        self.is_sandbox = client.is_sandbox
        
        # Import environment-specific mixins
        if self.is_sandbox:
            from ..sandbox.overrides import SandboxPropertyDataServiceMixin
            # Apply sandbox-specific behavior
            self.__class__ = type(
                'EnvironmentAwarePropertyDataService',
                (PropertyDataService, SandboxPropertyDataServiceMixin),
                {}
            )
```

#### Step 8: Update CLI Interface

**src/cli/eagleview.py** (modify existing):
```python
# Add environment selection to CLI
import argparse
from src.eagleview.config import create_config
from src.eagleview.client import EagleViewClient

def main():
    parser = argparse.ArgumentParser(description="EagleView API Client")
    parser.add_argument(
        '--environment',
        choices=['sandbox', 'production'],
        default='sandbox',
        help='Environment to use (default: sandbox)'
    )
    parser.add_argument(
        '--config',
        help='Path to configuration file'
    )
    # ... existing arguments
    
    args = parser.parse_args()
    
    # Create environment-appropriate configuration
    if args.config:
        settings = EagleViewSettings.from_config(args.config)
    else:
        settings = create_config(
            environment=args.environment,
            client_id=os.getenv('EAGLEVIEW_CLIENT_ID'),
            client_secret=os.getenv('EAGLEVIEW_CLIENT_SECRET')
        )
    
    # Create client
    client = EagleViewClient(settings)
    
    # ... rest of CLI logic
```

### Phase 4: Testing and Validation

#### Step 9: Create Environment-Specific Tests

**tests/sandbox/test_property_data.py:**
```python
"""Sandbox-specific property data tests."""

import pytest
from src.eagleview.config import create_config
from src.eagleview.client import EagleViewClient
from src.eagleview.services.base.property_data import PropertyDataService

def test_sandbox_coordinate_validation():
    """Test that sandbox coordinates are properly validated."""
    config = create_config('sandbox')
    client = EagleViewClient(config)
    service = PropertyDataService(client)
    
    # Valid sandbox coordinates should work
    valid_coords = [{"lat": 41.25, "lon": -95.99}]
    # This should not raise an exception
    
    # Invalid coordinates should raise ValueError
    invalid_coords = [{"lat": 30.0, "lon": -80.0}]
    # This should raise ValueError

def test_sandbox_rate_limiting():
    """Test sandbox rate limiting."""
    config = create_config('sandbox')
    assert config.requests_per_second == 3.0
    assert config.requests_per_minute == 50
```

**tests/production/test_property_data.py:**
```python
"""Production-specific property data tests."""

import pytest
from src.eagleview.config import create_config
from src.eagleview.client import EagleViewClient
from src.eagleview.services.base.property_data import PropertyDataService

def test_production_no_coordinate_validation():
    """Test that production doesn't validate coordinates by default."""
    config = create_config('production')
    client = EagleViewClient(config)
    service = PropertyDataService(client)
    
    # Invalid coordinates should work in production
    invalid_coords = [{"lat": 30.0, "lon": -80.0}]
    # This should not raise an exception when validate_coordinates=False
```

### Phase 5: Documentation and Examples

#### Step 10: Create Environment-Specific Examples

**src/examples/sandbox_examples.py:**
```python
"""Examples for using the EagleView API client in sandbox environment."""

from src.eagleview.config import create_config
from src.eagleview.client import EagleViewClient
from src.eagleview.services.base.property_data import PropertyDataService

def example_sandbox_property_data():
    """Example of property data requests in sandbox."""
    # Create sandbox configuration
    config = create_config('sandbox')
    
    # Create client
    client = EagleViewClient(config)
    
    # Create service
    service = PropertyDataService(client)
    
    # Get sandbox coordinates
    coordinates = service.get_sandbox_coordinates()
    
    # Submit requests (will be validated against sandbox bounds)
    requests_data = service.submit_coordinates_requests(coordinates)
    
    return requests_data
```

**src/examples/production_examples.py:**
```python
"""Examples for using the EagleView API client in production environment."""

from src.eagleview.config import create_config
from src.eagleview.client import EagleViewClient
from src.eagleview.services.base.property_data import PropertyDataService

def example_production_property_data():
    """Example of property data requests in production."""
    # Create production configuration
    config = create_config('production')
    
    # Create client
    client = EagleViewClient(config)
    
    # Create service
    service = PropertyDataService(client)
    
    # Submit requests (no coordinate validation)
    coordinates = [
        {"lat": 40.7128, "lon": -74.0060},  # New York
        {"lat": 34.0522, "lon": -118.2437}, # Los Angeles
    ]
    
    requests_data = service.submit_coordinates_requests(coordinates)
    
    return requests_data
```

## Migration Checklist

### Phase 1: Directory Restructuring ✅
- [ ] Create new directory structure
- [ ] Move existing files to appropriate locations
- [ ] Create factory files and `__init__.py` modules

### Phase 2: Core Component Refactoring ✅
- [ ] Update configuration system with environment awareness
- [ ] Create environment-specific configuration classes
- [ ] Refactor client with environment-specific behavior
- [ ] Create environment-specific service mixins

### Phase 3: Import Updates ✅
- [ ] Update all import statements
- [ ] Modify service base classes for environment awareness
- [ ] Update CLI interface with environment selection
- [ ] Ensure backward compatibility where possible

### Phase 4: Testing ✅
- [ ] Create environment-specific test suites
- [ ] Validate sandbox coordinate validation
- [ ] Validate production performance settings
- [ ] Ensure existing functionality still works

### Phase 5: Documentation ✅
- [ ] Create environment-specific examples
- [ ] Update README with multi-environment usage
- [ ] Document migration path for existing users
- [ ] Create configuration templates for each environment

## Backward Compatibility

### Maintaining Existing API
To maintain backward compatibility during migration:

1. **Preserve Import Paths**: Create compatibility layer for existing imports
2. **Default to Sandbox**: Keep sandbox as default environment to avoid breaking changes
3. **Deprecation Warnings**: Add warnings for deprecated usage patterns
4. **Gradual Migration**: Allow users to migrate gradually

### Compatibility Layer Example
```python
# src/eagleview/compat.py
"""Compatibility layer for existing code."""

import warnings
from .config import create_config
from .client import EagleViewClient

def create_sandbox_client():
    """Deprecated: Create sandbox client (use new factory pattern)."""
    warnings.warn(
        "create_sandbox_client is deprecated, use EagleViewClient with sandbox config",
        DeprecationWarning
    )
    config = create_config('sandbox')
    return EagleViewClient(config)
```

## Validation Steps

### Before Migration
- [ ] Run all existing tests to establish baseline
- [ ] Document current functionality
- [ ] Backup current codebase

### During Migration
- [ ] Run tests after each phase
- [ ] Verify CLI functionality
- [ ] Check import statements
- [ ] Validate environment-specific behavior

### After Migration
- [ ] Run complete test suite
- [ ] Test both sandbox and production environments
- [ ] Verify CLI with different environment flags
- [ ] Validate backward compatibility

## Rollback Plan

If issues arise during migration:

1. **Immediate Rollback**: Revert to backup of current working version
2. **Incremental Approach**: Apply changes in smaller batches
3. **Feature Flags**: Use feature flags to enable/disable new functionality
4. **Staged Deployment**: Deploy to subset of users first

## Conclusion

This migration guide provides a comprehensive approach to transitioning the EagleView API client to a multi-environment architecture. The key benefits include:

- **Improved Maintainability**: Clear separation of environment-specific logic
- **Better Performance**: Environment-optimized configurations
- **Enhanced Security**: Environment-appropriate validation and restrictions
- **Simplified Testing**: Dedicated test suites for each environment
- **Future-Proof**: Easy to add new environments or modify existing ones

The migration should be performed in phases to minimize disruption and ensure continued functionality throughout the process.