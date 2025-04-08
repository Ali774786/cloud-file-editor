from flask import Blueprint
from app.views.views import get_data, upload_csv, update_record

# Create blueprint
api_bp = Blueprint('api', __name__)

# Register page routes
api_bp.add_url_rule('/', view_func=get_data, endpoint='index')
api_bp.add_url_rule('/upload', view_func=upload_csv, methods=['GET', 'POST'], endpoint='upload_file')

# Register API routes
api_bp.add_url_rule('/api/update/<int:record_id>', view_func=update_record, methods=['POST'], endpoint='update_record') 