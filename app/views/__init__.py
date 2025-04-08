# This file should not import from app.routes
# The routes will import from views, not the other way around

# Views module initialization
# Export view functions
from app.views.views import get_data, upload_csv, update_record

__all__ = ['get_data', 'upload_csv', 'update_record'] 