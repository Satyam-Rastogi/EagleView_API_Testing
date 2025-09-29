# Makefile for EagleView API Client

# Variables
PYTHON := python3
PIP := pip
VENV := eagleview_env
VENV_BIN := $(VENV)/bin
ACTIVATE := source $(VENV_BIN)/activate

# Default target
.PHONY: help
help:
	@echo "EagleView API Client Makefile"
	@echo ""
	@echo "Usage:"
	@echo "  make setup           - Setup the development environment"
	@echo "  make install         - Install dependencies"
	@echo "  make install-dev     - Install development dependencies"
	@echo "  make run-help        - Show CLI help"
	@echo "  make run-demo        - Run demo"
	@echo "  make run-property    - Run property data requests"
	@echo "  make run-imagery     - Run imagery requests"
	@echo "  make test            - Run tests (if available)"
	@echo "  make clean           - Clean build artifacts"
	@echo "  make docker-build    - Build Docker image"
	@echo "  make docker-run      - Run Docker container"
	@echo "  make docker-demo     - Run demo in Docker"
	@echo "  make docker-dev      - Run development shell in Docker"

# Setup virtual environment
.PHONY: setup
setup:
	$(PYTHON) -m venv $(VENV)
	$(VENV_BIN)/pip install --upgrade pip
	$(VENV_BIN)/pip install -r scripts/requirements.txt

# Install dependencies
.PHONY: install
install:
	$(ACTIVATE) && $(PIP) install -r scripts/requirements.txt

# Install development dependencies
.PHONY: install-dev
install-dev:
	$(ACTIVATE) && $(PIP) install -r scripts/requirements-dev.txt

# Run CLI help
.PHONY: run-help
run-help:
	$(ACTIVATE) && $(PYTHON) -m cli.eagleview --help

# Run demo
.PHONY: run-demo
run-demo:
	$(ACTIVATE) && $(PYTHON) -m cli.eagleview --operation demo

# Run property data requests
.PHONY: run-property
run-property:
	$(ACTIVATE) && $(PYTHON) -m cli.eagleview --operation property-data

# Run imagery requests
.PHONY: run-imagery
run-imagery:
	$(ACTIVATE) && $(PYTHON) -m cli.eagleview --operation imagery

# Run tests (placeholder)
.PHONY: test
test:
	$(ACTIVATE) && $(PYTHON) -m pytest tests/ || echo "No tests found or pytest not installed"

# Clean build artifacts
.PHONY: clean
clean:
	rm -rf $(VENV)
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

# Docker commands
.PHONY: docker-build
docker-build:
	docker build -t eagleview-client .

.PHONY: docker-run
docker-run:
	docker run -it --rm \
		-v $(PWD)/data:/app/data \
		-v $(PWD)/config:/app/config \
		-v $(PWD)/.env:/app/.env \
		--env-file .env \
		eagleview-client

.PHONY: docker-demo
docker-demo:
	docker run -it --rm \\\n\t\t-v $(PWD)/data:/app/data \\\n\t\t-v $(PWD)/config:/app/config \\\n\t\t-v $(PWD)/.env:/app/.env \\\n\t\t--env-file .env \\\n\t\teagleview-client python -m cli.eagleview --operation demo

.PHONY: docker-dev
docker-dev:
	docker run -it --rm \
		-v $(PWD):/app \
		-v $(PWD)/data:/app/data \
		-v $(PWD)/config:/app/config \
		-v $(PWD)/.env:/app/.env \
		--env-file .env \
		eagleview-client /bin/bash