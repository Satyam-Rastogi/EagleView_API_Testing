#!/bin/bash

# EagleView API Client Setup Script for Unix/Linux/macOS

echo "========================================"
echo "EagleView API Client Setup"
echo "========================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3.12 is not installed or not in PATH"
    echo "Please install Python 3.12 from https://www.python.org/downloads/"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "Found Python $PYTHON_VERSION"

# Check if pip is available
if ! python3 -m pip --version &> /dev/null; then
    echo "ERROR: pip is not available"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv eagleview_env
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source eagleview_env/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi

# Upgrade pip
echo "Upgrading pip..."
python3 -m pip install --upgrade pip
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to upgrade pip"
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r scripts/requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

# Install development dependencies (optional)
echo ""
echo "Do you want to install development dependencies? (y/n)"
read -r DEV_DEPS
if [[ $DEV_DEPS == "y" || $DEV_DEPS == "Y" ]]; then
    echo "Installing development dependencies..."
    pip install -r scripts/requirements-dev.txt
    if [ $? -ne 0 ]; then
        echo "WARNING: Failed to install development dependencies"
    fi
fi

# Create data directories
echo "Creating data directories..."
mkdir -p data/cache data/imagery data/requests data/reports data/results

# Create sample config file if it doesn't exist
if [ ! -f config/eagleview.yaml ]; then
    echo "Creating sample configuration file..."
    mkdir -p config
    cat > config/eagleview.yaml << EOF
# EagleView API Client Configuration

eagleview:
  # API Credentials (required)
  client_id: "your_client_id_here"
  client_secret: "your_client_secret_here"
  
  # Rate limiting settings
  requests_per_second: 3.0
  requests_per_minute: 50
  
  # Environment settings
  is_sandbox: true
  
  # Output directory for files
  output_directory: "data"
  
  # Logging level
  log_level: "INFO"
EOF
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating sample .env file..."
    cat > .env << EOF
# EagleView API Client Environment Variables
EAGLEVIEW_CLIENT_ID=your_client_id_here
EAGLEVIEW_CLIENT_SECRET=your_client_secret_here
EAGLEVIEW_REQUESTS_PER_SECOND=3
EAGLEVIEW_REQUESTS_PER_MINUTE=50
EAGLEVIEW_IS_SANDBOX=true
EAGLEVIEW_OUTPUT_DIR=data
EAGLEVIEW_LOG_LEVEL=INFO
EOF
fi

echo ""
echo "Setup completed successfully!"
echo ""
echo "To use the EagleView API client:"
echo "1. Activate the virtual environment: source eagleview_env/bin/activate"
echo "2. Set your API credentials in .env or config/eagleview.yaml"
echo "3. Run the CLI: python -m cli.eagleview --help"
echo ""
echo "For Docker usage:"
echo "1. Build image: docker build -t eagleview-client ."
echo "2. Run container: docker run -it eagleview-client"
echo ""