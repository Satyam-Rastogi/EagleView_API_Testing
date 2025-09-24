"""
Imagery service for EagleView API client.
Handles imagery requests and processing.
"""

import logging
import json
import time
from typing import List, Dict, Optional
from ...client.base import EagleViewClient
from ...utils.file_ops import save_json_data, generate_timestamped_filename, get_data_directory, setup_logging

logger = setup_logging(__name__)

class ImageryService:
    """Service for handling imagery operations.
    
    This service provides methods to request and manage imagery data from the
    EagleView Imagery API. It handles retry logic, error handling, and data persistence.
    """
    
    def __init__(self, client: EagleViewClient):
        """Initialize the imagery service.
        
        Args:
            client: An authenticated EagleViewClient instance
        """
        self.client = client
    
    def request_imagery_for_location(self, name: str, lat: float, lon: float) -> Optional[Dict]:
        """Request imagery for a specific location.
        
        This method requests imagery for a specific location with retry logic
        and exponential backoff.
        
        Args:
            name: A descriptive name for the location
            lat: Latitude coordinate
            lon: Longitude coordinate
            
        Returns:
            A dictionary containing the imagery response data or None if failed
            
        Raises:
            ValueError: If coordinates are not valid or out of bounds
        """
        # Validate coordinates
        if not isinstance(lat, (int, float)) or not isinstance(lon, (int, float)):
            raise ValueError("Latitude and longitude must be numeric")
        
        # If in sandbox mode, validate coordinates are within bounds
        if self.client.settings.is_sandbox:
            bounds = {
                'min_lat': 41.24140396772262,
                'max_lat': 41.25672882015283,
                'min_lon': -96.00532698173473,
                'max_lon': -95.97589954958912
            }
            if not (bounds['min_lat'] <= lat <= bounds['max_lat']):
                raise ValueError(f"Latitude {lat} is outside sandbox bounds")
            if not (bounds['min_lon'] <= lon <= bounds['max_lon']):
                raise ValueError(f"Longitude {lon} is outside sandbox bounds")
        
        logger.info(f"Requesting imagery for {name} ({lat}, {lon})")
        
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
        
        retry_count = 3
        for attempt in range(retry_count):
            try:
                imagery_response = self.client.get_imagery_for_location(imagery_request)
                if imagery_response:
                    logger.info(f"  [SUCCESS] Imagery request completed for {name}")
                    return imagery_response
                else:
                    logger.warning(f"  [WARNING] No imagery data returned for {name}")
                    if attempt < retry_count - 1:
                        logger.info(f"  Retrying... (attempt {attempt + 2}/{retry_count})")
                        time.sleep(2 ** attempt)  # Exponential backoff
                    return None
            except Exception as e:
                logger.error(f"  [ERROR] Exception during imagery request for {name}: {e}")
                if attempt < retry_count - 1:
                    logger.info(f"  Retrying... (attempt {attempt + 2}/{retry_count})")
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"  Failed to get imagery after {retry_count} attempts")
                    return None
    
    def save_imagery_data(self, imagery_data: Dict, name: str, lat: float, lon: float, 
                         output_dir: str = None) -> bool:
        """Save imagery data to a JSON file.
        
        Args:
            imagery_data: The imagery response data to save
            name: A descriptive name for the location
            lat: Latitude coordinate
            lon: Longitude coordinate
            output_dir: Directory to save the file (defaults to data/imagery)
            
        Returns:
            True if save was successful, False otherwise
        """
        if not imagery_data:
            logger.warning("No imagery data to save")
            return False
        
        # Use default directory if not specified
        if output_dir is None:
            output_dir = get_data_directory("imagery")
        
        filename = f"imagery_data_{name.replace(' ', '_')}_{lat}_{lon}.json"
        filepath = f"{output_dir}/{filename}"
        
        return save_json_data(imagery_data, filepath)