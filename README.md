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

## Features
- **OAuth 2.0 Client Credentials Authentication**: Secure server-to-server authentication
- **Property Data Access**: Retrieve detailed property information including roof analysis, structure measurements, and environmental factors
- **Imagery Data Access**: Obtain oblique and ortho images for property assessment
- **Report Management**: Fetch and download measurement/order reports
- **Image Downloading**: Download actual property images using image tokens
- **Rate Limiting**: Built-in request throttling to respect API limits
- **Error Handling**: Automatic retry logic with exponential backoff
- **Token Management**: Automatic token refresh and caching

## Prerequisites
- Python 3.12 or higher
- `requests` library
- EagleView API credentials (client ID and secret)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Satyam-Rastogi/EagleView_API_Testing.git
   cd EagleView_API_Testing
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
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

### Accessing Images
To access images:
1. Request property data for a location within the sandbox area
2. Extract image tokens and references from the property data response
3. Use the image tokens to download specific images via the `/property/v2/image/{image_token}` endpoint

## Configuration

Before running the scripts, you need to update the client credentials in each Python file:

1. Open each Python file that makes API requests:
   - `fetch_reports_client_credentials.py`
   - `fetch_images_client_credentials.py`
   - `fetch_and_download_reports.py`
   - `demo_fetch_reports.py`
   - `download_images.py`

2. Find the configuration section and replace the placeholder values:
   ```python
   config = EagleViewConfig(
       client_id="YOUR_CLIENT_ID_HERE",
       client_secret="YOUR_CLIENT_SECRET_HERE",
       # ... other configuration options
   )
   ```

3. Replace `YOUR_CLIENT_ID_HERE` and `YOUR_CLIENT_SECRET_HERE` with your actual EagleView API credentials.

## Usage

### Run the complete demo workflow:
```bash
python fetch_reports_client_credentials.py
python fetch_images_client_credentials.py
python download_images.py
```

### Alternative: Run individual components:
1. Request property data:
   ```bash
   python fetch_reports_client_credentials.py
   ```

2. Request imagery data:
   ```bash
   python fetch_images_client_credentials.py
   ```

3. Fetch and download measurement/order reports:
   ```bash
   python fetch_and_download_reports.py
   ```

4. Demo report information fetching:
   ```bash
   python demo_fetch_reports.py
   ```

5. Download property images:
   ```bash
   python download_images.py
   ```

### View demo information:
```bash
python demo_run.py
python demo_overview.py
```

## Docker Support

You can also run this project using Docker:

1. Build the Docker image:
   ```bash
   docker build -t eagleview-api-client .
   ```

2. Run the demo:
   ```bash
   docker run -it eagleview-api-client
   ```

## Project Structure

### Core Library
- `client_credentials_eagleview.py` - Main client library with authentication and API methods

### Main Programs
- `fetch_reports_client_credentials.py` - Requests property data for locations within the sandbox area
- `fetch_images_client_credentials.py` - Retrieves imagery information for locations within the sandbox area
- `fetch_and_download_reports.py` - Fetches measurement/order reports and downloads associated files
- `demo_fetch_reports.py` - Demonstrates report information fetching without downloading
- `download_images.py` - Downloads actual property images using image tokens

### Demo Scripts
- `demo_run.py` - Demo execution script
- `demo_overview.py` - Demo overview script

### Utility Scripts
- `test_additional_data.py` - Additional location testing
- `test_custom_locations.py` - Custom location testing
- `test_address_requests.py` - Address-based request testing
- `download_all_test_images.py` - Comprehensive image downloading

## Output Files

### JSON Data Files
- Property data requests and results
- Imagery data requests and responses
- Authentication tokens (cached for efficiency)

### Image Directories
- `downloaded_property_images/` - Original demo images
- `custom_location_images/` - Images from custom location tests
- `address_based_images/` - Images from address-based request tests

## API Endpoints

### Property Data V2 API
- **Request Property Data:** `POST /property/v2/request`
- **Get Results:** `GET /property/v2/result/{requestId}`
- **Download Image:** `GET /property/v2/image/{imageToken}`

### Imagery API
- **Get Imagery for Location:** `POST /imagery/v3/discovery/rank/location`

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