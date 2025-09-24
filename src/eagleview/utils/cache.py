"""
Data caching utilities for EagleView API client.
Provides caching mechanisms to reduce API calls and improve performance.
"""

import os
import json
import time
import hashlib
import logging
from typing import Any, Dict, Optional
from functools import wraps
from .file_ops import get_data_directory, ensure_directory_exists

logger = logging.getLogger(__name__)

def get_cache_directory() -> str:
    """Get the cache directory path."""
    cache_dir = get_data_directory("cache")
    ensure_directory_exists(cache_dir)
    return cache_dir

def generate_cache_key(func_name: str, *args, **kwargs) -> str:
    """Generate a cache key based on function name and arguments."""
    # Create a string representation of args and kwargs
    args_str = str(args)
    kwargs_str = str(sorted(kwargs.items()))
    combined = f"{func_name}:{args_str}:{kwargs_str}"
    
    # Generate MD5 hash
    return hashlib.md5(combined.encode()).hexdigest()

def cache_result(ttl_seconds: int = 3600):
    """Decorator to cache function results.
    
    Args:
        ttl_seconds: Time to live for cached results in seconds (default: 1 hour)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = generate_cache_key(func.__name__, *args, **kwargs)
            cache_file = os.path.join(get_cache_directory(), f"{cache_key}.json")
            
            # Check if cached result exists and is still valid
            if os.path.exists(cache_file):
                try:
                    with open(cache_file, 'r') as f:
                        cached_data = json.load(f)
                    
                    # Check if cache is still valid
                    if time.time() - cached_data['timestamp'] < ttl_seconds:
                        logger.info(f"Returning cached result for {func.__name__}")
                        return cached_data['result']
                    else:
                        logger.info(f"Cache expired for {func.__name__}, fetching fresh data")
                except Exception as e:
                    logger.warning(f"Error reading cache file {cache_file}: {e}")
            
            # Call the function and cache the result
            result = func(*args, **kwargs)
            
            # Save result to cache
            try:
                cache_data = {
                    'timestamp': time.time(),
                    'result': result,
                    'function': func.__name__,
                    'args': str(args),
                    'kwargs': str(kwargs)
                }
                with open(cache_file, 'w') as f:
                    json.dump(cache_data, f, indent=2, default=str)
                logger.info(f"Cached result for {func.__name__}")
            except Exception as e:
                logger.warning(f"Error writing cache file {cache_file}: {e}")
            
            return result
        return wrapper
    return decorator

def clear_cache():
    """Clear all cached data."""
    cache_dir = get_cache_directory()
    if os.path.exists(cache_dir):
        import shutil
        shutil.rmtree(cache_dir)
        ensure_directory_exists(cache_dir)
        logger.info("Cache cleared")