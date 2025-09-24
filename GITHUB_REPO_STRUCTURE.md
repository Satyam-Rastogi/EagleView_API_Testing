# EagleView API Client - GitHub Repository Structure

## Files to Push to GitHub

### 📁 Source Code (`src/eagleview/`)
- `src/eagleview/__init__.py` - Package initialization
- `src/eagleview/config/__init__.py` - Configuration factory module
- `src/eagleview/config/base.py` - Base configuration with environment awareness
- `src/eagleview/config/sandbox.py` - Sandbox-specific configuration
- `src/eagleview/config/production.py` - Production-specific configuration
- `src/eagleview/client/__init__.py` - Client factory module
- `src/eagleview/client/base.py` - Base client with multi-environment support
- `src/eagleview/services/__init__.py` - Services module initialization
- `src/eagleview/services/base/__init__.py` - Base services module
- `src/eagleview/services/base/property_data_service.py` - Property data service with environment awareness
- `src/eagleview/services/base/imagery_service.py` - Imagery service with environment awareness
- `src/eagleview/services/base/image_download_service.py` - Image download service with environment awareness
- `src/eagleview/services/sandbox/__init__.py` - Sandbox service modules
- `src/eagleview/services/sandbox/overrides.py` - Sandbox-specific service behavior
- `src/eagleview/services/production/__init__.py` - Production service modules
- `src/eagleview/services/production/overrides.py` - Production-specific service behavior
- `src/eagleview/utils/__init__.py` - Utilities module initialization
- `src/eagleview/utils/file_ops.py` - File operations utilities with multi-environment support
- `src/eagleview/utils/cache.py` - Caching utilities with multi-environment support

### 📁 Command Line Interface (`cli/`)
- `cli/eagleview.py` - Main CLI with environment selection support

### 📁 Examples (`examples/`)
- `examples/sandbox_examples.py` - Sandbox environment usage examples
- `examples/production_examples.py` - Production environment usage examples

### 📁 Documentation (`docs/`)
- `docs/MULTI_ENVIRONMENT_ARCHITECTURE.md` - Multi-environment architecture blueprint
- `docs/MIGRATION_TO_MULTI_ENV.md` - Multi-environment migration guide
- `docs/README.md` - Main documentation
- `docs/GETTING_STARTED.md` - Getting started guide
- `docs/SETUP_GUIDE.md` - Setup guide
- `docs/CODE_QUALITY_ANALYSIS.md` - Code quality documentation
- `docs/CURRENT_STATUS.md` - Current implementation status
- `docs/COMPREHENSIVE_EXAMPLES.md` - Comprehensive usage examples
- `docs/DEMO_SUMMARY.md` - Demo summary documentation
- `docs/CUSTOMIZABILITY.md` - Customizability guide
- `docs/IMAGE_DOWNLOAD_SERVICE.md` - Image download service documentation
- `docs/IMAGE_DOWNLOAD_IMPLEMENTATION_STATUS.md` - Image download implementation status

### 📁 Configuration Examples (`config/`)
- `config/eagleview.yaml` - Example configuration file for different environments
- `config/eagleview_sandbox.yaml` - Example sandbox configuration
- `config/eagleview_production.yaml` - Example production configuration

### 📁 Demo Files (`demo_*.py`)
- `demo_programmatic_usage.py` - Programmatic usage examples
- `demo_cli_functionality.py` - CLI functionality examples
- `demo_image_download_functionality.py` - Image download functionality examples
- `demo_all_functionalities.py` - All functionalities demo
- `demo_comprehensive.py` - Comprehensive demo
- `demo_summary.py` - Demo summary

### 📁 Scripts and Utilities (`scripts/`)
- `scripts/eagleview.py` - Original CLI script (for reference)
- `scripts/cleanup_redundant_files.py` - Cleanup utilities

### 📄 Root Files
- `README.md` - Main project README
- `DEMO_README.md` - Demo-specific README
- `pyproject.toml` - Project dependencies and build configuration
- `docker-compose.yml` - Docker Compose configuration
- `Dockerfile` - Docker image configuration
- `Makefile` - Make utilities
- `run_all_demos.py` - Script to run all demos
- `simple_cli_demo.py` - Simple CLI demo
- `simple_demo_runner.py` - Simple demo runner
- `simple_programmatic_demo.py` - Simple programmatic demo
- `setup.sh` - Unix setup script
- `setup.bat` - Windows batch setup
- `setup.ps1` - Windows PowerShell setup
- `.gitignore` - Git ignore rules

