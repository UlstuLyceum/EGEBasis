from os import environ

# Flask config
FLASK_PORT = environ.get("PORT", 8000)
FLASK_DEBUG = False
SECRET_KEY = environ.get("SECRET_KEY", "somesecretkey")

# MongoDB config
DB_HOST = environ.get("DB_HOST", "")
DB_NAME = environ.get("DB_NAME", "egebasis-test")

# Security config
SALT = environ.get("SALT", "somesalt")
