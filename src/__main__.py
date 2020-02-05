from src.init import app

try:
    import src.local_config as config
except ImportError:
    import src.config as config

    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.FLASK_PORT, debug=config.FLASK_DEBUG)
