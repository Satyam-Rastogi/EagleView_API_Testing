"""
Script to fetch property data results using request IDs from saved request files.
This fills the gap in the existing functionality to retrieve actual property data
after submitting initial requests.
"""

import json
import os
import time
from typing import List, Dict, Optional
from src.eagleview.config.base import EagleViewSettings
from src.eagleview.client.base import EagleViewClient
from src.eagleview.utils.file_ops import setup_logging, save_json_data, get_data_directory

logger = setup_logging(__name__)


def load_request_files(requests_dir: str = None) -> List[Dict]:
    """
    Load property data request files from the requests directory.
    
    Args:
        requests_dir: Directory containing request files (defaults to data/requests)
    
    Returns:
        List of request data dictionaries
    """
    if requests_dir is None:
        requests_dir = get_data_directory("property_requests")
    
    if not os.path.exists(requests_dir):
        logger.warning(f"Requests directory does not exist: {requests_dir}")
        return []
    
    request_files = []
    for filename in os.listdir(requests_dir):
        if filename.endswith('.json') and 'request' in filename:
            filepath = os.path.join(requests_dir, filename)
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        request_files.extend(data)  # Add individual requests
                    else:
                        request_files.append(data)  # Add single request
                logger.info(f"Loaded requests from {filename}")
            except Exception as e:
                logger.error(f"Error loading {filename}: {e}")
    
    return request_files


def get_request_ids(request_data: List[Dict]) -> List[str]:
    """
    Extract request IDs from request data.
    
    Args:
        request_data: List of request dictionaries
        
    Returns:
        List of request IDs
    """
    request_ids = []
    for request in request_data:
        if 'request' in request and 'id' in request['request']:
            request_ids.append(request['request']['id'])
        elif 'id' in request:
            request_ids.append(request['id'])
    return request_ids


def fetch_property_results(settings: EagleViewSettings, request_ids: List[str]) -> Dict[str, Dict]:
    """
    Fetch property data results for the given request IDs.
    
    Args:
        settings: EagleView configuration settings
        request_ids: List of request IDs to fetch results for
        
    Returns:
        Dictionary mapping request IDs to their results
    """
    client = EagleViewClient(settings)
    results = {}
    
    for i, request_id in enumerate(request_ids):
        logger.info(f"[{i+1}/{len(request_ids)}] Fetching result for request ID: {request_id}")
        
        # Retry loop for requests that are still processing
        max_attempts = 10
        attempt = 0
        
        while attempt < max_attempts:
            result = client.get_property_data_result(request_id)
            
            if result:
                # Check if the request is still processing
                status = result.get('status', result.get('request', {}).get('status', 'Unknown'))
                
                if status == 'In Progress' or ('In Progress' in str(result.get('request', {}).get('status', ''))):
                    logger.info(f"  Request {request_id} still in progress, status: {status}. Waiting...")
                    time.sleep(30)  # Wait 30 seconds before trying again
                    attempt += 1
                else:
                    logger.info(f"  Retrieved result for request {request_id}, status: {status}")
                    results[request_id] = result
                    break
            else:
                logger.warning(f"  Failed to retrieve result for request {request_id}")
                results[request_id] = {}
                break
        
        # If we've exhausted attempts and still have no complete result
        if attempt == max_attempts:
            logger.warning(f"  Max attempts reached for request {request_id}, saving latest result")
            results[request_id] = result if result else {}
    
    return results


def save_property_results(results: Dict[str, Dict], output_dir: str = None):
    """
    Save property data results to individual JSON files.
    
    Args:
        results: Dictionary of request ID to result data
        output_dir: Directory to save results (defaults to data/results)
    """
    if output_dir is None:
        output_dir = get_data_directory("property_results")
    
    for request_id, result in results.items():
        if result:  # Only save if there's actual result data
            filename = f"property_data_result_{request_id}.json"
            filepath = os.path.join(output_dir, filename)
            save_json_data(result, filepath)
            logger.info(f"Saved property data result to: {filepath}")
        else:
            logger.warning(f"No result data to save for request ID: {request_id}")


def main():
    """Main function to fetch property data results."""
    print("EagleView Property Data Results Fetcher")
    print("=" * 50)
    
    # Load configuration
    settings = EagleViewSettings.from_environment()
    if not settings.validate():
        print("❌ Please set the following environment variables:")
        print("   EAGLEVIEW_CLIENT_ID")
        print("   EAGLEVIEW_CLIENT_SECRET")
        return

    # Load request files to get request IDs
    print("\n1. Loading existing property data requests...")
    request_data = load_request_files()
    
    if not request_data:
        print("No property data requests found in data/requests/")
        print("You need to submit property data requests first using:")
        print("  python -m cli.eagleview --operation property-data")
        return
    
    # Extract request IDs
    request_ids = get_request_ids(request_data)
    print(f"Found {len(request_ids)} request IDs to fetch results for")
    
    if not request_ids:
        print("No valid request IDs found in the request files")
        return
    
    # Fetch property data results
    print(f"\n2. Fetching property data results for {len(request_ids)} requests...")
    results = fetch_property_results(settings, request_ids)
    
    # Save results
    print(f"\n3. Saving property data results...")
    save_property_results(results)
    
    print(f"\n{'='*50}")
    print("PROCESS COMPLETED!")
    print(f"Fetched results for {len([r for r in results.values() if r])} out of {len(request_ids)} requests")
    print("Results saved to data/results/ directory")
    print("="*50)


if __name__ == "__main__":
    main()