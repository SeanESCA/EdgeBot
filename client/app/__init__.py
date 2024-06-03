from flask import Flask
from .routes import site
import secrets
from .events import socketio


def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = secrets.token_hex(16)
    app.register_blueprint(site)

    socketio.init_app(app)

    return app, socketio

