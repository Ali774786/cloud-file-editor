from flask import Blueprint
from app.views.s3_views import (
    list_processes, 
    list_files, 
    view_file,
    update_file
)

# Create blueprint for S3 routes
s3_bp = Blueprint('s3', __name__, url_prefix='/s3')

# Register S3 routes
s3_bp.add_url_rule('/', view_func=list_processes, endpoint='list_processes')
s3_bp.add_url_rule('/process/<process_id>', view_func=list_files, endpoint='list_files')
s3_bp.add_url_rule('/file', view_func=view_file, endpoint='view_file')
s3_bp.add_url_rule('/update', view_func=update_file, methods=['POST'], endpoint='update_file') 