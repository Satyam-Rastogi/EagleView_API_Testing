# Multi-Environment Architecture for EagleView API Client

## ⚠️ FORWARD-LOOKING DOCUMENT

**Note**: This document describes a planned future architecture for supporting multiple environments (sandbox, production, development) in the EagleView API client. It is intended as a blueprint for future enhancement rather than documentation of current functionality.

## Overview

This document outlines the recommended architecture for supporting multiple environments (sandbox, production, development) in the EagleView API client. The goal is to maximize code reuse while allowing environment-specific customization.

## Current Status

The current EagleView API client has been successfully refactored with a modern, modular architecture that provides a solid foundation for multi-environment support. The current implementation includes:

### ✅ Current Features
- **Modern Modular Design**: Clean service-based architecture with clear separation of concerns
- **Enhanced Configuration Management**: Support for both environment variables and YAML configuration files
- **Unified CLI Interface**: Single command-line interface for all operations
- **Data Caching**: Performance optimization through intelligent caching
- **Standardized Data Structure**: Organized directory layout for all data types
- **Comprehensive Error Handling**: Robust error management with retry logic and detailed logging
- **Flexible Deployment Options**: Native installation, Docker containers, and Docker Compose support

### 📋 Future Enhancement Opportunity
While the current implementation is production-ready and highly functional, there may be future opportunities to enhance the architecture with explicit multi-environment support as described in this document.

## Future Recommendations

### When to Consider Multi-Environment Architecture
Consider implementing the full multi-environment architecture when:

1. **Complex Environment Differences**: Significant behavioral differences between sandbox and production environments
2. **Advanced Customization Needs**: Requirements for extensive environment-specific customization
3. **Large Scale Deployment**: Enterprise-level deployments with complex environment management needs
4. **Regulatory Compliance**: Strict compliance requirements that necessitate separate environment implementations

## Proposed Future Architecture

### Environment-Aware Single Codebase Approach

For future consideration, if explicit multi-environment support becomes necessary:

```

## Recommended Architecture

### Environment-Aware Single Codebase Approach

```
src/
├── eagleview/
│   ├── __init__.py          # Package initialization
│   ├── config/
│   │   ├── __init__.py      # Config factory
│   │   ├── base.py          # Base configuration
│   │   ├── sandbox.py       # Sandbox configuration
│   │   └── production.py    # Production configuration
│   │
│   ├── client/
│   │   ├── __init__.py      # Client factory
│   │   ├── base.py          # Base client
│   │   ├── sandbox.py       # Sandbox client
│   │   └── production.py    # Production client
│   │
│   ├── services/
│   │   ├── __init__.py      # Service factory
│   │   ├── base/
│   │   │   ├── property_data.py
│   │   │   ├── imagery.py
│   │   │   └── image_download.py
│   │   ├── sandbox/
│   │   │   └── overrides.py # Sandbox-specific overrides
│   │   └── production/
│   │       └── overrides.py # Production-specific overrides
│   │
│   └── utils/
│       ├── logging.py       # Shared logging
│       ├── validation.py    # Shared validation
│       └── file_ops.py      # Shared file operations
│
├── cli/
│   └── eagleview.py         # Unified CLI
│
└── examples/
    ├── sandbox_examples.py
    └── production_examples.py
```

## Key Design Principles

### 1. Factory Pattern
Use factories to create environment-appropriate instances:

```python
# src/eagleview/client/__init__.py
from .base import EagleViewClient
from .sandbox import SandboxClient
from .production import ProductionClient

def create_client(environment='sandbox'):
    if environment == 'sandbox':
        return SandboxClient()
    elif environment == 'production':
        return ProductionClient()
    else:
        return EagleViewClient()
```

### 2. Configuration-Driven
Let configuration determine behavior:

```python
# src/eagleview/config/base.py
class BaseConfig:
    def __init__(self, environment='sandbox'):
        self.environment = environment
        self.is_sandbox = environment == 'sandbox'
        self.setup_environment()
    
    def setup_environment(self):
        if self.is_sandbox:
            self.base_url = 'https://sandbox.apicenter.eagleview.com'
            self.imagery_url = 'https://sandbox.apis.eagleview.com'
        else:
            self.base_url = 'https://apicenter.eagleview.com'
            self.imagery_url = 'https://apis.eagleview.com'
```

### 3. Inheritance for Overrides
Use inheritance for environment-specific behavior:

```python
# src/eagleview/client/base.py
class BaseEagleViewClient:
    def __init__(self, config):
        self.config = config
        self.setup_client()
    
    def setup_client(self):
        # Base client setup
        pass
    
    def make_request(self, *args, **kwargs):
        # Base request logic
        pass

# src/eagleview/client/sandbox.py
class SandboxClient(BaseEagleViewClient):
    def setup_client(self):
        super().setup_client()
        # Sandbox-specific setup
        self.rate_limit = 3  # Lower rate limit for sandbox
    
    def validate_coordinates(self, lat, lon):
        # Sandbox coordinate validation
        bounds = {
            'min_lat': 41.24140396772262,
            'max_lat': 41.25672882015283,
            'min_lon': -96.00532698173473,
            'max_lon': -95.97589954958912
        }
        # Validate coordinates are within sandbox bounds
