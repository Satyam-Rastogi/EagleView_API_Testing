"""
Demo Execution Script
"""

import os

def show_demo_commands():
    """Show the commands to run the demo"""
    print("EAGLEVIEW API CLIENT DEMO COMMANDS")
    print("=" * 40)
    print()
    print("To run the complete demo workflow:")
    print()
    print("1. First, make sure you have the required dependencies:")
    print("   pip install requests")
    print()
    print("2. Update the client credentials in each Python file:")
    print("   - client_credentials_eagleview.py")
    print("   - fetch_reports_client_credentials.py")
    print("   - fetch_images_client_credentials.py")
    print("   - download_images.py")
    print()
    print("3. Run the property data requests:")
    print("   python fetch_reports_client_credentials.py")
    print()
    print("4. Run the imagery data requests:")
    print("   python fetch_images_client_credentials.py")
    print()
    print("5. Download actual property images:")
    print("   python download_images.py")
    print()
    print("6. Check the output files:")
    print("   - JSON files with API responses")
    print("   - Downloaded images in the 'downloaded_property_images' directory")
    print()

def show_file_structure():
    """Show the demo file structure"""
    print("DEMO FILE STRUCTURE")
    print("=" * 20)
    print()
    
    files = [
        "client_credentials_eagleview.py",
        "fetch_reports_client_credentials.py", 
        "fetch_images_client_credentials.py",
        "download_images.py",
        "README.md",
        "demo_overview.py",
        "eagleview_property_data_requests_*.json",
        "additional_property_data_requests_*.json",
        "property_data_result_*.json",
        "eagleview_imagery_summary_*.json",
        "imagery_data_*.json",
        "eagleview_client_credentials_tokens.json",
        "downloaded_property_images/"
    ]
    
    for file in files:
        print(f"  {file}")
    print()

if __name__ == "__main__":
    show_demo_commands()
    print()
    show_file_structure()