### 📄 Test Files (`tests/`)
- `tests/unit/` - Unit tests
- `tests/integration/` - Integration tests
- `tests/sandbox/` - Sandbox-specific tests
- `tests/production/` - Production-specific tests

---

## 📊 Sample Output Data Structures

### Environment Configuration Output
```json
{
  "environment": "sandbox",
  "is_sandbox": true,
  "base_url": "https://sandbox.apicenter.eagleview.com",
  "imagery_base_url": "https://sandbox.apis.eagleview.com",
  "requests_per_second": 3.0,
  "requests_per_minute": 50,
  "validate_coordinates": true
}
```

### Property Data Request Output
```json
{
  "request": {
    "id": "17a4d3b0-dbb4-4f86-84e2-3882df406936",
    "status": "accepted",
    "timestamp": "2025-09-24T13:06:52.433Z"
  },
  "coordinates": {
    "lat": 41.25,
    "lon": -95.99
  },
  "environment": "sandbox"
}
```

### Imagery Service Response Output
```json
{
  "location": "demo_location_1",
  "coordinates": {
    "lat": 41.25,
    "lon": -95.99
  },
  "imagery_data": {
    "images_available": 15,
    "image_tokens": ["token1", "token2", ...],
    "metadata": {
      "date_range": "2024-01-01 to 2024-12-31",
      "resolution": "high",
      "coverage": "full_property"
    }
  },
  "environment": "sandbox"
}
```

### CLI Environment Output
```
EagleView API Client Demo
========================================
Environment: sandbox
Base URL: https://sandbox.apicenter.eagleview.com
1. Submitting property data requests...
   Submitted 3 property data requests
2. Requesting imagery...
   Retrieved imagery for demo_location_1
Demo workflow completed!
```

### Configuration Factory Usage Output
```
Testing Multi-Environment Architecture
==================================================

1. Testing Sandbox Configuration:
   Environment: sandbox
   Is Sandbox: True
   Base URL: https://sandbox.apicenter.eagleview.com
   Imagery URL: https://sandbox.apis.eagleview.com
   Requests per sec: 3.0
   Validate coordinates: True

2. Testing Production Configuration:
   Environment: production
   Is Sandbox: False
   Base URL: https://apicenter.eagleview.com
   Imagery URL: https://apis.eagleview.com
   Requests per sec: 10.0
   Validate coordinates: False
```

### Sandbox Coordinates Output
```json
[
  {
    "lat": 41.25,
    "lon": -95.99
  },
  {
    "lat": 41.245,
    "lon": -95.98
  },
  {
    "lat": 41.255,
    "lon": -96.0
  }
]
```

### Error Handling Output
```
2025-09-24 13:08:06,299 - src.eagleview.client.base - ERROR - Error requesting property data: API request failed after 3 attempts: 401 - {"message":"Please use the production app credentials"} (Status: 401)
```

### File Structure Output Example
```
data/
├── cache/                 # Cached API responses
│   └── *.json
├── imagery/              # Downloaded images
│   ├── downloaded_images/
│   ├── address_based_images/
│   ├── custom_location_images/
│   └── *.json (imagery data)
├── requests/             # Property data requests
│   └── *.json
├── results/              # Property data results
│   └── *.json
└── tokens/               # Authentication tokens
    └── *.json
```

## 🚀 Key Features Demonstrated in Output

1. **Environment Detection**: Clear identification of sandbox vs production environment
2. **URL Differentiation**: Different base URLs per environment
3. **Rate Limiting**: Different rate limits applied per environment (3/sec for sandbox, 10/sec for production)
4. **Validation Settings**: Coordinate validation enabled for sandbox, disabled for production
5. **API Authentication**: Proper error handling with environment-specific messages
6. **Service Coordination**: All services working with environment-specific configurations
7. **Logging**: Comprehensive logging with environment context included

## ✅ Files That Should NOT Be Pushed

### Files to Exclude (already in .gitignore):
- `*.pyc` files
- `__pycache__/` directories
- `.env` files
- Configuration files with credentials
- Local data files (`data/` directory contents for sensitive data)
- Log files
- Temporary files

### Configuration Template:
- Create `config/eagleview.yaml.example` as a template with placeholders instead of real credentials
- Include instructions for users to create their own `config/eagleview.yaml` file