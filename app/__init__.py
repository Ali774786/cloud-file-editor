from flask import Flask, redirect, url_for
import os

def create_app():
    app = Flask(__name__)
    
    # Configure secret key
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-development')
    
    # Register blueprints
    from app.routes import s3_bp
    app.register_blueprint(s3_bp)
    
    # Add root route that redirects to S3 browser
    @app.route('/')
    def index():
        return redirect(url_for('s3.list_processes'))
    
    return app
