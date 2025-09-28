# EagleView API Client

A modern, modular Python client library for interacting with the EagleView API.

## Overview

This project provides a comprehensive Python client for the EagleView API, enabling automated access to property data, imagery, and reports. After extensive refactoring and improvements, it now features:

- **Modular Architecture**: Clean separation of concerns with service-based design
- **Enhanced Error Handling**: Robust error management with retry logic and detailed logging
- **Flexible Configuration**: Support for both environment variables and YAML configuration files
- **Command-Line Interface**: Unified CLI for all common operations
- **Data Caching**: Performance optimization through intelligent caching
- **Standardized Structure**: Organized data directory layout

## Features

- **OAuth 2.0 Client Credentials Flow**: Server-to-server authentication without user interaction
- **Rate Limiting**: Automatic rate limiting to respect API quotas
- **Token Management**: Automatic token refresh and persistence
- **Retry Logic**: Exponential backoff for failed requests
- **Modular Design**: Clean separation of concerns with service classes
- **Configuration Flexibility**: Support for both environment variables and YAML configuration files
- **Comprehensive Error Handling**: Custom exceptions with detailed error information
- **Data Persistence**: Automatic saving of results to JSON and CSV files
- **Image Download**: Support for downloading property images
- **CLI Interface**: Command-line interface for common operations
- **Data Caching**: Caching mechanisms to reduce API calls
- **Input Validation**: Comprehensive validation of inputs and responses
- **Standardized Data Structure**: Organized directory layout for all data types
- **Cross-Platform Setup**: Windows batch, Unix shell, PowerShell, and Docker support
- **Containerization**: Docker and Docker Compose support for easy deployment
- **Development Tools**: Makefile support for Unix-like systems

## Installation

### Quick Setup (Recommended)

#### Windows Users
Double-click `scripts/setup.bat` or run in command prompt:
```bash
cd scripts
setup.bat
```

#### Unix/Linux/macOS Users
Run the setup script:
```bash
cd scripts
chmod +x setup.sh
./setup.sh
```

#### PowerShell Users (Windows)
Run the PowerShell setup script:
```powershell
cd scripts
.\setup.ps1
```

### Manual Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd eagleview-api-client
   ```

2. Create virtual environment:
   ```bash
   python -m venv eagleview_env
   ```

3. Activate virtual environment:
   - Windows: `eagleview_env\Scripts\activate.bat`
   - Unix/Linux/macOS: `source eagleview_env/bin/activate`

4. Install dependencies:
   ```bash
   pip install -r scripts/requirements.txt
   ```

5. Create data directories:
   ```bash
   mkdir -p data/cache data/imagery data/property_requests data/property_reports data/property_results
   ```

## Docker Support

### Using Docker

1. Build the Docker image:
   ```bash
   docker build -t eagleview-client .
   ```

2. Run the client:
   ```bash
   docker run -it eagleview-client
   ```

### Using Docker Compose

1. Build and run with docker-compose:
   ```bash
   docker-compose up
   ```

2. Run specific services:
   ```bash
   # Run demo
   docker-compose run eagleview-demo
   
   # Run development shell
   docker-compose run eagleview-dev
   ```

### Docker with Persistent Data

Mount volumes to persist data between container runs:
```bash
docker run -it \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/.env:/app/.env \
  --env-file .env \
  eagleview-client
```

## Makefile Support (Unix/Linux/macOS)

For Unix-like systems, use the provided Makefile:

```bash
# Setup environment
make setup

# Run demo
make run-demo

# Run property data requests
make run-property

# Run imagery requests
make run-imagery

# Build Docker image
make docker-build

