"""
Fetch and Download EagleView Reports

This script demonstrates how to fetch all measurement/order reports for a customer using 
OAuth 2.0 Client Credentials flow and download the associated report files.

Usage:
1. Update the configuration with your actual client credentials
2. Run the script: python fetch_and_download_reports.py
"""

import json
import logging
import sys
import os
from datetime import datetime
from typing import List, Dict

# Add parent directory to path to import client_credentials_eagleview
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from client_credentials_eagleview import ClientCredentialsEagleViewClient, EagleViewConfig, EagleViewAPIException

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fetch_and_download_reports.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def fetch_and_download_reports():
    """Fetch all reports and download associated files"""
    
    # Initialize configuration with your credentials
    config = EagleViewConfig(
        client_id="0oa16yo11pa57TLPa2p8",
        client_secret="BAfJ05yNlGaNt8Gm3gnO_0ekJ1DRlwJsaNgU4aePS9o5iCuxyOuZL1kmxxHionD7",
        # Conservative rate limits to be respectful
        requests_per_second=3,
        requests_per_minute=50,
        is_sandbox=True  # Set to False for production
    )
    
    try:
        # Create client credentials client
        logger.info("Initializing Client Credentials client...")
        client = ClientCredentialsEagleViewClient(config)
        
        # Test authentication
        logger.info("Testing authentication...")
        token = client._get_access_token()
        logger.info("Authentication successful!")
        
        # Fetch all reports
        logger.info("Fetching all customer reports...")
        reports = client.get_all_customer_reports(save_to_csv=True)
        
        if not reports:
            logger.info("No reports found for this customer")
            return []
        
        logger.info(f"Found {len(reports)} reports. Processing each report...")
        
        # Create directory for downloaded reports
        reports_dir = "downloaded_reports"
        os.makedirs(reports_dir, exist_ok=True)
        logger.info(f"Created directory for reports: {reports_dir}")
        
        # Track downloaded files
        downloaded_files = []
        
        # Process each report
        for i, report in enumerate(reports):
            report_id = report.get('Id') or report.get('ReportId')
            if not report_id:
                logger.warning(f"Skipping report at index {i} - no report ID found")
                continue
                
            logger.info(f"Processing report {report_id} ({i+1}/{len(reports)})")
            
            try:
                # Get detailed report information
                logger.info(f"  Getting detailed information for report {report_id}")
                report_detail = client.get_report_detail(report_id)
                
                if report_detail:
                    # Save report detail to JSON
                    detail_filename = f"{reports_dir}/report_{report_id}_detail.json"
                    with open(detail_filename, 'w') as f:
                        json.dump(report_detail, f, indent=2, default=str)
                    logger.info(f"    Saved report detail to: {detail_filename}")
                    
                    # Check if there's a download link in the report detail
                    download_link = report_detail.get('ReportDownloadLink')
                    if download_link:
                        logger.info(f"    Found PDF download link for report {report_id}")
                        # Download the PDF report
                        try:
                            # Make a direct HTTP request to download the file
                            import requests
                            headers = {'Authorization': f'Bearer {token}'}
                            response = requests.get(download_link, headers=headers)
                            
                            if response.status_code == 200:
                                # Determine file extension from content type or default to .pdf
                                content_type = response.headers.get('Content-Type', '').lower()
                                if 'pdf' in content_type:
                                    extension = '.pdf'
                                else:
                                    extension = '.pdf'  # Default to PDF
                                
                                pdf_filename = f"{reports_dir}/report_{report_id}{extension}"
                                with open(pdf_filename, 'wb') as f:
                                    f.write(response.content)
                                logger.info(f"    ✓ Downloaded PDF report: {pdf_filename}")
                                downloaded_files.append({
                                    'report_id': report_id,
                                    'file_type': 'PDF',
                                    'filename': pdf_filename,
                                    'size_bytes': len(response.content)
                                })
                            else:
                                logger.warning(f"    Failed to download PDF for report {report_id}: {response.status_code}")
                        except Exception as e:
                            logger.warning(f"    Error downloading PDF for report {report_id}: {e}")
                    else:
                        logger.info(f"    No direct download link found in report detail")
                    
                    # Get file links for the report
                    logger.info(f"  Getting file links for report {report_id}")
                    file_links = client.get_report_file_links(report_id)
                    
                    if file_links and isinstance(file_links, list) and len(file_links) > 0:
                        logger.info(f"    Found {len(file_links)} file links for report {report_id}")
                        
                        # Download each file
                        for j, file_link in enumerate(file_links):
                            link = file_link.get('Link')
                            file_type = file_link.get('FileType')
                            expire_timestamp = file_link.get('ExpireTimestamp')
                            
                            if link and file_type:
                                logger.info(f"    Downloading file type {file_type}")
                                
                                try:
                                    # Download the file using the direct link
                                    import requests
                                    headers = {'Authorization': f'Bearer {token}'}
                                    response = requests.get(link, headers=headers)
                                    
                                    if response.status_code == 200:
                                        # Determine file extension based on content type or file type
                                        content_type = response.headers.get('Content-Type', '')
                                        if 'pdf' in content_type:
                                            extension = ".pdf"
                                        elif 'zip' in content_type:
                                            extension = ".zip"
                                        elif 'jpeg' in content_type or 'jpg' in content_type:
                                            extension = ".jpg"
                                        elif 'png' in content_type:
                                            extension = ".png"
                                        else:
                                            # Default based on file type
                                            extension = ".pdf" if file_type == "PDF" else ".zip" if file_type == "ZIP" else ".dat"
                                        
                                        # Create filename
                                        filename = f"{reports_dir}/report_{report_id}_file_{j+1}_{file_type}{extension}"
                                        
                                        # Save file
                                        with open(filename, 'wb') as f:
                                            f.write(response.content)
                                        
                                        logger.info(f"      ✓ Saved file: {filename}")
                                        downloaded_files.append({
                                            'report_id': report_id,
                                            'file_type': file_type,
                                            'expire_timestamp': expire_timestamp,
                                            'filename': filename,
                                            'size_bytes': len(response.content)
                                        })
                                    else:
                                        logger.warning(f"      Failed to download file: {response.status_code} - {response.text}")
                                        
                                except Exception as e:
                                    logger.warning(f"      Failed to download file: {e}")
                            else:
                                logger.warning(f"    Invalid file link data for report {report_id}")
                    else:
                        logger.info(f"    No file links found for report {report_id}")
                else:
                    logger.warning(f"  Failed to get detailed information for report {report_id}")
                    
            except EagleViewAPIException as e:
                logger.warning(f"  Failed to process report {report_id}: {e}")
            except Exception as e:
                logger.warning(f"  Unexpected error processing report {report_id}: {e}")
            
            # Add a small delay to be respectful
            import time
            time.sleep(0.5)
        
        # Save download summary to JSON
        if downloaded_files:
            summary_filename = f"downloaded_reports_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(summary_filename, 'w') as f:
                json.dump(downloaded_files, f, indent=2, default=str)
            logger.info(f"Download summary saved to: {summary_filename}")
        
        return downloaded_files
        
    except EagleViewAPIException as e:
        logger.error(f"API Error: {e}")
        if hasattr(e, 'status_code'):
            logger.error(f"  Status Code: {e.status_code}")
        if hasattr(e, 'response') and e.response:
            logger.error(f"  Response: {json.dumps(e.response, indent=2)}")
        return []
        
    except Exception as e:
        logger.error(f"Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        return []

def display_download_summary(downloaded_files: List[Dict]) -> None:
    """Display a formatted summary of downloaded files
    
    Args:
        downloaded_files (List[Dict]): List of downloaded file information
    """
    if not downloaded_files:
        print("No files downloaded")
        return
        
    print("\n" + "="*80)
    print("DOWNLOAD SUMMARY")
    print("="*80)
    
    # Headers
    print(f"{'Report ID':<15} {'File Type':<15} {'Size (KB)':<12} {'Filename':<30}")
    print("-"*80)
    
    # Display downloaded files
    for file_info in downloaded_files:
        report_id = file_info.get('report_id', 'N/A')
        file_type = file_info.get('file_type', 'Unknown')[:14]  # Truncate if too long
        size_kb = file_info.get('size_bytes', 0) // 1024
        filename = os.path.basename(file_info.get('filename', ''))[:29]  # Truncate if too long
        
        print(f"{report_id:<15} {file_type:<15} {size_kb:<12} {filename:<30}")
        
    print("="*80)

def main():
    """Main function"""
    print("EagleView Reports Fetcher and Downloader (Client Credentials)")
    print("=" * 70)
    print("NO BROWSER REQUIRED - Fully Automated!")
    print("Using OAuth 2.0 Client Credentials Flow")
    print("Perfect for server-to-server communication")
    print()
    
    # Check if credentials are properly configured
    client_id = "0oa16yo11pa57TLPa2p8"
    client_secret = "BAfJ05yNlGaNt8Gm3gnO_0ekJ1DRlwJsaNgU4aePS9o5iCuxyOuZL1kmxxHionD7"
    
    # Validate credentials
    if not client_id or not client_secret:
        print("❌ Please update the client credentials in the script!")
        print("💡 Look for 'YOUR_CLIENT_ID_HERE' and 'YOUR_CLIENT_SECRET_HERE' in the code")
        return
    
    downloaded_files = fetch_and_download_reports()
    
    if downloaded_files:
        display_download_summary(downloaded_files)
        print("\n" + "="*70)
        print("PROCESS COMPLETED SUCCESSFULLY!")
        print(f"Downloaded {len(downloaded_files)} files")
        print("Files saved to 'downloaded_reports' directory")
        print("="*70)
    else:
        print("\n" + "="*70)
        print("PROCESS COMPLETED WITH NO FILES DOWNLOADED")
        print("This might be because:")
        print("   - No reports were found for this customer")
        print("   - Reports don't have downloadable files")
        print("   - Check the log file for details")
        print("="*70)

if __name__ == "__main__":
    main()