from flask import Flask
import os

def create_app():
    print("Starting to create app...")
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    
    print("Registering blueprint...")
    from app import main
    app.register_blueprint(main.bp)
    
    print("App creation complete.")
    return app

print("__init__.py loaded")
