"""
Configuration module for Moretus application
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database Configuration
DB_PATH = os.getenv("DB_PATH", "moretus.db")

# Streamlit Configuration
STREAMLIT_DEBUG = os.getenv("STREAMLIT_DEBUG", "false").lower() == "true"

# Application Configuration
APP_ENV = os.getenv("APP_ENV", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Streamlit page configuration
STREAMLIT_CONFIG = {
    "page_title": "Moretus Application",
    "page_icon": "📊",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
    "menu_items": {
        "Get Help": "https://www.streamlit.io",
        "Report a bug": "https://github.com",
        "About": "Moretus Application v1.0"
    }
}

# Database configuration
DATABASE_CONFIG = {
    "path": DB_PATH,
    "timeout": 5.0,
    "check_same_thread": False,
}

# Application constants
APP_NAME = "Moretus"
APP_VERSION = "1.0.0"
