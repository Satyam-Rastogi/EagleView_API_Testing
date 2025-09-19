# EagleView API Client

This project provides a Python client library and example programs for interacting with the EagleView API using OAuth 2.0 Client Credentials authentication.

## Author
Satyam Rastogi

## Prerequisites
- Python 3.12 or higher
- Docker (optional, for containerized deployment)

## Quick Start with Docker

1. Build the Docker image:
   ```bash
   docker build -t eagleview-api-client .
   ```

2. Run the demo:
   ```bash
   docker run -it eagleview-api-client
   ```

## Quick Start without Docker

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd eagleview-api-client
   ```

2. Install dependencies (requires Python 3.12+):
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your EagleView API credentials in the Python files:
   - Replace `YOUR_CLIENT_ID_HERE` and `YOUR_CLIENT_SECRET_HERE` with your actual credentials

4. Run the demo:
   ```bash
   python demo_run.py
   ```

## Project Structure
- `client_credentials_eagleview.py` - Main client library
- `fetch_reports_client_credentials.py` - Property data requests
- `fetch_images_client_credentials.py` - Imagery data requests
- `download_images.py` - Image downloading utility
- `demo_run.py` - Demo execution script
- `demo_overview.py` - Demo overview script

## Usage

### Run the complete demo workflow:
```bash
python fetch_reports_client_credentials.py
python fetch_images_client_credentials.py
python download_images.py
```

### View demo information:
```bash
python demo_run.py
python demo_overview.py
```