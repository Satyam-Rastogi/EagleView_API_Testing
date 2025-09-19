"""
Script to download property images for custom locations
"""

import json
import requests
from client_credentials_eagleview import ClientCredentialsEagleViewClient, EagleViewConfig
import os

def download_images_for_custom_locations():
    """Download property images for custom locations"""
    
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
    
    # Create directory for images
    images_dir = "custom_location_images"
    os.makedirs(images_dir, exist_ok=True)
    
    print("Downloading Property Images for Custom Locations")
    print("=" * 60)
    
    # Read the custom property data result file
    try:
        with open('custom_property_data_result_db49fd0b-e350-4bf0-9b0f-07f9891a9f84.json', 'r') as f:
            property_data = json.load(f)
    except FileNotFoundError:
        print("Custom property data file not found. Run the custom locations script first.")
        return
    
    # Get image references
    image_references = property_data.get('property_images', {}).get('image_references', [])
    imagery_data = property_data.get('imagery', {})
    
    print(f"Found {len(image_references)} image references")
    
    # Download each image
    downloaded_count = 0
    for i, image_ref in enumerate(image_references):
        if image_ref in imagery_data:
            image_info = imagery_data[image_ref]
            image_token = image_info.get('image_token')
            
            if image_token:
                print(f"\nDownloading image {i+1}/{len(image_references)}: {image_ref}")
                print(f"  Token: {image_token[:20]}...")
                print(f"  View: {image_info.get('metadata', {}).get('view', 'unknown')}")
                print(f"  Shot date: {image_info.get('metadata', {}).get('shot_date', 'unknown')}")
                
                try:
                    # Get access token
                    token = client._get_access_token()
                    
                    # Prepare headers
                    headers = {
                        'Authorization': f'Bearer {token}',
                        'Accept': 'image/png'
                    }
                    
                    # Make request to download image
                    url = f"https://sandbox.apis.eagleview.com/property/v2/image/{image_token}"
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
                        
                        print(f"  [SUCCESS] Image saved to: {filename}")
                        downloaded_count += 1
                    else:
                        print(f"  [ERROR] Failed to download image: {response.status_code}")
                        print(f"  Response: {response.text[:100]}...")
                        
                except Exception as e:
                    print(f"  [ERROR] Exception during download: {e}")
            else:
                print(f"  [WARNING] No image token found for {image_ref}")
        else:
            print(f"  [WARNING] No imagery data found for {image_ref}")
    
    print(f"\nDownload Summary:")
    print(f"  Total images referenced: {len(image_references)}")
    print(f"  Successfully downloaded: {downloaded_count}")
    print(f"  Images saved to: {images_dir}")
    
    # Also try to download images for the address-based requests
    print("\n" + "=" * 60)
    print("Downloading Property Images for Address-Based Requests")
    print("=" * 60)
    
    # Create directory for address-based images
    address_images_dir = "address_based_images"
    os.makedirs(address_images_dir, exist_ok=True)
    
    # Read one of the address-based property data result files
    try:
        with open('address_property_data_result_f0663526-d75d-499d-af08-1df40b28893f.json', 'r') as f:
            property_data = json.load(f)
    except FileNotFoundError:
        print("Address-based property data file not found.")
        return
    
    # Get image references
    image_references = property_data.get('property_images', {}).get('image_references', [])
    imagery_data = property_data.get('imagery', {})
    
    print(f"Found {len(image_references)} image references")
    
    # Download each image
    address_downloaded_count = 0
    for i, image_ref in enumerate(image_references):
        if image_ref in imagery_data:
            image_info = imagery_data[image_ref]
            image_token = image_info.get('image_token')
            
            if image_token:
                print(f"\nDownloading image {i+1}/{len(image_references)}: {image_ref}")
                print(f"  Token: {image_token[:20]}...")
                print(f"  View: {image_info.get('metadata', {}).get('view', 'unknown')}")
                print(f"  Shot date: {image_info.get('metadata', {}).get('shot_date', 'unknown')}")
                
                try:
                    # Get access token
                    token = client._get_access_token()
                    
                    # Prepare headers
                    headers = {
                        'Authorization': f'Bearer {token}',
                        'Accept': 'image/png'
                    }
                    
                    # Make request to download image
                    url = f"https://sandbox.apis.eagleview.com/property/v2/image/{image_token}"
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
                        filename = f"{address_images_dir}/{image_ref}_{image_token[:8]}{extension}"
                        
                        # Save image
                        with open(filename, 'wb') as f:
                            f.write(response.content)
                        
                        print(f"  [SUCCESS] Image saved to: {filename}")
                        address_downloaded_count += 1
                    else:
                        print(f"  [ERROR] Failed to download image: {response.status_code}")
                        print(f"  Response: {response.text[:100]}...")
                        
                except Exception as e:
                    print(f"  [ERROR] Exception during download: {e}")
            else:
                print(f"  [WARNING] No image token found for {image_ref}")
        else:
            print(f"  [WARNING] No imagery data found for {image_ref}")
    
    print(f"\nAddress-Based Download Summary:")
    print(f"  Total images referenced: {len(image_references)}")
    print(f"  Successfully downloaded: {address_downloaded_count}")
    print(f"  Images saved to: {address_images_dir}")

if __name__ == "__main__":
    download_images_for_custom_locations()