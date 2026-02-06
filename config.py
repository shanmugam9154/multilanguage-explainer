import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from .env file
load_dotenv(os.path.join(BASE_DIR, ".env"))

class Config:
    """
    Production-ready configuration class.
    Reads sensitive data from environment variables to avoid hardcoding secrets.
    """
    
    # Flask Settings
    DEBUG = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    SECRET_KEY = os.environ.get("SECRET_KEY", "default-dev-key-change-in-production")
    
    # Gemini AI Settings
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    
    if not GEMINI_API_KEY:
        # Raising an error during startup ensures the app doesn't fail silently later
        raise ValueError("CRITICAL: GEMINI_API_KEY is not set in the environment.")

    # API Configuration
    JSON_SORT_KEYS = False
    CORS_HEADERS = "Content-Type"

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    # In production, we strictly require a real SECRET_KEY
    SECRET_KEY = os.environ.get("SECRET_KEY")

# Mapping for easy selection
config_map = {
    "dev": DevelopmentConfig,
    "prod": ProductionConfig
}