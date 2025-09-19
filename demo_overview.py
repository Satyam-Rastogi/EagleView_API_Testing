"""
Demo Script for EagleView API Client
"""

import os
import json

def demo_overview():
    """Show an overview of the demo files"""
    print("=" * 60)
    print("EAGLEVIEW API CLIENT DEMO")
    print("=" * 60)
    print()
    print("This demo shows a complete working example of the EagleView API client.")
    print("The client demonstrates:")
    print("1. OAuth 2.0 Client Credentials authentication")
    print("2. Property data requests for locations in the sandbox area")
    print("3. Imagery data requests for properties")
    print("4. Downloading actual property images")
    print()
    print("Sandbox Area (Omaha, Nebraska):")
    print("  Latitude:  41.24140396772262 to 41.25672882015283")
    print("  Longitude: -96.00532698173473 to -95.97589954958912")
    print()

def show_core_files():
    """Show the core implementation files"""
    print("CORE IMPLEMENTATION FILES")
    print("-" * 30)
    print("1. client_credentials_eagleview.py - Main client library")
    print("2. fetch_reports_client_credentials.py - Property data requests")
    print("3. fetch_images_client_credentials.py - Imagery data requests")
    print("4. download_images.py - Image downloading utility")
    print()

def show_sample_outputs():
    """Show sample output files"""
    print("SAMPLE OUTPUT FILES")
    print("-" * 25)
    
    # Show property data request
    if os.path.exists("eagleview_property_data_requests_20250920_022800.json"):
        with open("eagleview_property_data_requests_20250920_022800.json", "r") as f:
            data = json.load(f)
        print(f"Property data requests: {len(data)} requests")
        print("  Sample request ID:", data[0]["request"]["id"])
        print()
    
    # Show property data result
    if os.path.exists("property_data_result_dce2f233-b84a-4b0d-880b-1bded5ede99a.json"):
        with open("property_data_result_dce2f233-b84a-4b0d-880b-1bded5ede99a.json", "r") as f:
            data = json.load(f)
        address = data.get("response_address", {}).get("full_address", "Unknown")
        print(f"Property data result:")
        print(f"  Address: {address}")
        print(f"  Roof material: {data['structures'][0]['roof']['structure_roof_material_primary']['value']}")
        print(f"  Roof condition: {data['structures'][0]['roof']['structure_roof_condition_rating']['value']}")
        print()
    
    # Show imagery data
    if os.path.exists("eagleview_imagery_summary_20250920_022819.json"):
        with open("eagleview_imagery_summary_20250920_022819.json", "r") as f:
            data = json.load(f)
        print(f"Imagery requests: {len(data)} locations")
        print(f"  Sample captures: {data[0]['captures']}")
        print()
    
    # Show downloaded images
    if os.path.exists("downloaded_property_images"):
        images = os.listdir("downloaded_property_images")
        print(f"Downloaded images: {len(images)} files")
        if images:
            print(f"  Sample image: {images[0]}")
        print()

def demo_workflow():
    """Explain the demo workflow"""
    print("DEMO WORKFLOW")
    print("-" * 15)
    print("1. Authentication: Client automatically handles OAuth 2.0 authentication")
    print("2. Property Data: Request property information for locations in sandbox area")
    print("3. Imagery Data: Request imagery information for properties")
    print("4. Image Download: Download actual property images using image tokens")
    print()
    print("To run the demo:")
    print("  python fetch_reports_client_credentials.py")
    print("  python fetch_images_client_credentials.py")
    print("  python download_images.py")
    print()

def main():
    """Main demo function"""
    demo_overview()
    show_core_files()
    show_sample_outputs()
    demo_workflow()
    
    print("=" * 60)
    print("DEMO READY - All files are in the eagleview_demo directory")
    print("=" * 60)

if __name__ == "__main__":
    main()