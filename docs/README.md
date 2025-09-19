# EagleView API Testing Suite

A comprehensive Python testing suite for the EagleView API, demonstrating property data retrieval, imagery access, and report downloading capabilities.

## Author
Satyam Rastogi

## Overview
This repository contains a complete Python client library and example programs for interacting with the EagleView API using OAuth 2.0 Client Credentials authentication. The suite demonstrates:

- Property data requests for locations within the sandbox area
- Imagery data requests for properties
- Measurement/order report fetching and downloading
- Property image downloading
- Rate limiting and error handling

For detailed API documentation, please refer to the [EagleView Developer Portal](https://developer.eagleview.com/).

## What is EagleView?

EagleView is a technology company that provides aerial property imaging and analysis services. Using high-resolution aerial photographs, EagleView creates detailed property reports that include measurements, roof analysis, and other important property characteristics. This information is valuable for insurance companies, roofing contractors, real estate professionals, and city planners.

## What Does This Code Do?

This repository contains a Python-based client that demonstrates how to interact with the EagleView API. The code shows how to:

- Automatically retrieve property data using addresses or coordinates
- Access high-resolution aerial images of properties
- Download detailed property reports
- Handle authentication and rate limiting

Think of it as a bridge between your applications and EagleView's powerful property analysis capabilities. Instead of manually requesting property information through a web interface, this code allows you to programmatically access the same data, making it possible to process many properties automatically.

## What Information Do We Send?

To retrieve property data from EagleView, we need to send specific information:

### 1. Authentication Credentials
Before we can access any data, we need to prove we're authorized to use the API:
- **Client ID**: Like a username that identifies your application
- **Client Secret**: Like a password that authenticates your application

These credentials are obtained by registering on the EagleView Developer Portal.

### 2. Property Location Information
To get information about a specific property, we send either:
- **Coordinates**: Latitude and longitude values (e.g., 41.25, -95.99)
- **Address**: A complete street address (e.g., "123 Main Street, Omaha, NE 68102")

### 3. Request Parameters
We also specify what type of information we want:
- **Property details**: Roof measurements, structure information, environmental factors
- **Images**: Aerial photos from different angles
- **Reports**: Measurement reports and other deliverables

Think of it like filling out a form - we tell EagleView exactly what property we're interested in and what information we want about it.

## Features
- **OAuth 2.0 Client Credentials Authentication**: Secure server-to-server authentication
- **Property Data Access**: Retrieve detailed property information including roof analysis, structure measurements, and environmental factors
- **Imagery Data Access**: Obtain oblique and ortho images for property assessment
- **Report Management**: Fetch and download measurement/order reports
- **Image Downloading**: Download actual property images using image tokens
- **Rate Limiting**: Built-in request throttling to respect API limits
- **Error Handling**: Automatic retry logic with exponential backoff
- **Token Management**: Automatic token refresh and caching

For detailed information about these features and the underlying APIs, please consult the [EagleView Developer Portal](https://developer.eagleview.com/).

## Prerequisites
- Python 3.12 or higher
- `requests` library
- EagleView API credentials (client ID and secret)

> To obtain API credentials, you'll need to register on the [EagleView Developer Portal](https://developer.eagleview.com/).

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Satyam-Rastogi/EagleView_API_Testing.git
   cd EagleView_API_Testing
   ```

2. Install the required dependencies:
   ```bash
   pip install -r scripts/requirements.txt
   ```

## Sandbox Area Information

The EagleView API sandbox environment is limited to a specific geographic area in Omaha, Nebraska. All API requests must use coordinates within this bounding box to work in the sandbox environment.

### Bounding Box Coordinates
- **Minimum Latitude:** 41.24140396772262
- **Maximum Latitude:** 41.25672882015283
- **Minimum Longitude:** -96.00532698173473
- **Maximum Longitude:** -95.97589954958912

### Valid ZIP Codes in Sandbox Area
The sandbox area primarily covers parts of Omaha, Nebraska, including ZIP codes such as:
- 68106
- 68105
- 68104
- 68102
- 68131

### Sample Coordinates Within Sandbox Area
These coordinates are confirmed to work within the sandbox environment:

1. **Central Location**: (41.25, -95.99)
2. **Downtown Omaha**: (41.248, -95.985)
3. **Midtown Omaha**: (41.252, -95.995)
4. **North Omaha**: (41.243, -95.978)
5. **South Omaha**: (41.255, -96.0)
6. **West Omaha**: (41.245, -95.98)
7. **East Omaha**: (41.251, -95.992)

### Important Notes
- API requests outside of this bounding box will fail with permission errors in the sandbox environment
- For production access, contact EagleView support for additional scopes and geographic coverage
- The sandbox environment provides access to a limited but representative dataset for testing purposes

## Image Types and Limitations

### Image Categories
The EagleView API provides two main categories of property images:

1. **Ortho Images (Top-Down Views)**
   - Direct vertical aerial photographs
   - Provide a bird's-eye view of the property
   - Useful for measuring property dimensions and footprint analysis

2. **Oblique Images (Angled Views)**
   - Taken at an angle from four cardinal directions:
     - North-facing views
     - East-facing views
     - South-facing views
     - West-facing views
   - Provide detailed views of building sides, roof structures, and elevations
   - Essential for roof analysis, siding assessment, and 3D modeling

### Image Access Limitations

#### Sandbox Environment Restrictions
- **Geographic Limitation**: Images are only available for properties within the Omaha, Nebraska bounding box
- **Data Set Limitation**: The sandbox contains a limited dataset representing a subset of EagleView's full imagery catalog
- **Temporal Limitation**: Images in the sandbox may not represent the most current available imagery

#### Technical Limitations
- **Authentication Required**: All image downloads require valid OAuth 2.0 Client Credentials
- **Rate Limiting**: Requests are subject to API rate limits (configurable in the client)
- **Token-Based Access**: Individual images require specific image tokens obtained through property data requests
- **Format Limitations**: Images are typically provided in PNG or JPEG formats

#### Image Metadata
Each image comes with metadata including:
- **Shot Date**: When the image was captured
- **View Type**: Whether it's ortho (top-down) or oblique (angled)
- **Cardinal Direction**: For oblique images, the direction the camera was facing
- **Bounding Box**: Geographic coordinates of the image coverage area
- **Masking Information**: Whether the image has privacy or security masking applied

### Image Resolution and Quality
- **High Resolution**: Images are typically high-resolution suitable for detailed analysis
- **Consistent Quality**: All images in the dataset maintain consistent quality standards
- **Multi-Temporal**: Some properties may have imagery from different time periods

## How Images Are Fetched

The image fetching process involves a three-step workflow:

### Step 1: Request Property Data by Coordinates
To get images for a specific location, you must first request property data using latitude and longitude coordinates:

```python
# Example coordinates within Omaha sandbox
lat, lon = 41.25, -95.99

# Request property data
response = client.request_property_data_by_coordinates(lat, lon)
request_id = response['request']['id']
```

This step:
- Takes latitude/longitude coordinates as input
- Submits a request to the `/property/v2/request` endpoint
- Returns a request ID for tracking the processing status

### Step 2: Retrieve Property Data Results
Once the property data processing is complete, retrieve the results which contain image information:

```python
# Get the property data result
result = client.get_property_data_result(request_id)

# Extract image references and tokens
image_references = result['property_images']['image_references']
imagery_data = result['imagery']
```

The result contains:
- **Image References**: List of available image identifiers
- **Imagery Data**: Detailed information for each image including tokens
- **Image Tokens**: Unique identifiers required to download each specific image

### Step 3: Download Images Using Tokens
Use the image tokens to download the actual image files:

```python
# For each image reference
for image_ref in image_references:
    if image_ref in imagery_data:
        image_token = imagery_data[image_ref]['image_token']
        
        # Download the image using the token
        url = f"https://sandbox.apis.eagleview.com/property/v2/image/{image_token}"
        response = requests.get(url, headers=headers)
```

This step:
- Uses the image token in the URL path
- Requires proper authentication headers
- Downloads the actual image file content

### Important Notes About Image Fetching
- **Fixed Image Set**: Each property location has a predetermined set of images (typically 6-64 images)
- **No Arbitrary Requests**: You cannot request additional images beyond what's provided in the property data
- **Token-Based Security**: Each image requires a specific token, preventing unauthorized access
- **Geographic Restriction**: Only locations within the Omaha bounding box return image data

## In Simple Terms: How This Works

Think of this process like ordering photos from a property database:

1. **Request Property Information**: You tell the system "I want information about the property at this address/coordinate"
2. **Receive a List of Available Images**: The system responds with a list of all available photos of that property (like a menu of photos)
3. **Download the Photos**: For each photo you want, you use a special "ticket" (token) to actually download it

This is similar to ordering items from a catalog - you first ask for the catalog (property data), then you see what's available (image list), and finally you purchase what you want (download images).

## Data Flow: What We Send and Receive

Here's a visual representation of the information flow when using this API client:

```
┌─────────────────┐    1. Credentials + Location    ┌──────────────────┐
│   Your          │ ────────────────────────────────→ │   EagleView      │
│   Application   │                                   │   API            │
│                 │ ←──────────────────────────────── │                  │
└─────────────────┘    2. Property Data + Image List  └──────────────────┘
                                                       │
                                                       │ 3. Image Tokens
                                                       ↓
┌─────────────────┐                                   ┌──────────────────┐
│   Downloaded    │ ←──────────────────────────────── │   Image Files    │
│   Images        │    4. Actual Image Downloads     │   (PNG/JPEG)     │
└─────────────────┘                                   └──────────────────┘
```

**Step-by-step breakdown:**

1. **What We Send**: 
   - Client ID and Secret (for authentication)
   - Property coordinates or address (to identify what we want)

2. **What We Receive**:
   - Property details (measurements, roof info, etc.)
   - List of available images with unique tokens

3. **What We Send (again)**:
   - Image tokens (to request specific images)

4. **What We Receive**:
   - Actual image files that can be saved locally

## Configuration

Before running the scripts, you need to update the client credentials in each Python file:

1. Open each Python file that makes API requests:
   - `src/core/fetch_reports_client_credentials.py`
   - `src/core/fetch_images_client_credentials.py`
   - `src/core/fetch_and_download_reports.py`
   - `src/demos/demo_fetch_reports.py`
   - `src/core/download_images.py`

2. Find the configuration section and replace the placeholder values:
   ```python
   config = EagleViewConfig(
       client_id="YOUR_CLIENT_ID_HERE",
       client_secret="YOUR_CLIENT_SECRET_HERE",
       # ... other configuration options
   )
   ```

3. Replace `YOUR_CLIENT_ID_HERE` and `YOUR_CLIENT_SECRET_HERE` with your actual EagleView API credentials.

> ⚠️ **Important Note About Credentials**: 
> Currently, the client credentials are hardcoded in the source files for testing purposes only. In a production environment, you should NEVER hardcode sensitive credentials in source code. We plan to migrate to using environment variables (via a `.env` file) in a future update to improve security. Always protect your API credentials and avoid committing them to version control systems.

## Usage

### Run the complete demo workflow:
```bash
python src/core/fetch_reports_client_credentials.py
python src/core/fetch_images_client_credentials.py
python src/core/download_images.py
```

### Alternative: Run individual components:
1. Request property data:
   ```bash
   python src/core/fetch_reports_client_credentials.py
   ```

2. Request imagery data:
   ```bash
   python src/core/fetch_images_client_credentials.py
   ```

3. Fetch and download measurement/order reports:
   ```bash
   python src/core/fetch_and_download_reports.py
   ```

4. Demo report information fetching:
   ```bash
   python src/demos/demo_fetch_reports.py
   ```

5. Download property images:
   ```bash
   python src/core/download_images.py
   ```

### Quick Win: See Results Fast

To quickly see what this code can do, try running this simple example:

1. Make sure you've updated your credentials in `src/core/fetch_reports_client_credentials.py`
2. Run this command:
   ```bash
   python src/core/fetch_reports_client_credentials.py
   ```
3. This will:
   - Request property data for sample locations in Omaha
   - Save the results as JSON files in the current directory
   - Download actual property images to the `downloaded_property_images` folder

Within a few minutes, you'll have real property data and images that demonstrate the capabilities of the EagleView API!

### View demo information:
```bash
python src/demos/demo_run.py
python src/demos/demo_overview.py
```

## Docker Support

You can also run this project using Docker:

1. Build the Docker image:
   ```bash
   docker build -f scripts/Dockerfile -t eagleview-api-client .
   ```

2. Run the demo:
   ```bash
   docker run -it eagleview-api-client
   ```

## Project Structure

### Core Library (`src/core/`)
- `client_credentials_eagleview.py` - Main client library with authentication and API methods
- `fetch_reports_client_credentials.py` - Requests property data for locations within the sandbox area
- `fetch_images_client_credentials.py` - Retrieves imagery information for locations within the sandbox area
- `fetch_and_download_reports.py` - Fetches measurement/order reports and downloads associated files
- `download_images.py` - Downloads actual property images using image tokens

### Demo Scripts (`src/demos/`)
- `demo_fetch_reports.py` - Demonstrates report information fetching without downloading
- `demo_run.py` - Demo execution script
- `demo_overview.py` - Demo overview script

### Test Scripts (`src/tests/`)
- `test_additional_data.py` - Additional location testing
- `test_custom_locations.py` - Custom location testing
- `test_address_requests.py` - Address-based request testing

### Utility Scripts (`src/utils/`)
- `download_address_images.py` - Address-based image downloading
- `download_all_test_images.py` - Comprehensive image downloading
- `demo_info.bat` - Batch script for demo information

### Data Files (`data/`)
- `requests/` - API request data files
- `results/` - API result data files
- `imagery/` - Imagery data files
- `tokens/` - Authentication tokens

### Images (`images/`)
- `samples/` - Sample images included in the repository
- `downloaded/` - Downloaded images from API requests
- `processed/` - Processed images (if any)

### Documentation (`docs/`)
- `api/` - API documentation
- `guides/` - User guides
- `technical/` - Technical documentation
- Main documentation files (README.md, etc.)

### Configuration (`config/`)
- Configuration files for the application

### Scripts (`scripts/`)
- `Dockerfile` - Docker configuration
- `Makefile` - Makefile for building
- `setup.py` - Setup script
- `requirements.txt` - Python dependencies
- `pyproject.toml` - Project configuration

### Outputs (`outputs/`)
- Log files
- Compiled Python files
- Package information

## Output Files

### JSON Data Files (`data/`)
- Property data requests and results (`data/requests/` and `data/results/`)
- Imagery data requests and responses (`data/imagery/`)
- Authentication tokens (cached for efficiency in `data/tokens/`)

### Image Directories (`images/`)
- `samples/` - Sample images included in the repository
- `downloaded/` - Images downloaded from API requests (in subdirectories)
- `processed/` - Processed images (if any)

### Sample Images
The repository now includes sample images in the `images/samples/` directory to demonstrate the types of property imagery available through the EagleView API. These images include:

- **Ortho Images**: Top-down aerial views showing property footprints
- **Oblique Images**: Angled views from cardinal directions (North, East, South, West) showing building sides and roof structures

These sample images were generated using the sandbox API and represent typical property imagery available through EagleView's services.

## API Endpoints

### Property Data V2 API
- **Request Property Data:** `POST /property/v2/request`
- **Get Results:** `GET /property/v2/result/{requestId}`
- **Download Image:** `GET /property/v2/image/{imageToken}`

### Imagery API
- **Get Imagery for Location:** `POST /imagery/v3/discovery/rank/location`

> Note: The EagleView Imagery API primarily uses POST requests for querying imagery data. Image downloads themselves use GET requests with tokens as described in the Property Data V2 API section.

## Data Content

### Property Data Results
- Address information (full address, street, city, state, ZIP code)
- Geocoordinates (latitude/longitude)
- Roof analysis (material, condition, area, pitch)
- Structure details (footprint, eave heights, centroid)
- Environmental factors (tree overhang, vegetation coverage)
- Vulnerability ratings (wildfire, hail)
- Additional features (pool, fence, driveway, lawn condition)

### Imagery Data
- Capture information (dates, URNs)
- Oblique images (north, east, south, west directions)
- Ortho (top-down) images
- Image URNs for accessing actual image files

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This client is designed for use with the EagleView API sandbox environment. Ensure you have proper authorization and credentials before using with production APIs.

> ⚠️ **Security Note**: 
> This repository currently contains hardcoded client credentials for testing purposes. These should be replaced with your own credentials, and in production environments, you should use environment variables or other secure methods to manage sensitive information. Never commit real API credentials to version control systems.