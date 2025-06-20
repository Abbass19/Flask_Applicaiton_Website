from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')


    # Import your models here to register them with SQLAlchemy
    from .models import Artist, Album, Customer, Comment  # etc.

    # Optional config
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_object('app.config.Config')

    # Replace with your PostgreSQL info
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:NewPassword2004@localhost:5432/chinook_auto_increment'

    # Register blueprints
    from .routes.main_routes import main
    from .routes.auth_routes import auth

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(main, url_prefix='/')

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
