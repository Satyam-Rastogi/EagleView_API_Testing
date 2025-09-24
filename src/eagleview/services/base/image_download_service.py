"""
Image download service for EagleView API client.
Handles downloading and saving property images.
"""

import logging
import requests
import os
import time
from typing import Dict, List
from ...client.base import EagleViewClient
from ...utils.file_ops import ensure_directory_exists, get_data_directory, setup_logging

logger = setup_logging(__name__)

class ImageDownloadService:
    """Service for handling image download operations.
    
    This service provides methods to download property images using image tokens
    from property data results. It handles retry logic, error handling, and
    file management.
    """
    
    def __init__(self, client: EagleViewClient):
        """Initialize the image download service.
        
        Args:
            client: An authenticated EagleViewClient instance
        """
        self.client = client
    
    def download_property_images(self, property_data: Dict, image_category: str = "property_images") -> int:
        """Download property images using image tokens from property data results.
        
        This method downloads property images with retry logic and exponential backoff.
        Images are saved in the data/imagery/{image_category} directory.
        
        Args:
            property_data: Property data response containing image references and tokens
            image_category: Category name for organizing downloaded images
            
        Returns:
            Number of successfully downloaded images
        """
        # Create directory for images in the data/imagery folder
        images_dir = get_data_directory(f"imagery/{image_category}")
        ensure_directory_exists(images_dir)
        
        # Get image references
        image_references = property_data.get('property_images', {}).get('image_references', [])
        imagery_data = property_data.get('imagery', {})
        
        logger.info(f"Found {len(image_references)} image references")
        
        # Get the base URL for image downloads from client settings
        urls = self.client.settings.get_api_urls()
        image_base_url = urls['imagery_base_url']
        
        # Download each image
        downloaded_count = 0
        for i, image_ref in enumerate(image_references):
            if image_ref in imagery_data:
                image_info = imagery_data[image_ref]
                image_token = image_info.get('image_token')
                
                if image_token:
                    logger.info(f"Downloading image {i+1}/{len(image_references)}: {image_ref}")
                    logger.info(f"  Token: {image_token}")
                    logger.info(f"  View: {image_info.get('metadata', {}).get('view', 'unknown')}")
                    logger.info(f"  Shot date: {image_info.get('metadata', {}).get('shot_date', 'unknown')}")
                    
                    retry_count = 3
                    for attempt in range(retry_count):
                        try:
                            # Get access token
                            token = self.client.get_access_token()
                            
                            # Prepare headers
                            headers = {
                                'Authorization': f'Bearer {token}',
                                'Accept': 'image/png'
                            }
                            
                            # Make request to download image using configurable URL
                            url = f"{image_base_url}/property/v2/image/{image_token}"
                            response = requests.get(url, headers=headers)
                            
                            if response.status_code == 200:
                                # Determine file extension based on content type
                                content_type = response.headers.get('Content-Type', 'image/png')
                                if 'jpeg' in content_type:
                                    extension = '.jpg'
                                elif 'png' in content_type:
                                    extension = '.png'
                                else:
                                    extension = '.png'
                                
                                # Create filename
                                filename = f"{images_dir}/{image_ref}_{image_token[:8]}{extension}"
                                
                                # Save image
                                with open(filename, 'wb') as f:
                                    f.write(response.content)
                                
                                logger.info(f"  [SUCCESS] Image saved to: {filename}")
                                downloaded_count += 1
                                break  # Success, break out of retry loop
                            else:
                                logger.error(f"  [ERROR] Failed to download image: {response.status_code}")
                                logger.error(f"  Response: {response.text[:100]}...")
                                if attempt < retry_count - 1:
                                    logger.info(f"  Retrying... (attempt {attempt + 2}/{retry_count})")
                                    time.sleep(2 ** attempt)  # Exponential backoff
                        except Exception as e:
                            logger.error(f"  [ERROR] Exception during download: {e}")
                            if attempt < retry_count - 1:
                                logger.info(f"  Retrying... (attempt {attempt + 2}/{retry_count})")
                                time.sleep(2 ** attempt)  # Exponential backoff
                            else:
                                logger.error(f"  Failed to download image after {retry_count} attempts")
                else:
                    logger.warning(f"  [WARNING] No image token found for {image_ref}")
            else:
                logger.warning(f"  [WARNING] No imagery data found for {image_ref}")
        
        logger.info(f"Download Summary:")
        logger.info(f"  Total images referenced: {len(image_references)}")
        logger.info(f"  Successfully downloaded: {downloaded_count}")
        logger.info(f"  Images saved to: {images_dir}")
        
        return downloaded_count