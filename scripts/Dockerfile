# Dockerfile for EagleView API Client

FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all Python files
COPY *.py ./

# Create directories for output files
RUN mkdir -p downloaded_property_images eagleview_images

# Expose port (if needed for future web interface)
EXPOSE 8000

# Command to run the demo overview
CMD ["python", "demo_overview.py"]