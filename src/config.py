from os import environ

# Flask config
FLASK_PORT = environ.get("PORT", 8000)
FLASK_DEBUG = False
SECRET_KEY = environ.get("SECRET_KEY", "somesecretkey")
APP_URL = "http://ege-basis.herokuapp.com/"

# MongoDB config
DB_HOST = environ.get("DB_HOST", "")
DB_NAME = environ.get("DB_NAME", "egebasis-test")

# Security config
SALT = environ.get("SALT", "somesalt")

# Mail config
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = environ.get("MAIL_USERNAME", "someone@gmail.com")
MAIL_DEFAULT_SENDER = MAIL_USERNAME
MAIL_PASSWORD = environ.get("MAIL_PASSWORD", "")
