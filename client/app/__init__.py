from flask import Flask
from .routes import site
from celery import Celery, Task
import secrets
from .events import socketio


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object('celeryConfig')
    celery_app.Task = FlaskTask
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = secrets.token_hex(16)
    app.register_blueprint(site)

    socketio.init_app(app)
    celery_init_app(app)

    return app, socketio

