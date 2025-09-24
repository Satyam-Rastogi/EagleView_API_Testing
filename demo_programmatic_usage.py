"""
Programmatic API Usage Demo
This script demonstrates how to use the EagleView API Client programmatically.
"""
import os
import json
from datetime import datetime
from src.eagleview.config.base import EagleViewSettings
from src.eagleview.client.base import EagleViewClient
from src.eagleview.services.base.property_data_service import PropertyDataService
from src.eagleview.services.base.imagery_service import ImageryService
from src.eagleview.services.base.image_download_service import ImageDownloadService

def demo_programmatic_usage():
    print("EAGLEVIEW API CLIENT - PROGRAMMATIC USAGE DEMO")
    print("=" * 60)
    print("Demo started at: {}".format(datetime.now()))
    print("\nThis demo shows how to use the EagleView API Client programmatically.")
    
    # 1. Load configuration
    print("\n1. Loading configuration...")
    try:
        settings = EagleViewSettings.from_config('config/eagleview.yaml')
        print("   + Configuration loaded: Client ID = {}... (truncated)".format(settings.client_id[:10] if settings.client_id else "None"))
        print("   + Environment: {}".format(settings.environment))
        print("   + Is Sandbox: {}".format(settings.is_sandbox))
        print("   + Rate limits: {}/sec, {}/min".format(settings.requests_per_second, settings.requests_per_minute))
        if not settings.validate():
            print("   ! Warning: Configuration is missing required credentials")
    except Exception as e:
        print("   - Error loading configuration: {}".format(e))
        return
    
    # 2. Create client
    print("\n2. Creating API client...")
    try:
        client = EagleViewClient(settings)
        print("   + Client created successfully")
        print("   + Base URL: {}".format(client.base_url))
        print("   + Imagery Base URL: {}".format(client.imagery_base_url))
    except Exception as e:
        print("   - Error creating client: {}".format(e))
        return
    
    # 3. Property Data Service
    print("\n3. Property Data Service...")
    try:
        property_service = PropertyDataService(client)
        print("   + Property Data Service created")
        
        # Get sample coordinates (these would be used if we had valid credentials)
        coordinates = property_service.get_sandbox_coordinates()
        print("   + Sample coordinates retrieved: {} locations".format(len(coordinates)))
        for i, coord in enumerate(coordinates[:2]):  # Show first 2
            print("     - Location {}: {}, {}".format(i+1, coord['lat'], coord['lon']))
        
    except Exception as e:
        print("   - Error with Property Data Service: {}".format(e))
    
    # 4. Imagery Service
    print("\n4. Imagery Service...")
    try:
        imagery_service = ImageryService(client)
        print("   + Imagery Service created")
        
        # Test imagery request preparation
        test_coords = {"lat": 41.25, "lon": -95.99}
        print("   + Imagery request prepared for coordinates: ({}, {})".format(test_coords['lat'], test_coords['lon']))
        
    except Exception as e:
        print("   - Error with Imagery Service: {}".format(e))
    
    # 5. Image Download Service
    print("\n5. Image Download Service...")
    try:
        download_service = ImageDownloadService(client)
        print("   + Image Download Service created")
        
        # Check if we have any property data results to work with
        import glob
        import os
        data_dir = settings.output_directory
        property_data_pattern = os.path.join(data_dir, "results", "*property_data_result*.json")
        property_data_files = glob.glob(property_data_pattern)
        
        if property_data_files:
            print("   + Found {} property data files for image downloads".format(len(property_data_files)))
            print("   + Example file: {}".format(os.path.basename(property_data_files[0])))
        else:
            print("   ! No property data files found for image downloads")
        
    except Exception as e:
        print("   - Error with Image Download Service: {}".format(e))
    
    # 6. Configuration flexibility
    print("\n6. Configuration Flexibility...")
    print("   + Supports YAML configuration files")
    print("   + Supports environment variables")
    print("   + Supports runtime validation")
    print("   + Supports token persistence")
    
    # 7. Error handling demonstration
    print("\n7. Error Handling & Retry Logic...")
    print("   + Automatic token refresh")
    print("   + Rate limiting with configurable limits")
    print("   + Retry logic with exponential backoff")
    print("   + Comprehensive error logging")
    print("   + Custom exception handling")
    
    # 8. Data management
    print("\n8. Data Management...")
    print("   + Automatic JSON file creation")
    print("   + Organized directory structure")
    print("   + Caching with TTL")
    print("   + File naming with timestamps")
    
    print("\n" + "="*60)
    print("PROGRAMMATIC USAGE DEMO SUMMARY")
    print("=" * 60)
    print("The client provides:")
    print("- Modular service architecture")
    print("- Comprehensive configuration options") 
    print("- Robust error handling and retry logic")
    print("- Data persistence and caching")
    print("- Proper authentication and authorization")
    print("- Rate limiting for API compliance")
    
    if not settings.validate():
        print("\nTIP: To run with actual API functionality, update config/eagleview.yaml")
        print("    with your actual EagleView API credentials.")

def demo_data_structure():
    """Demonstrate the expected data structure"""
    print("\n" + "="*60)
    print("DATA STRUCTURE DEMO")
    print("=" * 60)
    print("The system organizes data in the following structure:")
    print('''
    data/
    |-- cache/                 # Cached API responses
    |   `-- *.json
    |-- imagery/              # Downloaded images
    |   |-- downloaded_images/
    |   |-- address_based_images/
    |   |-- custom_location_images/
    |   `-- *.json (imagery data)
    |-- requests/             # Property data requests
    |   `-- *.json
    |-- results/              # Property data results
    |   `-- *.json
    `-- tokens/               # Authentication tokens
        `-- *.json
    ''')
    
    # Show what's currently in the data directory
    import os
    data_path = "data"
    if os.path.exists(data_path):
        print("Current data directory contents:")
        for root, dirs, files in os.walk(data_path):
            level = root.replace(data_path, '').count(os.sep)
            indent = ' ' * 2 * level
            print("{}{}/".format(indent, os.path.basename(root)))
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                if file.endswith(('.json', '.png', '.jpg', '.jpeg')):
                    print("{}{}".format(subindent, file))

if __name__ == "__main__":
    demo_programmatic_usage()
    demo_data_structure()