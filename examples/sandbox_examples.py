"""
Examples for using the EagleView API client in sandbox environment.
"""

from src.eagleview.config import create_config
from src.eagleview.client import create_client
from src.eagleview.services import PropertyDataService

def example_sandbox_property_data():
    """Example of property data requests in sandbox."""
    # Create sandbox configuration
    config = create_config('sandbox')
    
    # Create client
    client = create_client(config)
    
    # Create service
    service = PropertyDataService(client)
    
    # Get sandbox coordinates
    coordinates = service.get_sandbox_coordinates()
    
    # Submit requests (will be validated against sandbox bounds)
    try:
        requests_data = service.submit_coordinates_requests(coordinates)
        
        print("Successfully submitted {} requests in sandbox environment".format(len(requests_data)))
        print("API URLs: {}".format(config.get_api_urls()))
        
        return requests_data
    except ValueError as e:
        print("Coordinate validation error (expected without valid credentials): {}".format(e))
        return None

def example_sandbox_imagery():
    """Example of imagery requests in sandbox."""
    from src.eagleview.services.base.imagery_service import ImageryService
    from src.eagleview.services.base.property_data_service import PropertyDataService
    
    # Create sandbox configuration
    config = create_config('sandbox')
    
    # Create client
    client = create_client(config)
    
    # Create service
    service = ImageryService(client)
    
    # Use the property data service to get sandbox coordinates
    property_service = PropertyDataService(client)
    coordinates = property_service.get_sandbox_coordinates()
    
    # Request imagery for the first coordinate
    try:
        coord = coordinates[0]
        imagery_data = service.request_imagery_for_location("sandbox_demo", coord["lat"], coord["lon"])
        
        print("Imagery data retrieved: {}".format(bool(imagery_data)))
        print("Environment: {}".format(config.environment))
        
        return imagery_data
    except Exception as e:
        print("Imagery request failed (expected without valid credentials): {}".format(e))
        return None

if __name__ == "__main__":
    print("Running sandbox examples...")
    print("\n1. Property Data Example:")
    example_sandbox_property_data()
    
    print("\n2. Imagery Example:")
    example_sandbox_imagery()
    
    print("\nSandbox examples completed!")