"""
Fetch Full Reports using Client Credentials Authentication

This script demonstrates how to fetch all reports for a customer using 
OAuth 2.0 Client Credentials flow which requires no user interaction.

Usage:
1. Update the configuration with your actual client credentials
2. Run the script: python fetch_reports_client_credentials.py
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
        logging.FileHandler('fetch_reports_client_credentials.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def fetch_property_data_requests() -> List[Dict]:
    """Fetch property data using Client Credentials authentication by submitting requests
    for coordinates within the sandbox area
    
    Returns:
        List[Dict]: List of property data request responses
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
        
        # Define coordinates within the sandbox area
        # Bounding box: -96.00532698173473, 41.24140396772262, -95.97589954958912, 41.25672882015283
        coordinates = [
            {"lat": 41.25, "lon": -95.99},
            {"lat": 41.245, "lon": -95.98},
            {"lat": 41.255, "lon": -96.0}
        ]
        
        # Submit property data requests
        logger.info("Submitting property data requests...")
        requests_data = []
        
        for i, coord in enumerate(coordinates):
            logger.info(f"Submitting request {i+1}/{len(coordinates)} for coordinates {coord}")
            response = client.request_property_data_by_coordinates(coord["lat"], coord["lon"])
            if response and 'request' in response:
                requests_data.append(response)
                logger.info(f"  Request ID: {response['request']['id']}")
            else:
                logger.warning(f"  Failed to submit request for coordinates {coord}")
        
        # Save to JSON
        if requests_data:
            json_filename = f"eagleview_property_data_requests_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(json_filename, 'w') as f:
                json.dump(requests_data, f, indent=2, default=str)
            logger.info(f"Property data requests saved to: {json_filename}")
            
            return requests_data
        else:
            logger.info("No property data requests were successful")
            return []
            
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

def display_report_summary(reports: List[Dict]) -> None:
    """Display a formatted summary of the reports
    
    Args:
        reports (List[Dict]): List of report dictionaries
    """
    if not reports:
        print("No reports to display")
        return
        
    print("\n" + "="*80)
    print("REPORT SUMMARY")
    print("="*80)
    
    # Headers
    print(f"{'ID':<10} {'Status':<15} {'Date Placed':<20} {'Product':<20} {'Address':<30}")
    print("-"*80)
    
    # Display first 10 reports
    for report in reports[:10]:
        report_id = report.get('Id', 'N/A')
        status = report.get('Status', 'Unknown')[:14]  # Truncate if too long
        date_placed = report.get('DatePlaced', 'N/A')[:19]  # Truncate timestamp
        product = report.get('ProductPrimary', 'Unknown')[:19]  # Truncate if too long
        address = f"{report.get('Street1', '')}, {report.get('City', '')}"[:29]  # Truncate if too long
        
        print(f"{report_id:<10} {status:<15} {date_placed:<20} {product:<20} {address:<30}")
    
    if len(reports) > 10:
        print(f"\n... and {len(reports) - 10} more reports")
        
    print("="*80)

def main():
    """Main function"""
    print("EagleView Property Data Requests (Client Credentials)")
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
        print("X Please update the client credentials in the script!")
        print("Look for 'YOUR_CLIENT_ID_HERE' and 'YOUR_CLIENT_SECRET_HERE' in the code")
        return
    
    requests_data = fetch_property_data_requests()
    
    if requests_data:
        print("\n" + "="*60)
        print("PROCESS COMPLETED SUCCESSFULLY!")
        print(f"Submitted {len(requests_data)} property data requests")
        print("Requests saved to JSON file")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("PROCESS COMPLETED WITH NO REQUESTS")
        print("Check the log file for details")
        print("="*60)

if __name__ == "__main__":
    main()