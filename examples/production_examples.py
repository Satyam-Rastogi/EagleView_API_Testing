"""
Examples for using the EagleView API client in production environment.
"""

from src.eagleview.config import create_config
from src.eagleview.client import create_client
from src.eagleview.services import PropertyDataService

def example_production_property_data():
    """Example of property data requests in production."""
    # Create production configuration
    config = create_config('production')
    
    # Create client
    client = create_client(config)
    
    # Create service
    service = PropertyDataService(client)
    
    # Use coordinates for a real location (e.g., New York, but with safe values)
    coordinates = [
        {"lat": 41.25, "lon": -95.99},  # Use sandbox coordinates to avoid validation issues for demo
    ]
    
    # Submit requests (no coordinate validation in production by default)
    try:
        requests_data = service.submit_coordinates_requests(coordinates)
        
        print("Successfully submitted {} requests in production environment".format(len(requests_data)))
        print("API URLs: {}".format(config.get_api_urls()))
        print("Validate coordinates: {}".format(config.validate_coordinates))
        
        return requests_data
    except ValueError as e:
        print("Coordinate validation error (expected without valid credentials): {}".format(e))
        return None

def example_production_imagery():
    """Example of imagery requests in production."""
    from src.eagleview.services.base.imagery_service import ImageryService
    
    # Create production configuration
    config = create_config('production')
    
    # Create client
    client = create_client(config)
    
    # Create service
    service = ImageryService(client)
    
    # Use coordinates for a real location (same for demo purposes)
    coordinates = [
        {"lat": 41.25, "lon": -95.99},  # Use sandbox coordinates for demo
    ]
    
    # Request imagery for the first coordinate
    try:
        coord = coordinates[0]
        imagery_data = service.request_imagery_for_location("production_demo", coord["lat"], coord["lon"])
        print("Imagery data retrieved: {}".format(bool(imagery_data)))
        print("Environment: {}".format(config.environment))
        return imagery_data
    except Exception as e:
        print("Imagery request failed (expected without valid credentials): {}".format(e))
        return None

if __name__ == "__main__":
    print("Running production examples...")
    print("\n1. Property Data Example:")
    example_production_property_data()
    
    print("\n2. Imagery Example:")
    example_production_imagery()
    
    print("\nProduction examples completed!")
"""