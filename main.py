# main.py
"""
@file main.py
@brief Entry point for the Flask application.
"""
from flask import Flask
from controllers.api import api_bp
from config import Config
from logger import get_logger

logger = get_logger(__name__)

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_bp)

    @app.route("/health", methods=["GET"])
    def health():
        logger.debug("Health check endpoint called")
        return {"status": "ok"}

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=Config.PORT, debug=False)
