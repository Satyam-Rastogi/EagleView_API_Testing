# Makefile for EagleView API Client

.PHONY: help install demo clean clean-images clean-data

help:
	@echo "EagleView API Client Makefile"
	@echo "============================"
	@echo "Available commands:"
	@echo "  make install     - Install dependencies (requires Python 3.12+)"
	@echo "  make demo        - Run the complete demo workflow"
	@echo "  make clean       - Clean all generated files"
	@echo "  make clean-images - Clean downloaded images"
	@echo "  make clean-data  - Clean JSON data files"

install:
	pip install -r requirements.txt

demo: fetch-data fetch-images download-images

fetch-data:
	python fetch_reports_client_credentials.py

fetch-images:
	python fetch_images_client_credentials.py

download-images:
	python download_images.py

clean: clean-images clean-data

clean-images:
	rm -rf downloaded_property_images/*
	rm -rf custom_location_images/*
	rm -rf address_based_images/*

clean-data:
	rm -f *.json
	rm -f *.log
	rm -f eagleview_client_credentials_tokens.json