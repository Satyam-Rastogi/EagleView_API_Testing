"""
Script to download EagleView reports and related files using the Measurement Order API.
This script implements report downloading functionality using the /v1/File/GetReportFile
and /v3/Report/{reportId}/file-links endpoints.
"""

import json
import os
import requests
import time
from typing import Dict, List, Optional
from src.eagleview.config.base import EagleViewSettings
from src.eagleview.client.base import EagleViewClient
from src.eagleview.utils.file_ops import setup_logging, ensure_directory_exists, get_data_directory

logger = setup_logging(__name__)


def get_report_file_links(client: EagleViewClient, report_id: int) -> Dict:
    """
    Get file download links for a specific report using the file-links endpoint.
    
    Args:
        client: Authenticated EagleViewClient
        report_id: Report ID to get file links for
        
    Returns:
        Dictionary containing file download links
    """
    try:
        # Use the client's make_request method but target the reports API
        # The base URL may need to be different for reports
        endpoint = f'/v3/Report/{report_id}/file-links'
        response = client.make_request('GET', endpoint, use_imagery_base=False)  # Using main base URL for reports
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.warning(f"Failed to get file links for report {report_id}: {response.status_code}")
            logger.warning(f"Response: {response.text}")
            return {}
    except Exception as e:
        logger.error(f"Error getting file links for report {report_id}: {e}")
        return {}


def download_report_file(client: EagleViewClient, report_id: int, file_type: Optional[int] = None, 
                        file_format: Optional[int] = None, output_dir: str = None) -> bool:
    """
    Download a specific report file using the GetReportFile endpoint.
    
    Args:
        client: Authenticated EagleViewClient
        report_id: Report ID to download file for
        file_type: File type to download (optional)
        file_format: File format to download (optional)
        output_dir: Directory to save the file (optional)
        
    Returns:
        True if download was successful, False otherwise
    """
    if output_dir is None:
        output_dir = get_data_directory("property_reports")
        ensure_directory_exists(output_dir)
    
    try:
        # Build the endpoint with query parameters
        endpoint = f'/v1/File/GetReportFile?reportId={report_id}'
        if file_type is not None:
            endpoint += f'&fileType={file_type}'
        if file_format is not None:
            endpoint += f'&fileFormat={file_format}'
        
        # Get access token
        token = client.get_access_token()
        
        # Prepare headers for direct request (not using make_request to handle binary response)
        headers = {
            'Authorization': f'Bearer {token}',
            'Accept': 'application/json'  # This might need to be different for binary files
        }
        
        # Make request to download file
        # Note: This endpoint might return binary data, so we need to handle it specially
        base_url = client.base_url
        url = f"{base_url}{endpoint}"
        
        logger.info(f"Making request to: {url}")
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            # Determine file extension based on content type or default to .pdf
            content_type = response.headers.get('Content-Type', 'application/octet-stream')
            
            if 'pdf' in content_type.lower():
                extension = '.pdf'
            elif 'json' in content_type.lower():
                extension = '.json'
            elif 'xml' in content_type.lower():
                extension = '.xml'
            elif 'jpeg' in content_type.lower() or 'jpg' in content_type.lower():
                extension = '.jpg'
            elif 'png' in content_type.lower():
                extension = '.png'
            else:
                extension = '.dat'  # Default extension
            
            # Create filename
            filename = f"report_{report_id}"
            if file_type is not None:
                filename += f"_type_{file_type}"
            if file_format is not None:
                filename += f"_format_{file_format}"
            filename += extension
            
            filepath = os.path.join(output_dir, filename)
            
            # Write the binary content to file
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"Successfully downloaded report file to: {filepath}")
            return True
        else:
            logger.warning(f"Failed to download report file for report {report_id}: {response.status_code}")
            logger.warning(f"Response: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error downloading report file for report {report_id}: {e}")
        return False


def get_customer_reports(client: EagleViewClient) -> List[Dict]:
    """
    Get all customer reports to identify available report IDs for download.
    
    Args:
        client: Authenticated EagleViewClient
        
    Returns:
        List of report dictionaries
    """
    try:
        # Get all customer reports to identify which ones we can download
        all_reports = client.get_all_customer_reports(save_to_csv=False)
        return all_reports
    except Exception as e:
        logger.error(f"Error getting customer reports: {e}")
        return []


def main():
    """Main function to download reports."""
    print("EagleView Reports Downloader")
    print("=" * 40)
    
    # Load configuration
    settings = EagleViewSettings.from_environment()
    if not settings.validate():
        print("❌ Please set the following environment variables:")
        print("   EAGLEVIEW_CLIENT_ID")
        print("   EAGLEVIEW_CLIENT_SECRET")
        return

    # Create client
    client = EagleViewClient(settings)
    
    # Get available reports
    print("\n1. Fetching available reports...")
    reports = get_customer_reports(client)
    
    if not reports:
        print("No reports found in your account.")
        print("Reports can only be downloaded after they are ordered using the Measurement Order API.")
        return
    
    print(f"Found {len(reports)} report(s) in your account")
    
    # Download reports
    print(f"\n2. Downloading reports...")
    download_count = 0
    
    for i, report in enumerate(reports):
        report_id = report.get('Id') or report.get('reportId')
        if report_id:
            logger.info(f"[{i+1}/{len(reports)}] Downloading report {report_id}")
            
            # Try to get file links first (this gives us the download URLs)
            file_links = get_report_file_links(client, report_id)
            
            if file_links:
                logger.info(f"  Found {len(file_links.get('Links', []))} file links for report {report_id}")
                
                # If we have specific file links, we could download them here
                # For now, let's try the GetReportFile endpoint
                success = download_report_file(client, report_id)
                if success:
                    download_count += 1
            else:
                # Try to download directly without specific file type/format
                success = download_report_file(client, report_id)
                if success:
                    download_count += 1
        else:
            logger.warning(f"Report {i+1} has no report ID")
    
    print(f"\n{'='*40}")
    print("PROCESS COMPLETED!")
    print(f"Downloaded {download_count} out of {len(reports)} reports")
    print("Files saved to data/reports/ directory")
    print("="*40)


if __name__ == "__main__":
    main()