"""
EagleView API Client using Client Credentials Flow

This module provides a Python client for interacting with the EagleView API
using OAuth 2.0 Client Credentials flow for server-to-server authentication.
"""

import requests
import json
import time
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

class EagleViewAPIException(Exception):
    """Custom exception for EagleView API errors"""
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response

class EagleViewConfig:
    """Configuration for EagleView API client"""
    def __init__(self, client_id: str, client_secret: str, 
                 requests_per_second: float = 3, requests_per_minute: int = 50,
                 is_sandbox: bool = True):
        self.client_id = client_id
        self.client_secret = client_secret
        self.requests_per_second = requests_per_second
        self.requests_per_minute = requests_per_minute
        self.is_sandbox = is_sandbox
        
        # Set base URLs based on environment
        if is_sandbox:
            self.base_url = "https://sandbox.apicenter.eagleview.com"
            self.imagery_base_url = "https://sandbox.apis.eagleview.com"
        else:
            self.base_url = "https://apicenter.eagleview.com"
            self.imagery_base_url = "https://apis.eagleview.com"
            
        # Auth URL is always the same regardless of environment
        self.auth_url = "https://apicenter.eagleview.com/oauth2/v1/token"

class ClientCredentialsEagleViewClient:
    """EagleView API client using Client Credentials flow"""
    
    def __init__(self, config: EagleViewConfig):
        self.config = config
        self.access_token = None
        self.token_expires_at = None
        self.last_request_time = 0
        self.requests_this_minute = 0
        self.minute_start_time = time.time()
        
        # Try to load existing token
        self._load_token_from_file()
        
    def _load_token_from_file(self):
        """Load existing token from file if available"""
        try:
            if os.path.exists('eagleview_client_credentials_tokens.json'):
                with open('eagleview_client_credentials_tokens.json', 'r') as f:
                    token_data = json.load(f)
                    if token_data.get('client_id') == self.config.client_id:
                        self.access_token = token_data.get('access_token')
                        expires_str = token_data.get('token_expires_at')
                        if expires_str:
                            self.token_expires_at = datetime.fromisoformat(expires_str)
                        logger.info("Loaded existing token from file")
        except Exception as e:
            logger.warning(f"Could not load token from file: {e}")
    
    def _save_token_to_file(self, token_data: Dict):
        """Save token to file for reuse"""
        try:
            token_data['saved_at'] = datetime.now().isoformat()
            token_data['client_id'] = self.config.client_id
            token_data['auth_method'] = 'client_credentials'
            with open('eagleview_client_credentials_tokens.json', 'w') as f:
                json.dump(token_data, f, indent=2)
        except Exception as e:
            logger.warning(f"Could not save token to file: {e}")
    
    def _is_token_expired(self) -> bool:
        """Check if current token is expired or about to expire"""
        if not self.access_token or not self.token_expires_at:
            return True
        # Consider token expired if it expires in the next 5 minutes
        return datetime.now() >= (self.token_expires_at - timedelta(minutes=5))
    
    def _get_access_token(self) -> str:
        """Get access token using Client Credentials flow"""
        if not self._is_token_expired():
            return self.access_token
            
        logger.info("Getting new access token...")
        
        # Prepare token request with Basic Auth
        credentials = f"{self.config.client_id}:{self.config.client_secret}"
        encoded_credentials = credentials.encode('utf-8').hex()
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        
        # Add Basic Auth header
        import base64
        auth_string = f"{self.config.client_id}:{self.config.client_secret}"
        encoded_auth = base64.b64encode(auth_string.encode()).decode()
        headers['Authorization'] = f"Basic {encoded_auth}"
        
        data = {
            'grant_type': 'client_credentials',
            'scope': 'default'
        }
        
        try:
            response = requests.post(
                self.config.auth_url,
                headers=headers,
                data=data
            )
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data['access_token']
                expires_in = token_data.get('expires_in', 3600)  # Default to 1 hour
                self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
                
                # Save token for reuse
                self._save_token_to_file(token_data)
                
                logger.info(f"Successfully obtained access token. Expires at {self.token_expires_at}")
                return self.access_token
            else:
                raise EagleViewAPIException(
                    f"Failed to get access token: {response.status_code} - {response.text}",
                    status_code=response.status_code,
                    response=response.json() if response.content else None
                )
                
        except requests.RequestException as e:
            raise EagleViewAPIException(f"Network error while getting access token: {e}")
        except json.JSONDecodeError as e:
            raise EagleViewAPIException(f"Invalid JSON response: {e}")
    
    def _rate_limit(self):
        """Implement rate limiting"""
        current_time = time.time()
        
        # Reset minute counter if a minute has passed
        if current_time - self.minute_start_time >= 60:
            self.requests_this_minute = 0
            self.minute_start_time = current_time
        
        # Check minute limit
        if self.requests_this_minute >= self.config.requests_per_minute:
            sleep_time = 60 - (current_time - self.minute_start_time)
            if sleep_time > 0:
                logger.info(f"Minute rate limit reached. Sleeping for {sleep_time:.1f} seconds")
                time.sleep(sleep_time)
                self.requests_this_minute = 0
                self.minute_start_time = time.time()
        
        # Check per-second limit
        time_since_last_request = current_time - self.last_request_time
        min_interval = 1.0 / self.config.requests_per_second
        if time_since_last_request < min_interval:
            sleep_time = min_interval - time_since_last_request
            time.sleep(sleep_time)
        
        # Update rate limiting counters
        self.last_request_time = time.time()
        self.requests_this_minute += 1
    
    def _make_request(self, method: str, endpoint: str, use_imagery_base: bool = False, retry_count: int = 3, **kwargs) -> requests.Response:
        """Make authenticated request to EagleView API with retry logic"""
        # Apply rate limiting
        self._rate_limit()
        
        # Get access token
        token = self._get_access_token()
        
        # Prepare headers
        headers = {
            'Authorization': f'Bearer {token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        # Merge headers
        if 'headers' in kwargs:
            headers.update(kwargs['headers'])
        kwargs['headers'] = headers
        
        # Make request
        base_url = self.config.imagery_base_url if use_imagery_base else self.config.base_url
        url = f"{base_url}{endpoint}"
        logger.debug(f"Making {method} request to {url}")
        
        for attempt in range(retry_count):
            try:
                response = requests.request(method, url, **kwargs)
                
                # Handle common error responses
                if response.status_code == 401:
                    # Token might be expired, clear it and try once more
                    self.access_token = None
                    self.token_expires_at = None
                    token = self._get_access_token()
                    kwargs['headers']['Authorization'] = f'Bearer {token}'
                    response = requests.request(method, url, **kwargs)
                
                # If we get a successful response, return it
                if response.ok:
                    return response
                
                # If we get a 404, it might be that the endpoint doesn't exist
                if response.status_code == 404:
                    logger.warning(f"Endpoint {url} not found (404)")
                    return response
                    
                # For other errors, log and potentially retry
                logger.warning(f"Attempt {attempt + 1}/{retry_count} failed with status {response.status_code}")
                if attempt < retry_count - 1:  # Don't sleep on the last attempt
                    time.sleep(2 ** attempt)  # Exponential backoff
                    
            except requests.RequestException as e:
                logger.warning(f"Attempt {attempt + 1}/{retry_count} failed with network error: {e}")
                if attempt < retry_count - 1:  # Don't sleep on the last attempt
                    time.sleep(2 ** attempt)  # Exponential backoff
                if attempt == retry_count - 1:  # Last attempt
                    raise EagleViewAPIException(f"Network error after {retry_count} attempts: {e}")
        
        # If we get here, all retries failed
        raise EagleViewAPIException(
            f"API request failed after {retry_count} attempts: {response.status_code} - {response.text}",
            status_code=response.status_code,
            response=response.json() if response.content else None
        )

    def get_available_products(self) -> List[Dict]:
        """Get list of available products"""
        try:
            # Based on the API documentation, the correct endpoint is /GetAvailableProducts
            endpoint = '/GetAvailableProducts'
            response = self._make_request('GET', endpoint)
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"Products endpoint {endpoint} returned status {response.status_code}")
                logger.warning(f"Response: {response.text}")
                return []
        except Exception as e:
            logger.error(f"Error getting available products: {e}")
            # Return empty list instead of failing completely
            return []

    def get_all_customer_reports(self, save_to_csv: bool = True) -> List[Dict]:
        """Get all reports for the customer"""
        try:
            # Based on the API documentation, the correct endpoint is /v3/Report/GetReports
            # This requires a POST request with pagination parameters
            endpoint = '/v3/Report/GetReports'
            
            # First, we need to get reports with pagination
            page = 1
            count = 100  # Number of reports per page
            all_reports = []
            
            while True:
                # Prepare the request body for pagination
                body = {
                    "productsToFiterBy": [],  # Empty array to get all products
                    "statusesToFilterBy": "",
                    "sortBy": "",
                    "sortAscending": True,
                    "subStatusToFilterBy": "",
                    "fieldsToFilterBy": [],
                    "textToFilterBy": "",
                    "referenceId": "",
                    "emailCC": "",
                    "fromDate": "",
                    "toDate": ""
                }
                
                response = self._make_request('POST', f"{endpoint}?page={page}&count={count}", json=body)
                
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, list) and len(data) > 0:
                        # Extract reports from the response
                        reports_data = data[0] if len(data) > 0 else {}
                        report_list = reports_data.get('ReportList', [])
                        total_reports = reports_data.get('TotalOfReports', 0)
                        
                        if report_list:
                            # If report_list is a list of reports, extend all_reports
                            if isinstance(report_list, list):
                                all_reports.extend(report_list)
                            # If report_list is a single report object, append it
                            else:
                                all_reports.append(report_list)
                        
                        # Check if we've got all reports
                        if len(all_reports) >= total_reports or len(report_list) < count:
                            break
                        else:
                            page += 1
                    else:
                        break
                else:
                    logger.warning(f"Reports endpoint {endpoint} returned status {response.status_code}")
                    logger.warning(f"Response: {response.text}")
                    break
            
            if save_to_csv:
                self._save_reports_to_csv(all_reports)
            
            return all_reports
        except Exception as e:
            logger.error(f"Error getting customer reports: {e}")
            return []

    def _save_reports_to_csv(self, reports: List[Dict], filename: Optional[str] = None):
        """Save reports to CSV file"""
        if not reports:
            return
            
        if filename is None:
            filename = f"eagleview_reports_client_credentials_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        try:
            import csv
            
            # Get all possible field names
            fieldnames = set()
            for report in reports:
                fieldnames.update(report.keys())
            fieldnames = sorted(list(fieldnames))
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for report in reports:
                    writer.writerow(report)
            
            logger.info(f"Reports saved to CSV: {filename}")
        except Exception as e:
            logger.error(f"Error saving reports to CSV: {e}")

    def get_report_file_links(self, report_id: str) -> List[Dict]:
        """Get file links for a specific report"""
        try:
            # Based on the API documentation, the correct endpoint is /v3/Report/{reportId}/file-links
            endpoint = f'/v3/Report/{report_id}/file-links'
            response = self._make_request('GET', endpoint)
            if response.status_code == 200:
                data = response.json()
                # Extract links from the response
                if isinstance(data, list) and len(data) > 0:
                    return data[0].get('Links', []) if 'Links' in data[0] else []
                return []
            else:
                logger.warning(f"File links endpoint {endpoint} returned status {response.status_code}")
                logger.warning(f"Response: {response.text}")
                return []
        except Exception as e:
            logger.error(f"Error getting file links for report {report_id}: {e}")
            return []

    def download_report_file(self, report_id: str, file_type: str, file_format: str) -> bytes:
        """Download a specific file for a report"""
        try:
            # Based on the API documentation, the correct endpoint is /v1/File/GetReportFile
            endpoint = f'/v1/File/GetReportFile?reportId={report_id}&fileType={file_type}&fileFormat={file_format}'
            response = self._make_request('GET', endpoint)
            if response.status_code == 200:
                return response.content
            else:
                logger.warning(f"Download endpoint {endpoint} returned status {response.status_code}")
                logger.warning(f"Response: {response.text}")
                return b''
        except Exception as e:
            logger.error(f"Error downloading file for report {report_id}: {e}")
            return b''

    def get_report_detail(self, report_id: int) -> Dict:
        """Get detailed information for a specific report"""
        try:
            endpoint = f'/v3/Report/GetReport?reportId={report_id}'
            response = self._make_request('GET', endpoint)
            if response.status_code == 200:
                data = response.json()
                # Return the first item if it's a list
                if isinstance(data, list) and len(data) > 0:
                    return data[0]
                return data
            else:
                logger.warning(f"Report detail endpoint {endpoint} returned status {response.status_code}")
                logger.warning(f"Response: {response.text}")
                return {}
        except Exception as e:
            logger.error(f"Error getting report detail for report {report_id}: {e}")
            return {}

    def get_imagery_for_location(self, location_data: Dict) -> Dict:
        """Get imagery for a specific location using the Imagery API"""
        try:
            endpoint = '/imagery/v3/discovery/rank/location'
            response = self._make_request('POST', endpoint, use_imagery_base=True, json=location_data)
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"Imagery endpoint {endpoint} returned status {response.status_code}")
                logger.warning(f"Response: {response.text}")
                return {}
        except Exception as e:
            logger.error(f"Error getting imagery for location: {e}")
            return {}

    def request_property_data_by_coordinates(self, lat: float, lon: float) -> Dict:
        """Request property data using coordinates within the sandbox area
        
        Args:
            lat (float): Latitude within the sandbox bounding box
            lon (float): Longitude within the sandbox bounding box
            
        Returns:
            Dict: Request response with request ID and status
        """
        try:
            endpoint = '/property/v2/request'
            request_data = {
                "coordinates": {
                    "lat": lat,
                    "lon": lon
                }
            }
            response = self._make_request('POST', endpoint, use_imagery_base=True, json=request_data)
            if response.status_code == 202:
                return response.json()
            else:
                logger.warning(f"Property data endpoint {endpoint} returned status {response.status_code}")
                logger.warning(f"Response: {response.text}")
                return {}
        except Exception as e:
            logger.error(f"Error requesting property data: {e}")
            return {}

    def request_property_data_by_address(self, address: str) -> Dict:
        """Request property data using a complete address
        
        Args:
            address (str): Complete address string
            
        Returns:
            Dict: Request response with request ID and status
        """
        try:
            endpoint = '/property/v2/request'
            request_data = {
                "address": {
                    "completeAddress": address
                }
            }
            response = self._make_request('POST', endpoint, use_imagery_base=True, json=request_data)
            if response.status_code == 202:
                return response.json()
            else:
                logger.warning(f"Property data endpoint {endpoint} returned status {response.status_code}")
                logger.warning(f"Response: {response.text}")
                return {}
        except Exception as e:
            logger.error(f"Error requesting property data: {e}")
            return {}

    def get_property_data_result(self, request_id: str) -> Dict:
        """Get the result of a property data request
        
        Args:
            request_id (str): Request ID returned from request_property_data
            
        Returns:
            Dict: Property data result or status
        """
        try:
            endpoint = f'/property/v2/result/{request_id}'
            response = self._make_request('GET', endpoint, use_imagery_base=True)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 202:
                # Still processing
                return response.json()
            else:
                logger.warning(f"Property data result endpoint {endpoint} returned status {response.status_code}")
                logger.warning(f"Response: {response.text}")
                return {}
        except Exception as e:
            logger.error(f"Error getting property data result: {e}")
            return {}