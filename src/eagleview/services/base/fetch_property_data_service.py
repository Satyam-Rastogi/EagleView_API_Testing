"""
Fetch property data using Client Credentials Authentication.
Refactored version with improved structure and error handling.
"""

from ..core.configuration import EagleViewSettings
from ..core.client import EagleViewClient
from .property_data_service import PropertyDataService
from ..core.file_operations import setup_logging

# Setup logging
logger = setup_logging(__name__)

def main():
    """Main function."""
    print("EagleView Property Data Requests (Client Credentials)")
    print("=" * 60)
    print("NO BROWSER REQUIRED - Fully Automated!")
    print("Using OAuth 2.0 Client Credentials Flow")
    print("Perfect for server-to-server communication")
    print()
    
    # Load configuration
    settings = EagleViewSettings.from_environment()
    if not settings.validate():
        print("❌ Please set the following environment variables:")
        print("   EAGLEVIEW_CLIENT_ID")
        print("   EAGLEVIEW_CLIENT_SECRET")
        return
    
    # Create client and service
    client = EagleViewClient(settings)
    service = PropertyDataService(client)
    
    # Get coordinates and submit requests
    coordinates = service.get_sandbox_coordinates()
    requests_data = service.submit_coordinates_requests(coordinates)
    
    # Save results
    if requests_data:
        if service.save_requests_data(requests_data):
            print("\n" + "="*60)
            print("PROCESS COMPLETED SUCCESSFULLY!")
            print(f"Submitted {len(requests_data)} property data requests")
            print("Requests saved to JSON file")
            print("="*60)
        else:
            print("\n" + "="*60)
            print("ERROR: Failed to save requests data")
            print("="*60)
    else:
        print("\n" + "="*60)
        print("PROCESS COMPLETED WITH NO REQUESTS")
        print("Check the log file for details")
        print("="*60)

if __name__ == "__main__":
    main()