# Run in Docker
make docker-run
```

For detailed setup instructions, cross-platform installation guides, and troubleshooting tips, see `docs/SETUP_GUIDE.md`.

## Testing the Project

After setting up the project, you can test all functionalities using the CLI. Here are the commands for each operation:

### 1. Property Data Requests
Submit property data requests using coordinates:

**Real example:**
```bash
python -m cli.eagleview --operation property-data --environment sandbox --config config/eagleview_sandbox.yaml
```

**With custom coordinates:**
```bash
python -m cli.eagleview --operation property-data --coordinates "41.25,-95.99" "41.245,-95.98" --config config/eagleview.yaml
```

**Output:** Saves request files to `data/` directory (e.g., `eagleview_property_data_requests_YYYYMMDD_HHMMSS.json`)

### 2. Property Results Fetching  
Fetch completed property data results:

**Real example:**
```bash
python -m cli.eagleview --operation property-results --environment sandbox --config config/eagleview_sandbox.yaml
```

**Output:** Saves results to `data/property_results/` directory (e.g., `property_data_result_[request_id].json`)

### 3. Imagery Requests
Request imagery for specific locations:

**Real example:**
```bash
python -m cli.eagleview --operation imagery --environment sandbox --config config/eagleview_sandbox.yaml
```

**With custom coordinates:**
```bash
python -m cli.eagleview --operation imagery --coordinates "41.25,-95.99" --output-dir data/imagery
```

**Output:** Saves imagery data to `data/imagery/` directory (e.g., `imagery_data_location_1_41.25_-95.99.json`)

### 4. Download Property Images
Download images using property data results:

**Real example:**
```bash
python -m cli.eagleview --operation download-images --environment sandbox --config config/eagleview_sandbox.yaml
```

**With specific property data file:**
```bash
python -m cli.eagleview --operation download-images --property-data-file data/property_results/property_data_result_62aa5e23-0586-4fa6-8872-2335636ada3d.json
```

**Output:** Downloads images to `data/imagery/downloaded_images/` directory (e.g., `image_1_6c4e7705.png`)

### 5. Download Property Reports
Download EagleView property reports (requires ordered reports):

**Real example:**
```bash
python -m cli.eagleview --operation download-reports --environment sandbox --config config/eagleview_sandbox.yaml
```

**Output:** Saves reports to `data/property_reports/` directory

### 6. Complete Demo
Run the complete workflow demonstration:

**Real example:**
```bash
python -m cli.eagleview --operation demo --environment sandbox --config config/eagleview_sandbox.yaml
```

**Output:** Runs property data and imagery requests, saving to appropriate directories

### 7. Using Different Configuration Sources

**Environment variables:**
```bash
# Set environment variables first
export EAGLEVIEW_CLIENT_ID="your_client_id"
export EAGLEVIEW_CLIENT_SECRET="your_client_secret"
python -m cli.eagleview --operation property-data --environment sandbox
```

**Specific YAML configuration:**
```bash
python -m cli.eagleview --operation property-data --config config/eagleview_sandbox.yaml
```

### 8. Custom Output Directories
Specify custom output directories:

```bash
python -m cli.eagleview --operation property-data --output-dir custom_output_dir
```

### 9. Check Available Options
Get help with all available options:

```bash
python -m cli.eagleview --help
```

## Complete Testing Workflow

To test the full functionality end-to-end:

1. **Submit Property Data Requests:**
   ```bash
   python -m cli.eagleview --operation property-data --environment sandbox --config config/eagleview_sandbox.yaml
   ```
   Output: Saves request files to `data/property_requests/` directory

2. **Wait for Processing, Then Fetch Results:**  
   ```bash
   python -m cli.eagleview --operation property-results --environment sandbox --config config/eagleview_sandbox.yaml
   ```
   Output: Saves result files to `data/property_results/` directory

3. **Download Property Images Using Results:**
   ```bash
   python -m cli.eagleview --operation download-images --environment sandbox --config config/eagleview_sandbox.yaml
   ```
   Output: Downloads images to `data/imagery/downloaded_images/` directory

The project is successfully tested when you can run all operations without errors and see the appropriate output files saved to the correct directories in the `data/` folder:
- Property requests: `data/property_requests/`
- Property results: `data/property_results/`
- Imagery data: `data/imagery/`
- Downloaded images: `data/imagery/downloaded_images/`
- Property reports: `data/property_reports/`
- Cache files: `data/cache/`

## Configuration

### Environment Variables

Set the following environment variables:

```bash
export EAGLEVIEW_CLIENT_ID="your_client_id"
export EAGLEVIEW_CLIENT_SECRET="your_client_secret"
export EAGLEVIEW_REQUESTS_PER_SECOND=3
export EAGLEVIEW_REQUESTS_PER_MINUTE=50
export EAGLEVIEW_IS_SANDBOX=true
export EAGLEVIEW_OUTPUT_DIR="data"
export EAGLEVIEW_LOG_LEVEL="INFO"
```

### YAML Configuration

Alternatively, create a `config/eagleview.yaml` file:

```yaml
eagleview:
  client_id: "your_client_id"
  client_secret: "your_client_secret"
  requests_per_second: 3.0
  requests_per_minute: 50
  is_sandbox: true
  output_directory: "data"
  log_level: "INFO"
```

## Usage

### Command-Line Interface

```bash
# Submit property data requests
python -m cli.eagleview --operation property-data

# Fetch property data results 
python -m cli.eagleview --operation property-results

# Request imagery
python -m cli.eagleview --operation imagery

# Download property images
python -m cli.eagleview --operation download-images

# Run demo workflow
python -m cli.eagleview --operation demo

# With custom configuration file
python -m cli.eagleview --operation property-data --config config/eagleview.yaml

# With custom coordinates
python -m cli.eagleview --operation property-data --coordinates "41.25,-95.99" "41.245,-95.98"

