from celery import Celery
from app import create_app

app = create_app()
celery = Celery(app.name, broker='memory://')