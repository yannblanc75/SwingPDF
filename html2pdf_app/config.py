# config.py
import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    WTF_CSRF_ENABLED = True
    SESSION_COOKIE_SECURE = False
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "..", "instance", "generated")
    LOG_FILE = os.path.join(BASE_DIR, "..", "instance", "app.log")
    MAX_CONTENT_LENGTH = 4 * 1024 * 1024  # 4MB
    # Sécurité headers
    SEND_FILE_MAX_AGE_DEFAULT = 0

class ProdConfig(Config):
    SESSION_COOKIE_SECURE = True
    DEBUG = True

class DevConfig(Config):
    DEBUG = True
