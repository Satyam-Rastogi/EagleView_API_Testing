# EagleView API Client Demo

## Overview

This demo showcases a complete working implementation of an EagleView API client using OAuth 2.0 Client Credentials authentication. The client demonstrates how to interact with the EagleView API to request property data, retrieve imagery information, and download actual property images.

## Key Features Demonstrated

1. **OAuth 2.0 Client Credentials Authentication**
   - Automatic token management and refresh
   - Token caching for efficiency
   - Secure credential handling

2. **Property Data API Integration**
   - Request property data for locations within the sandbox area
   - Retrieve detailed property information including:
     - Address details
     - Roof analysis (material, condition, measurements)
     - Structure information
     - Environmental factors
     - Vulnerability assessments

3. **Imagery API Integration**
   - Request imagery data for properties
   - Retrieve information about available images:
     - Oblique images (north, east, south, west views)
     - Ortho (top-down) images
     - Image metadata and URNs

4. **Measurement/Order Reports API Integration**
   - Fetch all customer reports
   - Get detailed report information
   - Retrieve file download links for reports
   - Download actual report files (PDFs, ZIPs, etc.)

5. **Image Downloading**
   - Download actual property images using image tokens
   - Save images in appropriate formats
   - Handle image metadata

## Sandbox Environment

The demo works with the EagleView sandbox environment, which is limited to a specific bounding box in Omaha, Nebraska:

**Coordinates:**
- **Minimum Latitude:**  41.24140396772262
- **Maximum Latitude:**  41.25672882015283
- **Minimum Longitude:** -96.00532698173473
- **Maximum Longitude:** -95.97589954958912

**Sample Coordinates Within Sandbox Area:**
1. Central Location: (41.25, -95.99)
2. Downtown Omaha: (41.248, -95.985)
3. Midtown Omaha: (41.252, -95.995)
4. North Omaha: (41.243, -95.978)
5. South Omaha: (41.255, -96.0)
6. West Omaha: (41.245, -95.98)
7. East Omaha: (41.251, -95.992)

## Demo Files

### Core Implementation
- `client_credentials_eagleview.py` - Main client library with authentication and API methods
- `fetch_reports_client_credentials.py` - Requests property data for locations
- `fetch_images_client_credentials.py` - Retrieves imagery information for locations
- `fetch_and_download_reports.py` - Fetches measurement/order reports and downloads files
- `demo_fetch_reports.py` - Demonstrates report information fetching
- `download_images.py` - Downloads actual property images using image tokens

### Sample Output Files
- `eagleview_property_data_requests_*.json` - Sample property data requests
- `additional_property_data_requests_*.json` - Additional property data requests
- `property_data_result_*.json` - Sample property data results showing rich information
- `eagleview_imagery_summary_*.json` - Sample imagery requests
- `imagery_data_*.json` - Sample imagery data results
- `eagleview_client_credentials_tokens.json` - Sample authentication token file

### Downloaded Content
- `downloaded_property_images/` directory containing actual property images
- `downloaded_reports/` directory containing sample report files (in full implementation)

## Running the Demo

### Prerequisites
- Python 3.6 or higher
- `requests` library (`pip install requests`)

### Configuration
1. Update the client credentials in each Python file:
   ```python
   config = EagleViewConfig(
       client_id="YOUR_CLIENT_ID_HERE",
       client_secret="YOUR_CLIENT_SECRET_HERE",
       # ... other configuration options
   )
   ```

### Execution
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

## Data Content Examples

### Property Data Results
The property data results include comprehensive information:
- Full address: "965 S 50th St, Omaha, NE  68106-1913"
- Roof material: "shingle"
- Roof condition: "good"
- Structure footprint: 1230 square feet
- Eave heights: 8-9 feet
- Wildfire vulnerability rating: 10
- Hail vulnerability rating: Based on roof covering, tree overhang, and roof geometry

### Imagery Data Results
The imagery data results include:
- Capture dates: "2025-03-13" to "2025-03-16"
- Oblique images in all four cardinal directions
- Ortho (top-down) images
- Image URNs for accessing actual image files

### Report Data Results
The measurement/order report data includes:
- Report ID: Unique identifier for each report
- Status: Current processing status (e.g., "Complete", "In Progress")
- Product information: Type of report and delivery format
- Property details: Address, area measurements, roof characteristics
- Timestamps: Date placed, date completed
- Download links: URLs to download PDF reports and other deliverables
- File links: Signed URLs for specific file types with expiration timestamps

### Downloaded Content
- Actual property images in PNG format (1.9-2.9 MB each)
- PDF reports showing property measurements and analysis
- ZIP files containing additional deliverables
- Various file formats depending on report type

## Best Practices Demonstrated

1. **Rate Limiting**: Built-in rate limiting to respect API limits
2. **Error Handling**: Automatic retry logic with exponential backoff
3. **Token Management**: Automatic token refresh and caching
4. **Data Organization**: Timestamped filenames to prevent overwriting
5. **Security**: Secure credential handling

## Next Steps

To use this client with production APIs:
1. Contact EagleView for production credentials and access
2. Update endpoints to use production URLs
3. Modify programs to use additional API endpoints as needed
4. Implement additional error handling for production scenarios

## License

This demo is provided for educational and demonstration purposes. Ensure you have proper authorization and credentials before using with any EagleView APIs.