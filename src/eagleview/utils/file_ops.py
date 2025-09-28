"""
File operations utilities for EagleView API client.
Handles file I/O, directory management, and path resolution.

This module provides utility functions for common file operations including
JSON data handling, directory creation, and path resolution. It also includes
a standardized logging setup function.
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

def ensure_directory_exists(directory: str) -> bool:
    """Ensure a directory exists, creating it if necessary.
    
    This function creates a directory and any necessary parent directories
    if they don't already exist.
    
    Args:
        directory: Path to the directory to ensure exists
        
    Returns:
        True if directory exists or was created successfully, False otherwise
    """
    try:
        Path(directory).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Error creating directory {directory}: {e}")
        return False

def save_json_data(data: Dict[Any, Any], filepath: str, create_dirs: bool = True) -> bool:
    """Save data to a JSON file with proper error handling.
    
    This function saves data to a JSON file with proper error handling and
    optional directory creation.
    
    Args:
        data: Data to save to the JSON file
        filepath: Path to the JSON file
        create_dirs: Whether to create parent directories if they don't exist
        
    Returns:
        True if save was successful, False otherwise
    """
    try:
        if create_dirs:
            ensure_directory_exists(os.path.dirname(filepath))
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        logger.info(f"Data saved to: {filepath}")
        return True
    except Exception as e:
        logger.error(f"Error saving data to {filepath}: {e}")
        return False

def load_json_data(filepath: str) -> Optional[Dict[Any, Any]]:
    """Load data from a JSON file with proper error handling.
    
    This function loads data from a JSON file with proper error handling for
    common issues like missing files or invalid JSON.
    
    Args:
        filepath: Path to the JSON file to load
        
    Returns:
        Dictionary containing the loaded data, or None if loading failed
    """
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning(f"File not found: {filepath}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {filepath}: {e}")
        return None
    except Exception as e:
        logger.error(f"Error loading {filepath}: {e}")
        return None

def generate_timestamped_filename(prefix: str, extension: str = ".json") -> str:
    """Generate a timestamped filename.
    
    This function generates a filename with a timestamp prefix, useful for
    creating unique filenames for data exports.
    
    Args:
        prefix: Prefix for the filename
        extension: File extension (default: ".json")
        
    Returns:
        Timestamped filename string
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{prefix}_{timestamp}{extension}"

def resolve_project_path(relative_path: str) -> str:
    """Resolve a path relative to the project root.
    
    This function resolves a relative path to an absolute path based on the
    project root directory.
    
    Args:
        relative_path: Path relative to the project root
        
    Returns:
        Absolute path string
    """
    # Get the project root (assuming this file is in src/core)
    project_root = Path(__file__).parent.parent.parent
    return str(project_root / relative_path)

def get_data_directory(subdirectory: str = "") -> str:
    """Get the full path to a data subdirectory.
    
    This function returns the full path to a data subdirectory, creating the
    data directory if it doesn't exist.
    
    Args:
        subdirectory: Subdirectory within the data directory (optional)
        
    Returns:
        Full path to the data subdirectory
    """
    # Go up 3 levels from src/eagleview/utils to get to the project root
    project_root = Path(__file__).parent.parent.parent.parent
    if subdirectory:
        return str(project_root / "data" / subdirectory)
    return str(project_root / "data")

def setup_logging(name: str, level: str = "INFO") -> logging.Logger:
    """Set up standardized logging for a module.
    
    This function sets up standardized logging with both console and file
    handlers, using a consistent format across the application.
    
    Args:
        name: Logger name (typically __name__)
        level: Logging level (default: "INFO")
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Prevent adding multiple handlers
    if not logger.handlers:
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File handler - ensure logs go to logs directory
        logs_dir = "logs"
        os.makedirs(logs_dir, exist_ok=True)  # Create logs directory if it doesn't exist
        log_file = os.path.join(logs_dir, f"{name.lower()}_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger