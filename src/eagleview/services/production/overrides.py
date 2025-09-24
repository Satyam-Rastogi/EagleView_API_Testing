"""
Production-specific service overrides for EagleView API client.
Contains production-specific optimizations for services.
"""

class ProductionPropertyDataServiceMixin:
    """Mixin for production-specific property data service behavior."""
    
    def _validate_coordinates(self, coordinates):
        """In production, coordinates validation may be different or skipped."""
        # Production might have different validation rules
        # For now, just return coordinates as-is
        validated_coords = []
        for i, coord in enumerate(coordinates):
            lat = coord['lat']
            lon = coord['lon']
            
            # Basic validation for valid coordinate ranges
            if not (-90 <= lat <= 90):
                raise ValueError(f"Coordinate {i} latitude {lat} is out of range (-90 to 90)")
            if not (-180 <= lon <= 180):
                raise ValueError(f"Coordinate {i} longitude {lon} is out of range (-180 to 180)")
                
            validated_coords.append(coord)
        
        return validated_coords

class ProductionImageryServiceMixin:
    """Mixin for production-specific imagery service behavior."""
    
    def _apply_production_optimizations(self, request_data):
        """Apply production-specific optimizations to imagery requests."""
        # Production might have different optimization strategies
        # For now, just return as-is
        return request_data