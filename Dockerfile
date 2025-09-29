# EagleView API Client Dockerfile

# Use Python 3.12 slim image as base
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY scripts/requirements.txt scripts/requirements-dev.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Create data directory
RUN mkdir -p data/cache data/imagery data/requests data/reports data/results

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash eagleview
RUN chown -R eagleview:eagleview /app
USER eagleview

# Expose port for any web interface (if needed in future)
EXPOSE 8000

# Default command - show help
CMD ["python", "-m", "cli.eagleview", "--help"]