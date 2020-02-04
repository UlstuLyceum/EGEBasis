from os import environ

# Flask config
FLASK_PORT = environ.get("PORT", 8000)
