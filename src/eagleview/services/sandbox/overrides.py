"""
Sandbox-specific service overrides for EagleView API client.
Contains sandbox-specific behavior for services.
"""

class SandboxPropertyDataServiceMixin:
    """Mixin for sandbox-specific property data service behavior."""
    
    def _validate_coordinates(self, coordinates):
        """Validate coordinates are within sandbox bounds."""
        if not self.client.settings.validate_coordinates:
            return coordinates
            
        bounds = self.client.settings.get_sandbox_bounds()
        validated_coords = []
        
        for i, coord in enumerate(coordinates):
            lat = coord['lat']
            lon = coord['lon']
            
            if not (bounds['min_lat'] <= lat <= bounds['max_lat']):
                raise ValueError(f"Coordinate {i} latitude {lat} outside sandbox bounds")
            if not (bounds['min_lon'] <= lon <= bounds['max_lon']):
                raise ValueError(f"Coordinate {i} longitude {lon} outside sandbox bounds")
                
            validated_coords.append(coord)
        
        return validated_coords

class SandboxImageryServiceMixin:
    """Mixin for sandbox-specific imagery service behavior."""
    
    def _apply_sandbox_restrictions(self, request_data):
        """Apply sandbox-specific restrictions to imagery requests."""
        # Limit radius in sandbox if needed
        if 'center' in request_data and 'radius_in_meters' in request_data['center']:
            # For demonstration purposes, limit to 100m in sandbox
            # This is just an example since the actual API might not have this constraint
            request_data['center']['radius_in_meters'] = min(
                request_data['center']['radius_in_meters'], 100
            )
        return request_data