from flask import Flask
from celery import Celery
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
celery = Celery(__name__, broker='memory://')

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
        from . import routes
        app.register_blueprint(routes.main)

    return app