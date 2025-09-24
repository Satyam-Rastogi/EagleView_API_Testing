"""
Command-line interface for EagleView API client with multi-environment support.
Provides a unified interface for all client operations across different environments.
"""

import argparse
import sys
import os
import logging
from typing import List
from src.eagleview.config import create_config
from src.eagleview.client import create_client
from src.eagleview.services import PropertyDataService
from src.eagleview.services.base.imagery_service import ImageryService
from src.eagleview.services.base.image_download_service import ImageDownloadService
from src.eagleview.utils.file_ops import setup_logging

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="EagleView API Client")
    parser.add_argument(
        '--operation', 
        choices=['property-data', 'imagery', 'download-images', 'demo'],
        required=True,
        help='Operation to perform'
    )
    parser.add_argument(
        '--environment',
        choices=['sandbox', 'production'],
        default='sandbox',
        help='Environment to use (default: sandbox)'
    )
    parser.add_argument(
        '--coordinates',
        nargs='+',
        help='Coordinates in format "lat,lon" (e.g., "41.25,-95.99")'
    )
    parser.add_argument(
        '--output-dir',
        default='data',
        help='Output directory for files'
    )
    parser.add_argument(
        '--log-level',
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Logging level'
    )
    parser.add_argument(
        '--config',
        help='Path to YAML configuration file'
    )
    parser.add_argument(
        '--property-data-file',
        help='Path to property data JSON file for image download operation'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logging(__name__, args.log_level)
    
    # Load configuration based on environment
    if args.config:
        # Load from config file
        from src.eagleview.config.base import EagleViewSettings
        settings = EagleViewSettings.from_config(args.config)
    else:
        # Create environment-appropriate configuration
        settings = create_config(
            environment=args.environment,
            client_id=os.getenv('EAGLEVIEW_CLIENT_ID'),
            client_secret=os.getenv('EAGLEVIEW_CLIENT_SECRET')
        )
    
    if not settings.validate():
        logger.error("Missing required configuration. Set EAGLEVIEW_CLIENT_ID and EAGLEVIEW_CLIENT_SECRET environment variables or provide a configuration file.")
        sys.exit(1)
    
    # Create client
    client = create_client(settings)
    
    # Process based on operation
    if args.operation == 'property-data':
        service = PropertyDataService(client)
        coordinates = parse_coordinates(args.coordinates) if args.coordinates else service.get_sandbox_coordinates()
        requests_data = service.submit_coordinates_requests(coordinates)
        if requests_data:
            service.save_requests_data(requests_data, args.output_dir)
    elif args.operation == 'imagery':
        service = ImageryService(client)
        # For imagery, we need coordinates or addresses
        coordinates = parse_coordinates(args.coordinates) if args.coordinates else service.get_sandbox_coordinates()
        for i, coord in enumerate(coordinates):
            name = f"location_{i+1}"
            lat = coord["lat"]
            lon = coord["lon"]
            imagery_data = service.request_imagery_for_location(name, lat, lon)
            if imagery_data:
                service.save_imagery_data(imagery_data, name, lat, lon, args.output_dir)
    elif args.operation == 'download-images':
        service = ImageDownloadService(client)
        # For download-images, we need property data results
        property_data_file = args.property_data_file
        
        if not property_data_file:
            # Try to find a property data file
            import glob
            # Look for recent property data files
            data_dir = args.output_dir
            property_data_pattern = os.path.join(data_dir, "results", "*property_data_result*.json")
            property_data_files = glob.glob(property_data_pattern)
            
            if property_data_files:
                # Sort by modification time, newest first
                property_data_files.sort(key=os.path.getmtime, reverse=True)
                property_data_file = property_data_files[0]
                print(f"Using property data file: {property_data_file}")
            else:
                print("No property data files found.")
                print("Please run property-data operation first or provide --property-data-file")
                return
        
        # Load property data
        try:
            import json
            with open(property_data_file, 'r') as f:
                property_data = json.load(f)
            print(f"Loaded property data from: {property_data_file}")
        except Exception as e:
            print(f"Failed to load property data: {e}")
            return
        
        # Download images
        print("Downloading property images...")
        try:
            count = service.download_property_images(property_data, "downloaded_images")
            print(f"Downloaded {count} images successfully!")
            print("Images saved to: data/imagery/downloaded_images/")
        except Exception as e:
            print(f"Failed to download images: {e}")
            import traceback
            traceback.print_exc()
    elif args.operation == 'demo':
        print("EagleView API Client Demo")
        print("=" * 40)
        print(f"Environment: {settings.environment}")
        print(f"Base URL: {settings.base_url}")
        # Run complete workflow
        run_demo(client, args.output_dir, settings)

def parse_coordinates(coord_strings: List[str]) -> List[dict]:
    """Parse coordinate strings into coordinate dictionaries."""
    coordinates = []
    for coord_str in coord_strings:
        try:
            lat, lon = map(float, coord_str.split(','))
            coordinates.append({"lat": lat, "lon": lon})
        except ValueError:
            logging.warning(f"Invalid coordinate format: {coord_str}")
    return coordinates

def run_demo(client, output_dir: str, settings):
    """Run the complete demo workflow."""
    logging.info("Starting demo workflow...")
    
    # 1. Property data requests
    print("1. Submitting property data requests...")
    property_service = PropertyDataService(client)
    coordinates = property_service.get_sandbox_coordinates()
    
    # In production environment, get different coordinates if needed
    if settings.environment == 'production':
        # Use generic coordinates for production (user would need to provide real ones)
        coordinates = [{"lat": 40.7128, "lon": -74.0060}]  # Example: New York City
    
    requests_data = property_service.submit_coordinates_requests(coordinates)
    if requests_data:
        property_service.save_requests_data(requests_data, output_dir)
        print(f"   Submitted {len(requests_data)} property data requests")
    
    # 2. Imagery requests
    print("2. Requesting imagery...")
    imagery_service = ImageryService(client)
    for i, coord in enumerate(coordinates[:1]):  # Just first coordinate for demo
        name = f"demo_location_{i+1}"
        lat = coord["lat"]
        lon = coord["lon"]
        
        # Validate coordinates if needed based on settings
        try:
            imagery_data = imagery_service.request_imagery_for_location(name, lat, lon)
            if imagery_data:
                imagery_service.save_imagery_data(imagery_data, name, lat, lon, output_dir)
                print(f"   Retrieved imagery for {name}")
        except ValueError as e:
            print(f"   Skipped imagery for {name}: {e}")
    
    print("Demo workflow completed!")

if __name__ == "__main__":
    main()