```

### 4. Strategy Pattern
Use strategy pattern for environment-specific behavior:

```python
# src/eagleview/services/base/property_data.py
class PropertyDataService:
    def __init__(self, client, validator_strategy=None):
        self.client = client
        self.validator = validator_strategy or DefaultValidator()
    
    def submit_coordinates_requests(self, coordinates):
        # Validate coordinates using strategy
        validated_coords = [self.validator.validate(coord) for coord in coordinates]
        # Submit requests
        pass

# src/eagleview/services/sandbox/validator.py
class SandboxValidator:
    def validate(self, coordinate):
        # Sandbox-specific validation
        pass

# src/eagleview/services/production/validator.py
class ProductionValidator:
    def validate(self, coordinate):
        # Production-specific validation
        pass
```

## Directory Structure Details

### Shared Components (`src/eagleview/utils/`)
- **logging.py**: Standardized logging across all environments
- **validation.py**: Common validation utilities
- **file_ops.py**: Shared file operations and data handling

### Configuration (`src/eagleview/config/`)
- **base.py**: Base configuration class with common settings
- **sandbox.py**: Sandbox-specific configuration and constraints
- **production.py**: Production-specific configuration and optimizations

### Client (`src/eagleview/client/`)
- **base.py**: Base client with common API interactions
- **sandbox.py**: Sandbox client with rate limiting and validation
- **production.py**: Production client with optimizations and monitoring

### Services (`src/eagleview/services/`)
- **base/**: Core service implementations
  - `property_data.py`: Property data service base
  - `imagery.py`: Imagery service base
  - `image_download.py`: Image download service base
- **sandbox/**: Sandbox-specific overrides and constraints
- **production/**: Production-specific optimizations and features

## Benefits of This Approach

### 1. Maximum Code Reuse (80-90%)
- Core logic shared across environments
- Common utilities and helpers
- Unified error handling and logging

### 2. Easier Maintenance
- Single codebase to maintain
- Clear separation of concerns
- Environment-specific logic isolated

### 3. Better Testing
- Shared test infrastructure
- Environment-specific test suites
- Easy to mock different environments

### 4. Simpler Deployment
- Single package for all environments
- Environment selected at runtime
- Reduced deployment complexity

### 5. Clear Separation
- Well-defined interfaces between shared and environment-specific code
- Easy to add new environments
- Clear boundaries for customization

## Implementation Strategy

### Phase 1: Refactor Current Code
1. Move current implementation to `src/eagleview/` structure
2. Create base classes for all components
3. Implement factory patterns
4. Set up configuration system

### Phase 2: Environment-Specific Customization
1. Create sandbox-specific overrides
2. Create production-specific optimizations
3. Implement environment detection
4. Add environment-specific validation

### Phase 3: Testing and Documentation
1. Create environment-specific test suites
2. Document environment differences
3. Create examples for each environment
4. Update CLI to support environment selection

## CLI Interface for Multi-Environment

```bash
# Select environment via command line
python -m eagleview --environment sandbox --operation property-data
python -m eagleview --environment production --operation property-data

# Configuration file per environment
python -m eagleview --config config/sandbox.yaml --operation property-data
python -m eagleview --config config/production.yaml --operation property-data

# Environment variables
EAGLEVIEW_ENVIRONMENT=production python -m eagleview --operation property-data
```

## Testing Strategy

### Shared Tests
- Core functionality tests
- Integration tests with mocked APIs
- Performance tests
- Security tests

### Environment-Specific Tests
- `tests/sandbox/`: Sandbox-specific constraint tests
- `tests/production/`: Production-specific optimization tests
- `tests/integration/`: Cross-environment integration tests

## Configuration Management

### Environment Detection Priority
1. Command-line argument
2. Environment variable
3. Configuration file
4. Default (sandbox)

### Sample Configuration Files

**config/sandbox.yaml:**
```yaml
eagleview:
  environment: sandbox
  client_id: "sandbox_client_id"
  client_secret: "sandbox_client_secret"
  rate_limit: 3
  timeout: 30
  validate_coordinates: true
```

**config/production.yaml:**
```yaml
eagleview:
  environment: production
  client_id: "production_client_id"
  client_secret: "production_client_secret"
  rate_limit: 10
  timeout: 10
  validate_coordinates: false
```

## Migration Path

### From Current Structure
1. Create new `src/eagleview/` directory structure
2. Move existing code to appropriate locations
3. Create base classes and factories
4. Implement environment-specific overrides
5. Update imports throughout the codebase
6. Update CLI to support environment selection
7. Update documentation and examples

### Backward Compatibility
- Maintain existing import paths where possible
- Provide compatibility layer for old API
- Clear migration guide for users
- Deprecation warnings for old patterns

## Conclusion

The recommended environment-aware single codebase approach provides the best balance of code reuse and environment-specific customization. It maintains a clean, organized structure while allowing for the flexibility needed to handle different EagleView API environments effectively.

This architecture will make the EagleView API client more robust, maintainable, and suitable for production use across different deployment scenarios.