# Download images with specific property data file
python -m cli.eagleview --operation download-images --property-data-file data/property_results/property_data_result_01781285-3526-47a3-a6b9-243e571c5ee5.json

# Complete workflow example:
# 1. Submit property data requests
python -m cli.eagleview --operation property-data
# 2. Fetch the results once processing is complete
python -m cli.eagleview --operation property-results
# 3. Download images using the property data results
python -m cli.eagleview --operation download-images

# With custom configuration file
python -m cli.eagleview --operation property-data --config config/eagleview.yaml

# With custom coordinates
python -m cli.eagleview --operation property-data --coordinates "41.25,-95.99" "41.245,-95.98"

# Download images with specific property data file
python -m cli.eagleview --operation download-images --property-data-file data/property_results/property_data_result_01781285-3526-47a3-a6b9-243e571c5ee5.json
```

### Programmatic Usage

```python
from src.eagleview.config.base import EagleViewSettings
from src.eagleview.client.base import EagleViewClient
from src.eagleview.services.base.property_data_service import PropertyDataService
from src.eagleview.services.base.imagery_service import ImageryService
from src.eagleview.services.base.image_download_service import ImageDownloadService

# Load configuration
settings = EagleViewSettings.from_environment()
# or
settings = EagleViewSettings.from_config('config/eagleview.yaml')

# Validate configuration
if not settings.validate():
    raise ValueError("Invalid configuration")

# Create client
client = EagleViewClient(settings)

# Use services
property_service = PropertyDataService(client)
imagery_service = ImageryService(client)
download_service = ImageDownloadService(client)

# Submit property data requests
coordinates = property_service.get_sandbox_coordinates()
requests_data = property_service.submit_coordinates_requests(coordinates)
if requests_data:
    property_service.save_requests_data(requests_data)

# After retrieving full property data results with image tokens:
# count = download_service.download_property_images(property_data_results, "downloaded_images")
```

## Project Structure

```
eagleview-api-client/
├── cli/                    # Command-line interface
│   └── eagleview.py        # Main CLI entry point
├── config/                 # Configuration files
│   └── eagleview.yaml      # Sample YAML configuration
├── data/                   # Output data directory
│   ├── cache/              # Cached API responses
│   ├── imagery/            # Downloaded images
│   ├── property_requests/  # Property data requests
│   ├── property_reports/   # Customer reports
│   └── property_results/   # Property data results
├── scripts/                # Build/deployment scripts
├── src/                    # Source code
│   └── eagleview/          # Main EagleView API package
│       ├── client/         # API client implementation
│       │   └── base.py     # Main API client
│       ├── config/         # Configuration management
│       │   └── base.py     # Configuration classes
│       ├── core/           # Core modules and utilities
│       │   ├── configuration.py # Configuration management
│       │   ├── client.py        # Core client functionality
│       │   └── ...              # Other core modules
│       ├── services/       # Service modules
│       │   └── base/       # Base service implementations
│       │       ├── image_download_service.py
│       │       ├── imagery_service.py
│       │       └── property_data_service.py
│       └── utils/          # Utility modules
│           ├── file_ops.py # File operations
│           ├── cache.py    # Caching utilities
│           └── ...         # Other utilities
├── docker-compose.yml      # Docker orchestration
├── Dockerfile              # Container definition
├── Makefile                # Build automation
├── pyproject.toml          # Python project configuration
├── README.md               # This file
└── scripts/                # Build/deployment scripts
    ├── setup.bat           # Windows setup script
    ├── setup.ps1           # PowerShell setup script
    └── setup.sh            # Unix/Linux/macOS setup script
