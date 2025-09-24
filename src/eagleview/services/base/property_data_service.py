"""
Property data service for EagleView API client.
Handles property data requests and results processing with multi-environment support.
"""

import logging
import time
from typing import List, Dict, Optional
from ...client.base import EagleViewClient
from ...config.base import EagleViewSettings
from ...utils.file_ops import save_json_data, generate_timestamped_filename, get_data_directory, setup_logging
from ...utils.cache import cache_result

logger = setup_logging(__name__)

class PropertyDataService:
    """Service for handling property data operations.
    
    This service provides methods to submit property data requests and manage
    the results. It handles retry logic, error handling, and data persistence
    with environment-aware behavior.
    """
    
    def __init__(self, client: EagleViewClient):
        """Initialize the property data service.
        
        Args:
            client: An authenticated EagleViewClient instance
        """
        self.client = client
        self.environment = client.environment
        self.is_sandbox = client.is_sandbox
        
        # Apply environment-specific behavior
        if self.is_sandbox:
            # Import and apply sandbox-specific behavior
            from ..sandbox.overrides import SandboxPropertyDataServiceMixin
            # Enhance this class with sandbox-specific behavior if needed
    
    def submit_coordinates_requests(self, coordinates: List[Dict[str, float]]) -> List[Dict]:
        """Submit property data requests for a list of coordinates.
        
        This method submits property data requests for each coordinate pair
        with retry logic and exponential backoff, based on the environment.
        
        Args:
            coordinates: A list of dictionaries containing 'lat' and 'lon' keys
            
        Returns:
            A list of response dictionaries from the property data requests
            
        Raises:
            ValueError: If coordinates are not in the correct format or out of bounds
        """
        # Validate coordinates
        if not isinstance(coordinates, list):
            raise ValueError("Coordinates must be a list of dictionaries")
        
        for i, coord in enumerate(coordinates):
            if not isinstance(coord, dict):
                raise ValueError(f"Coordinate {i} must be a dictionary")
            if 'lat' not in coord or 'lon' not in coord:
                raise ValueError(f"Coordinate {i} must contain 'lat' and 'lon' keys")
            if not isinstance(coord['lat'], (int, float)) or not isinstance(coord['lon'], (int, float)):
                raise ValueError(f"Coordinate {i} 'lat' and 'lon' must be numeric")
            
            # Validate coordinates based on environment settings
            if self.client.settings.validate_coordinates:
                if self.client.validate_coordinates(coord['lat'], coord['lon']):
                    # Coordinate is valid
                    pass
                else:
                    if self.is_sandbox:
                        raise ValueError(f"Coordinate {i} ({coord['lat']}, {coord['lon']}) is outside sandbox bounds")
                    else:
                        raise ValueError(f"Coordinate {i} ({coord['lat']}, {coord['lon']}) is invalid")
        
        logger.info(f"Submitting property data requests for {len(coordinates)} coordinates")
        requests_data = []
        
        for i, coord in enumerate(coordinates):
            logger.info(f"Submitting request {i+1}/{len(coordinates)} for coordinates {coord}")
            retry_count = 3
            for attempt in range(retry_count):
                try:
                    response = self.client.request_property_data_by_coordinates(
                        coord["lat"], coord["lon"]
                    )
                    if response and 'request' in response:
                        requests_data.append(response)
                        logger.info(f"  Request ID: {response['request']['id']}")
                        break  # Success, break out of retry loop
                    else:
                        logger.warning(f"  Failed to submit request for coordinates {coord}")
                        if attempt < retry_count - 1:
                            logger.info(f"  Retrying... (attempt {attempt + 2}/{retry_count})")
                            time.sleep(2 ** attempt)  # Exponential backoff
                except Exception as e:
                    logger.error(f"  Error submitting request for coordinates {coord}: {e}")
                    if attempt < retry_count - 1:
                        logger.info(f"  Retrying... (attempt {attempt + 2}/{retry_count})")
                        time.sleep(2 ** attempt)  # Exponential backoff
                    else:
                        logger.error(f"  Failed to submit request after {retry_count} attempts")
        
        return requests_data
    
    def save_requests_data(self, requests_data: List[Dict], output_dir: str = None) -> bool:
        """Save property data requests to a JSON file.
        
        Args:
            requests_data: List of property data request responses
            output_dir: Directory to save the file (defaults to data/requests)
            
        Returns:
            True if save was successful, False otherwise
        """
        if not requests_data:
            logger.warning("No requests data to save")
            return False
        
        # Use default directory if not specified
        if output_dir is None:
            output_dir = get_data_directory("requests")
        
        filename = generate_timestamped_filename("eagleview_property_data_requests")
        filepath = f"{output_dir}/{filename}"
        
        return save_json_data(requests_data, filepath)
    
    def get_sandbox_coordinates(self) -> List[Dict[str, float]]:
        """Get default coordinates within the sandbox area.
        
        Returns:
            A list of coordinate dictionaries with 'lat' and 'lon' keys
        """
        # Bounding box: -96.00532698173473, 41.24140396772262, -95.97589954958912, 41.25672882015283
        return [
            {"lat": 41.25, "lon": -95.99},
            {"lat": 41.245, "lon": -95.98},
            {"lat": 41.255, "lon": -96.0}
        ]