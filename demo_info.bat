@echo off
echo ========================================
echo EAGLEVIEW API CLIENT DEMO
echo ========================================
echo.
echo This script will demonstrate the EagleView API client functionality.
echo.
echo Files included in this demo:
echo  - Core client library: client_credentials_eagleview.py
echo  - Property data requests: fetch_reports_client_credentials.py
echo  - Imagery data requests: fetch_images_client_credentials.py
echo  - Image downloading: download_images.py
echo  - Sample output files showing API responses
echo  - Downloaded property images
echo.
echo To run the demo programs, use the following commands:
echo.
echo 1. Request property data:
echo    python fetch_reports_client_credentials.py
echo.
echo 2. Request imagery data:
echo    python fetch_images_client_credentials.py
echo.
echo 3. Download property images:
echo    python download_images.py
echo.
echo For detailed information, run:
echo    python demo_overview.py
echo.
echo All programs use OAuth 2.0 Client Credentials authentication
echo and work with the EagleView sandbox environment.
echo.
echo Sandbox Area (Omaha, Nebraska):
echo  Latitude:  41.24140396772262 to 41.25672882015283
echo  Longitude: -96.00532698173473 to -95.97589954958912
echo.
pause