```

## API Operations

### Property Data Requests

Submit property data requests using coordinates or addresses within the sandbox area.

### Complete Property Data Workflow

The complete workflow for property data retrieval involves three steps:

1. **Submit Property Data Requests** - Submit requests for properties using coordinates:
   ```bash
   # Submit requests (saves request IDs to data/property_requests/)
   python -m cli.eagleview --operation property-data
   ```

2. **Fetch Property Data Results** - Retrieve the actual property data using request IDs:
   ```bash
   # Fetch results (saves to data/property_results/)
   python -m cli.eagleview --operation property-results
   ```

3. **Download Property Images** - Use the property data to download images:
   ```bash
   # Download images using the retrieved property data
   python -m cli.eagleview --operation download-images
   ```

Alternatively, you can specify property data files directly for image download:
```bash
# Download images with specific property data file
python -m cli.eagleview --operation download-images --property-data-file data/property_results/property_data_result_[request_id].json
```

### Report Downloads

EagleView offers two distinct types of data access:

1. **Property Data API** - Lightweight property insights and imagery access (what we've implemented above)
2. **Measurement Order API** - Full reports with pricing, ordering, and file downloading capabilities

To download complete EagleView reports (PDFs, data exports, etc.):
```bash
# Download reports using the Measurement Order API
python -m cli.eagleview --operation download-reports
```

**Note:** Report downloads require ordering reports first through the Measurement Order API, 
which is not implemented in this demo. The Property Data API provides lightweight property 
insights and image access, while the Measurement Order API enables full report ordering 
and download workflows.



### Imagery Requests

Request imagery for specific locations with customizable parameters.

### Report Management

Retrieve customer reports and detailed report information.

### Image Download

Download property images using image tokens from property data results.

The image download service provides:
- **Secure Downloads**: Authenticated API calls with OAuth 2.0 Bearer tokens
- **Retry Logic**: Automatic retry with exponential backoff
- **Organized Storage**: Images saved in `data/imagery/{category}/` directory structure
- **Flexible Categories**: Support for custom organization of downloaded images
- **Content Type Detection**: Automatic PNG/JPEG format detection
- **Error Handling**: Comprehensive exception handling with detailed logging

Images are saved with the naming convention: `image_reference_token_prefix.extension`

For detailed implementation information, see `docs/IMAGE_DOWNLOAD_SERVICE.md`.

### Basic Usage
```bash
# Download images using auto-detected property data files
python -m cli.eagleview --operation download-images

# Download images with specific property data file
python -m cli.eagleview --operation download-images --property-data-file data/property_results/my_property_data.json
```

### Advanced Usage
```bash
# Download images with custom category
python -m cli.eagleview --operation download-images --property-data-file data/property_results/property_data.json
```

For detailed information about the image download service implementation and usage, see `docs/IMAGE_DOWNLOAD_IMPLEMENTATION_STATUS.md` and `docs/IMAGE_DOWNLOAD_SERVICE.md`.

## Error Handling

The client includes comprehensive error handling with custom exceptions:

- `EagleViewAPIException`: Custom exception for API errors with status codes and response data
- Automatic retry logic with exponential backoff
- Detailed logging for debugging and monitoring
- Input validation to prevent errors

## Rate Limiting

The client automatically handles rate limiting based on configured values:

- Requests per second: Default 3
- Requests per minute: Default 50

These can be adjusted in the configuration.

## Data Persistence

All operations automatically save results to the configured output directory:

- JSON files for structured data
- CSV files for report data
- PNG/JPEG files for downloaded images
- Log files for operation tracking
- Cached responses for improved performance

## Data Directory Structure

The project uses a standardized data directory structure:

- `data/cache/`: Cached API responses
- `data/imagery/`: Downloaded property images
- `data/property_requests/`: Property data requests
- `data/property_reports/`: Customer reports
- `data/property_results/`: Property data results

See `docs/DATA_STRUCTURE.md` for detailed information.

## Caching

The client implements caching to reduce API calls and improve performance:

- Automatic caching of API responses
- Configurable time-to-live (TTL) for cached data
- Cache management utilities

## Recent Improvements

This project has undergone significant refactoring to improve:

1. **Modularity**: Clean separation of concerns with service classes
2. **Reliability**: Robust error handling and retry mechanisms
3. **Usability**: Comprehensive CLI and flexible configuration options
4. **Maintainability**: Extensive documentation and consistent code style
5. **Performance**: Caching and optimized data handling

## Comprehensive Examples

For detailed usage examples and advanced scenarios, see `docs/COMPREHENSIVE_EXAMPLES.md`.

## Setup and Installation Guide

For complete setup instructions, cross-platform installation guides, and troubleshooting tips, see `docs/SETUP_GUIDE.md`.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## Migration from Previous Versions

If you're migrating from an older version of this client, see `docs/MIGRATION_GUIDE.md` for detailed instructions.

## Future Enhancements

For planning documents related to future multi-environment support, see:
- `docs/MULTI_ENVIRONMENT_ARCHITECTURE.md` - Architecture blueprint
- `docs/MIGRATION_TO_MULTI_ENV.md` - Migration guide

## License

This project is proprietary and confidential. All rights reserved.

## CLI Demo Operation

The project includes a comprehensive demo workflow accessible through the CLI that demonstrates all core functionality:

### Running the Demo

Execute the complete demo workflow with:
```bash
python -m cli.eagleview --operation demo --environment sandbox --config config/eagleview_sandbox.yaml
```

This demo performs:
1. Property data requests using sandbox coordinates
2. Imagery requests for location data
3. Results in appropriate files saved to respective directories

### Additional Demo Files (Legacy)

Some legacy demo files may exist in the repository but are no longer maintained:
- `demo_all_prod_functionalities.py`
- `demo_image_download_prod.py`

These older demo files exist for historical purposes but the recommended approach is to use the CLI's built-in demo operation for testing and demonstration.

## Support

For issues and feature requests, please contact the development team.