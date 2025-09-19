"""
Script to check property data results and test with additional locations
"""

import json
import time
from client_credentials_eagleview import ClientCredentialsEagleViewClient, EagleViewConfig

def check_property_data_results():
    """Check the results of previously submitted property data requests"""
    
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
    
    print("Checking Property Data Results")
    print("=" * 40)
    
    # Read the request IDs from the previous run
    try:
        with open('eagleview_property_data_requests_20250920_022800.json', 'r') as f:
            requests_data = json.load(f)
    except FileNotFoundError:
        print("No previous requests found. Run fetch_reports_client_credentials.py first.")
        return
    
    # Check each request
    results = []
    for i, request_data in enumerate(requests_data):
        request_id = request_data['request']['id']
        print(f"\nChecking request {i+1}/{len(requests_data)}: {request_id}")
        
        try:
            result = client.get_property_data_result(request_id)
            if result:
                status = result.get('request', {}).get('status', 'Unknown')
                print(f"  Status: {status}")
                
                if status == 'Complete':
                    print("  [SUCCESS] Property data processing completed!")
                    # Save detailed result
                    result_filename = f"property_data_result_{request_id}.json"
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

def test_additional_locations():
    """Test with additional locations within the sandbox area"""
    
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
    
    print("\n\nTesting Additional Locations")
    print("=" * 40)
    
    # Additional coordinates within the sandbox area
    # Bounding box: -96.00532698173473, 41.24140396772262, -95.97589954958912, 41.25672882015283
    additional_locations = [
        {"lat": 41.248, "lon": -95.985, "name": "Downtown Omaha"},
        {"lat": 41.252, "lon": -95.995, "name": "Midtown Omaha"},
        {"lat": 41.243, "lon": -95.978, "name": "North Omaha"}
    ]
    
    # Submit requests for additional locations
    requests_data = []
    for i, location in enumerate(additional_locations):
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
        filename = f"additional_property_data_requests_{time.strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(requests_data, f, indent=2, default=str)
        print(f"\nAll additional requests saved to: {filename}")
    
    return requests_data

if __name__ == "__main__":
    # Check existing results
    results = check_property_data_results()
    
    # Test with additional locations
    additional_requests = test_additional_locations()
    
    print("\n" + "=" * 50)
    print("All tests completed!")
    print("=" * 50)