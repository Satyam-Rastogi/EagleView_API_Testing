# EagleView API Client

A Python client library and example programs for interacting with the EagleView API using OAuth 2.0 Client Credentials authentication.

## Author
Satyam Rastogi

## Features
- OAuth 2.0 Client Credentials authentication
- Property data requests for locations within the sandbox area
- Imagery data requests for properties
- Downloading actual property images
- Rate limiting and error handling

## Prerequisites
- Python 3.12 or higher
- `requests` library

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd eagleview-api-client
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Or install directly with pip:
   ```bash
   pip install requests
   ```

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

## Output Files

### JSON Data Files
- Property data requests and results
- Imagery data requests and responses
- Authentication tokens (cached for efficiency)

### Image Files
- Property images downloaded using image tokens
- Stored in the `downloaded_property_images` directory

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This client is designed for use with the EagleView API sandbox environment. Ensure you have proper authorization and credentials before using with production APIs.