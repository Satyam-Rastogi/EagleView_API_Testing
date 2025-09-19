"""
Script to test custom locations within the EagleView sandbox area
"""

import json
import time
from client_credentials_eagleview import ClientCredentialsEagleViewClient, EagleViewConfig

def test_custom_locations():
    """Test with custom locations within the sandbox area"""
    
    # Initialize configuration
    config = EagleViewConfig(
        client_id="0oa16yo11pa57TLPa2p8",
        client_secret="BAfJ05yNlGaNt8Gm3gnO_0ekJ1DRlwJsaNgU4aePS9o5iCuxyOuZL1kmxxHionD7",
        requests_per_second=3,
        requests_per_minute=50,
        is_sandbox=True
    )
    
    # Create client
    client = ClientCredentialsEagleViewClient(config)
    
    print("Testing Custom Locations")
    print("=" * 40)
    
    # Custom coordinates within the sandbox area
    # Bounding box: -96.00532698173473, 41.24140396772262, -95.97589954958912, 41.25672882015283
    custom_locations = [
        {"lat": 41.251, "lon": -95.992, "name": "Custom Location 1"},
        {"lat": 41.247, "lon": -95.988, "name": "Custom Location 2"},
        {"lat": 41.254, "lon": -95.998, "name": "Custom Location 3"}
    ]
    
    # Submit requests for custom locations
    requests_data = []
    for i, location in enumerate(custom_locations):
        lat, lon, name = location["lat"], location["lon"], location["name"]
        print(f"\nSubmitting request for {name} ({lat}, {lon})")
        
        try:
            response = client.request_property_data_by_coordinates(lat, lon)
            if response and 'request' in response:
                request_id = response['request']['id']
                print(f"  [SUCCESS] Request submitted: {request_id}")
                requests_data.append({
                    "location_name": name,
                    "coordinates": {"lat": lat, "lon": lon},
                    "request_id": request_id,
                    "response": response
                })
                
                # Also request imagery for the same location
                print(f"  Requesting imagery for {name}")
                imagery_request = {
                    "center": {
                        "point": {
                            "geojson": {
                                "value": json.dumps({
                                    "type": "Feature",
                                    "geometry": {
                                        "type": "Point",
                                        "coordinates": [lon, lat]
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
                if imagery_response:
                    print(f"  [SUCCESS] Imagery request completed")
                    # Save imagery data
                    imagery_filename = f"imagery_data_{name.replace(' ', '_')}_{lat}_{lon}.json"
                    with open(imagery_filename, 'w') as f:
                        json.dump(imagery_response, f, indent=2, default=str)
                    print(f"  Imagery data saved to: {imagery_filename}")
                else:
                    print(f"  [WARNING] No imagery data returned")
            else:
                print(f"  [ERROR] Failed to submit property data request")
        except Exception as e:
            print(f"  [ERROR] Exception: {e}")
        
        # Small delay between requests
        time.sleep(1)
    
    # Save all requests data
    if requests_data:
        filename = f"custom_property_data_requests_{time.strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(requests_data, f, indent=2, default=str)
        print(f"\nAll custom requests saved to: {filename}")
    
    return requests_data

def check_custom_results(request_ids):
    """Check the results of custom property data requests"""
    
    # Initialize configuration
    config = EagleViewConfig(
        client_id="0oa16yo11pa57TLPa2p8",
        client_secret="BAfJ05yNlGaNt8Gm3gnO_0ekJ1DRlwJsaNgU4aePS9o5iCuxyOuZL1kmxxHionD7",
        requests_per_second=3,
        requests_per_minute=50,
        is_sandbox=True
    )
    
    # Create client
    client = ClientCredentialsEagleViewClient(config)
    
    print("\n\nChecking Custom Property Data Results")
    print("=" * 40)
    
    # Check each request
    results = []
    for i, request_id in enumerate(request_ids):
        print(f"\nChecking request {i+1}/{len(request_ids)}: {request_id}")
        
        try:
            result = client.get_property_data_result(request_id)
            if result:
                status = result.get('request', {}).get('status', 'Unknown')
                print(f"  Status: {status}")
                
                if status == 'Complete':
                    print("  [SUCCESS] Property data processing completed!")
                    # Save detailed result
                    result_filename = f"custom_property_data_result_{request_id}.json"
                    with open(result_filename, 'w') as f:
                        json.dump(result, f, indent=2, default=str)
                    print(f"  Result saved to: {result_filename}")
                elif status == 'In Progress':
                    print("  [INFO] Processing still in progress...")
                else:
                    print(f"  [INFO] Status: {status}")
                
                results.append(result)
            else:
                print("  [ERROR] Failed to get result")
        except Exception as e:
            print(f"  [ERROR] Exception: {e}")
    
    return results

if __name__ == "__main__":
    # Test with custom locations
    custom_requests = test_custom_locations()
    
    # Extract request IDs for checking results
    request_ids = [req["request_id"] for req in custom_requests]
    
    if request_ids:
        # Wait a bit for processing
        print("\nWaiting for processing to complete...")
        time.sleep(10)
        
        # Check results
        results = check_custom_results(request_ids)
    
    print("\n" + "=" * 50)
    print("Custom location tests completed!")
    print("=" * 50)