from flask import Flask
from dotenv import load_dotenv
from config import Config, DevelopmentConfig, ProductionConfig, TestingConfig
from app.task_manager.routes import task_manager
from .database import db

def create_app(config_name=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(Config)

    load_dotenv()

    db.init_app(app)

    with app.app_context():
        db.create_all()
    
    app.register_blueprint(task_manager)

    # Print all routes
    # Not for production!
    with app.app_context():
        print('Registered routes:')
        for rule in app.url_map.iter_rules():
            methods = ','.join(sorted(rule.methods))
            print(f"{rule.endpoint:50s} {methods:30s} {rule}")

    return app
