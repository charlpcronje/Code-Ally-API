# config.py
"""
@file config.py
@brief Loads environment variables and provides configuration to the app.
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_KEY = os.getenv("API_KEY", "")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_PATH = os.getenv("LOG_PATH", "./logs/app.log")
    PORT = int(os.getenv("PORT", 5000))
