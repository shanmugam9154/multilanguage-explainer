import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from routes.api import api_bp

def create_app():
    """Application factory for the Multilingual Learning Assistant."""
    # Load environment variables from .env file
    load_dotenv()

    app = Flask(__name__)

    # Enable Cross-Origin Resource Sharing for frontend communication
    CORS(app)

    # Application Configuration
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "dev-secret-key")
    app.config['JSON_SORT_KEYS'] = False

    # Register the API blueprint with versioning prefix
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/health', methods=['GET'])
    def health_check():
        """Basic health check endpoint."""
        return {"status": "online", "service": "learning-assistant-api"}, 200

    return app

if __name__ == "__main__":
    app = create_app()
    
    # Run server on port 5000
    # Note: host='0.0.0.0' makes it accessible within a Docker container or local network
    app.run(
        host="0.0.0.0", 
        port=5000, 
        debug=os.getenv("FLASK_DEBUG", "True").lower() == "true"
    )