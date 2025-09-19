"""
Script to test property data requests using addresses
"""

import json
import time
from client_credentials_eagleview import ClientCredentialsEagleViewClient, EagleViewConfig

def test_address_based_requests():
    """Test with address-based property data requests"""
    
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
    
    print("Testing Address-Based Property Data Requests")
    print("=" * 50)
    
    # Test addresses (these should be within the sandbox area)
    test_addresses = [
        "965 S 50th St, Omaha, NE 68106",
        "835 S 51st St, Omaha, NE 68106"
    ]
    
    # Submit requests for addresses
    requests_data = []
    for i, address in enumerate(test_addresses):
        print(f"\nSubmitting request for address: {address}")
        
        try:
            response = client.request_property_data_by_address(address)
            if response and 'request' in response:
                request_id = response['request']['id']
                print(f"  [SUCCESS] Request submitted: {request_id}")
                requests_data.append({
                    "address": address,
                    "request_id": request_id,
                    "response": response
                })
            else:
                print(f"  [ERROR] Failed to submit property data request")
        except Exception as e:
            print(f"  [ERROR] Exception: {e}")
        
        # Small delay between requests
        time.sleep(1)
    
    # Save all requests data
    if requests_data:
        filename = f"address_based_property_data_requests_{time.strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(requests_data, f, indent=2, default=str)
        print(f"\nAll address-based requests saved to: {filename}")
    
    return requests_data

def check_address_results(request_ids):
    """Check the results of address-based property data requests"""
    
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
    
    print("\n\nChecking Address-Based Property Data Results")
    print("=" * 50)
    
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
                    result_filename = f"address_property_data_result_{request_id}.json"
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
    # Test with address-based requests
    address_requests = test_address_based_requests()
    
    # Extract request IDs for checking results
    request_ids = [req["request_id"] for req in address_requests]
    
    if request_ids:
        # Wait a bit for processing
        print("\nWaiting for processing to complete...")
        time.sleep(10)
        
        # Check results
        results = check_address_results(request_ids)
    
    print("\n" + "=" * 50)
    print("Address-based tests completed!")
    print("=" * 50)