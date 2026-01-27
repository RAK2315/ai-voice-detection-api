import os

# Get the base directory (project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# API Key from environment variable
API_KEY = os.getenv("API_KEY", "sk_voice_detection_12345_secret")

# Model path (works on any system)
MODEL_PATH = os.path.join(BASE_DIR, "models", "voice_detector.pkl")

# Supported languages
SUPPORTED_LANGUAGES = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]