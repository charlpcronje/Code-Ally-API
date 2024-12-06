# logger.py
"""
@file logger.py
@brief Configures logging for the application.
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from config import Config

# Ensure logs directory exists
os.makedirs(os.path.dirname(Config.LOG_PATH), exist_ok=True)

def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(Config.LOG_LEVEL.upper())

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(Config.LOG_LEVEL.upper())

    # File handler
    fh = RotatingFileHandler(Config.LOG_PATH, maxBytes=1048576, backupCount=5)
    fh.setLevel(Config.LOG_LEVEL.upper())

    formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(name)s: %(message)s")
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(ch)
        logger.addHandler(fh)

    return logger
