"""
Demo: Fetch EagleView Reports Information

This script demonstrates how to fetch information about measurement/order reports 
from EagleView API using OAuth 2.0 Client Credentials flow.

Usage:
1. Update the configuration with your actual client credentials
2. Run the script: python demo_fetch_reports.py
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
        logging.FileHandler('demo_fetch_reports.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def demo_fetch_reports():
    """Demo function to fetch and display report information"""
    
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
        token = client._get_access_token()
        logger.info("Authentication successful!")
        
        # Fetch all reports
        logger.info("Fetching all customer reports...")
        reports = client.get_all_customer_reports(save_to_csv=True)
        
        if not reports:
            logger.info("No reports found for this customer")
            return []
        
        logger.info(f"Found {len(reports)} reports.")
        
        # Display summary information for first 5 reports
        print("\n" + "="*100)
        print("REPORT INFORMATION (First 5 Reports)")
        print("="*100)
        print(f"{'ID':<10} {'Status':<15} {'Product':<20} {'Date Placed':<20} {'Download Link':<25}")
        print("-"*100)
        
        for i, report in enumerate(reports[:5]):
            report_id = report.get('Id') or report.get('ReportId', 'N/A')
            status = report.get('Status', 'Unknown')[:14]
            product = report.get('ProductPrimary', 'Unknown')[:19]
            date_placed = report.get('DatePlaced', 'N/A')[:19]
            has_download = 'Yes' if report.get('ReportDownloadLink') else 'No'
            
            print(f"{report_id:<10} {status:<15} {product:<20} {date_placed:<20} {has_download:<25}")
        
        if len(reports) > 5:
            print(f"\n... and {len(reports) - 5} more reports")
        
        print("="*100)
        
        # Get detailed information for the first report
        if reports:
            first_report = reports[0]
            report_id = first_report.get('Id') or first_report.get('ReportId')
            
            if report_id:
                logger.info(f"Getting detailed information for report {report_id}")
                report_detail = client.get_report_detail(report_id)
                
                if report_detail:
                    print(f"\nDETAILED INFORMATION FOR REPORT {report_id}")
                    print("-"*50)
                    
                    # Display key information
                    print(f"Status: {report_detail.get('Status', 'N/A')}")
                    print(f"Product: {report_detail.get('ProductPrimary', 'N/A')}")
                    print(f"Date Placed: {report_detail.get('DatePlaced', 'N/A')}")
                    print(f"Date Completed: {report_detail.get('DateCompleted', 'N/A')}")
                    print(f"Address: {report_detail.get('Street', 'N/A')}, {report_detail.get('City', 'N/A')}")
                    print(f"Area: {report_detail.get('Area', 'N/A')} sq ft")
                    print(f"Pitch: {report_detail.get('Pitch', 'N/A')}")
                    print(f"Has Download Link: {'Yes' if report_detail.get('ReportDownloadLink') else 'No'}")
                    
                    # Get file links
                    logger.info(f"Getting file links for report {report_id}")
                    file_links = client.get_report_file_links(report_id)
                    
                    if file_links and isinstance(file_links, list):
                        print(f"\nFILE LINKS ({len(file_links)} files available):")
                        for i, link_info in enumerate(file_links):
                            file_type = link_info.get('FileType', 'Unknown')
                            expire_time = link_info.get('ExpireTimestamp', 'N/A')
                            print(f"  {i+1}. Type: {file_type}, Expires: {expire_time}")
                    else:
                        print("\nNo file links available for this report.")
        
        return reports
        
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

def main():
    """Main function"""
    print("EagleView Reports Information Demo (Client Credentials)")
    print("=" * 60)
    print("This demo shows how to fetch information about reports")
    print("without downloading the actual files.")
    print()
    
    # Check if credentials are properly configured
    client_id = "0oa16yo11pa57TLPa2p8"
    client_secret = "BAfJ05yNlGaNt8Gm3gnO_0ekJ1DRlwJsaNgU4aePS9o5iCuxyOuZL1kmxxHionD7"
    
    # Validate credentials
    if not client_id or not client_secret:
        print("❌ Please update the client credentials in the script!")
        print("💡 Look for 'YOUR_CLIENT_ID_HERE' and 'YOUR_CLIENT_SECRET_HERE' in the code")
        return
    
    reports = demo_fetch_reports()
    
    if reports:
        print("\n" + "="*60)
        print("DEMO COMPLETED SUCCESSFULLY!")
        print(f"Found {len(reports)} reports")
        print("Check the log file for detailed information")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("DEMO COMPLETED - NO REPORTS FOUND")
        print("Check the log file for details")
        print("="*60)

if __name__ == "__main__":
    main()