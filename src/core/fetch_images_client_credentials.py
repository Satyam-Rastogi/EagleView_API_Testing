"""
Fetch Images using Client Credentials Authentication

This script demonstrates how to fetch images from EagleView API using 
OAuth 2.0 Client Credentials flow which requires no user interaction.

Usage:
1. Update the configuration with your actual client credentials
2. Run the script: python fetch_images_client_credentials.py
"""

import json
import logging
import sys
import os
from datetime import datetime
from typing import List, Dict

# Add parent directory to path to import client_credentials_eagleview
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from client_credentials_eagleview import ClientCredentialsEagleViewClient, EagleViewConfig, EagleViewAPIException

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fetch_images_client_credentials.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def fetch_imagery() -> List[Dict]:
    """Fetch imagery for locations using Client Credentials authentication
    
    Returns:
        List[Dict]: List of downloaded image information
    """
    
    # Initialize configuration with your credentials
    config = EagleViewConfig(
        client_id="0oa16yo11pa57TLPa2p8",
        client_secret="BAfJ05yNlGaNt8Gm3gnO_0ekJ1DRlwJsaNgU4aePS9o5iCuxyOuZL1kmxxHionD7",
        # Conservative rate limits to be respectful
        requests_per_second=3,
        requests_per_minute=50,
        is_sandbox=True  # Set to False for production
    )
    
    try:
        # Create client credentials client
        logger.info("Initializing Client Credentials client...")
        client = ClientCredentialsEagleViewClient(config)
        
        # Test authentication
        logger.info("Testing authentication...")
        # Just test that we can get a token
        token = client._get_access_token()
        logger.info("Authentication successful!")
        
        # Create directory for images
        images_dir = "eagleview_images"
        os.makedirs(images_dir, exist_ok=True)
        logger.info(f"Created directory for images: {images_dir}")
        
        # Define locations within the sandbox area
        # Bounding box: -96.00532698173473, 41.24140396772262, -95.97589954958912, 41.25672882015283
        locations = [
            {"lat": 41.25, "lon": -95.99, "name": "Location 1"},
            {"lat": 41.245, "lon": -95.98, "name": "Location 2"},
            {"lat": 41.255, "lon": -96.0, "name": "Location 3"}
        ]
        
        # Track imagery data
        imagery_data = []
        
        # Process locations
        for i, location in enumerate(locations):
            lat, lon, name = location["lat"], location["lon"], location["name"]
            logger.info(f"Processing {name} ({i+1}/{len(locations)}) at coordinates ({lat}, {lon})")
            
            try:
                # Request imagery for the location
                imagery_request = {
                    "center": {
                        "point": {
                            "geojson": {
                                "value": json.dumps({
                                    "type": "Feature",
                                    "geometry": {
                                        "type": "Point",
                                        "coordinates": [lon, lat]  # Note: GeoJSON uses [lon, lat]
                                    },
                                    "properties": None
                                }),
                                "epsg": "EPSG:4326"
                            }
                        },
                        "radius_in_meters": 50
                    }
                }
                
                imagery_response = client.get_imagery_for_location(imagery_request)
                
                if imagery_response and 'captures' in imagery_response:
                    capture_count = len(imagery_response['captures'])
                    logger.info(f"  Found {capture_count} captures for {name}")
                    
                    # Save imagery data
                    imagery_data.append({
                        'location_name': name,
                        'coordinates': {'lat': lat, 'lon': lon},
                        'captures': capture_count,
                        'response': imagery_response
                    })
                else:
                    logger.info(f"  No imagery captures found for {name}")
                    
            except EagleViewAPIException as e:
                logger.warning(f"  Failed to get imagery for {name}: {e}")
            except Exception as e:
                logger.warning(f"  Unexpected error processing {name}: {e}")
            
            # Add a small delay to be respectful
            import time
            time.sleep(0.5)
        
        # Save imagery summary to JSON
        if imagery_data:
            summary_filename = f"eagleview_imagery_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(summary_filename, 'w') as f:
                json.dump(imagery_data, f, indent=2, default=str)
            logger.info(f"Imagery summary saved to: {summary_filename}")
        
        return imagery_data
        
    except EagleViewAPIException as e:
        logger.error(f"API Error: {e}")
        if hasattr(e, 'status_code'):
            logger.error(f"  Status Code: {e.status_code}")
        if hasattr(e, 'response') and e.response:
            logger.error(f"  Response: {json.dumps(e.response, indent=2)}")
        return []
        
    except Exception as e:
        logger.error(f"Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        return []

def display_imagery_summary(imagery_data: List[Dict]) -> None:
    """Display a formatted summary of imagery data
    
    Args:
        imagery_data (List[Dict]): List of imagery data information
    """
    if not imagery_data:
        print("No imagery data found")
        return
        
    print("\n" + "="*80)
    print("IMAGERY SUMMARY")
    print("="*80)
    
    # Headers
    print(f"{'Location':<20} {'Coordinates':<25} {'Captures':<10}")
    print("-"*80)
    
    # Display imagery data
    for data in imagery_data:
        name = data.get('location_name', 'Unknown')[:19]  # Truncate if too long
        coords = f"{data['coordinates']['lat']:.4f}, {data['coordinates']['lon']:.4f}"
        captures = data.get('captures', 0)
        
        print(f"{name:<20} {coords:<25} {captures:<10}")
        
    print("="*80)

def main():
    """Main function"""
    print("EagleView Imagery Fetcher (Client Credentials)")
    print("=" * 60)
    print("NO BROWSER REQUIRED - Fully Automated!")
    print("Using OAuth 2.0 Client Credentials Flow")
    print("Perfect for server-to-server communication")
    print()
    
    # Check if credentials are properly configured
    client_id = "0oa16yo11pa57TLPa2p8"
    client_secret = "BAfJ05yNlGaNt8Gm3gnO_0ekJ1DRlwJsaNgU4aePS9o5iCuxyOuZL1kmxxHionD7"
    
    # Validate credentials
    if not client_id or not client_secret:
        print("❌ Please update the client credentials in the script!")
        print("💡 Look for 'YOUR_CLIENT_ID_HERE' and 'YOUR_CLIENT_SECRET_HERE' in the code")
        return
    
    imagery_data = fetch_imagery()
    
    if imagery_data:
        display_imagery_summary(imagery_data)
        print("\n" + "="*60)
        print("PROCESS COMPLETED SUCCESSFULLY!")
        print(f"Processed {len(imagery_data)} locations")
        print("Imagery data saved to JSON file")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("PROCESS COMPLETED WITH NO IMAGERY DATA")
        print("This might be because:")
        print("   - No imagery captures were found")
        print("   - Check the log file for details")
        print("="*60)

if __name__ == "__main__":
    main()