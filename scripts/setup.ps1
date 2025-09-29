# EagleView API Client Setup Script for PowerShell

Write-Host "========================================" -ForegroundColor Green
Write-Host "EagleView API Client Setup" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# Check if Python is installed
try {
    $pythonVersion = python --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Python not found"
    }
    Write-Host "Found $pythonVersion" -ForegroundColor Yellow
} catch {
    Write-Host "ERROR: Python 3.12 is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.12 from https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Check if pip is available
try {
    $pipVersion = python -m pip --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "pip not found"
    }
} catch {
    Write-Host "ERROR: pip is not available" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv eagleview_env
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to create virtual environment" -ForegroundColor Red
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
$env:VIRTUAL_ENV = "$(Get-Location)\eagleview_env"
$env:PATH = "$env:VIRTUAL_ENV\Scripts;$env:PATH"
$env:PYTHONHOME = $null

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to upgrade pip" -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r scripts/requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Install development dependencies (optional)
Write-Host ""
Write-Host "Do you want to install development dependencies? (y/n)" -ForegroundColor Cyan
$devDeps = Read-Host
if ($devDeps -eq "y" -or $devDeps -eq "Y") {
    Write-Host "Installing development dependencies..." -ForegroundColor Yellow
    pip install -r scripts/requirements-dev.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "WARNING: Failed to install development dependencies" -ForegroundColor Yellow
    }
}

# Create data directories
Write-Host "Creating data directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path "data" -Force | Out-Null
New-Item -ItemType Directory -Path "data\cache" -Force | Out-Null
New-Item -ItemType Directory -Path "data\imagery" -Force | Out-Null
New-Item -ItemType Directory -Path "data\requests" -Force | Out-Null
New-Item -ItemType Directory -Path "data\reports" -Force | Out-Null
New-Item -ItemType Directory -Path "data\results" -Force | Out-Null

# Create sample config file if it doesn't exist
if (-not (Test-Path "config\eagleview.yaml")) {
    Write-Host "Creating sample configuration file..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path "config" -Force | Out-Null
    
    Set-Content -Path "config\eagleview.yaml" -Value @"
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
"@
}

# Create .env file if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "Creating sample .env file..." -ForegroundColor Yellow
    
    Set-Content -Path ".env" -Value @"
# EagleView API Client Environment Variables
EAGLEVIEW_CLIENT_ID=your_client_id_here
EAGLEVIEW_CLIENT_SECRET=your_client_secret_here
EAGLEVIEW_REQUESTS_PER_SECOND=3
EAGLEVIEW_REQUESTS_PER_MINUTE=50
EAGLEVIEW_IS_SANDBOX=true
EAGLEVIEW_OUTPUT_DIR=data
EAGLEVIEW_LOG_LEVEL=INFO
"@
}

Write-Host ""
Write-Host "Setup completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "To use the EagleView API client:" -ForegroundColor Cyan
Write-Host "1. Activate the virtual environment: .\eagleview_env\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "2. Set your API credentials in .env or config\eagleview.yaml" -ForegroundColor White
Write-Host "3. Run the CLI: python -m cli.eagleview --help" -ForegroundColor White
Write-Host ""
Write-Host "For Docker usage:" -ForegroundColor Cyan
Write-Host "1. Build image: docker build -t eagleview-client ." -ForegroundColor White
Write-Host "2. Run container: docker run -it eagleview-client" -ForegroundColor White
Write-Host ""