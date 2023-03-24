from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_app():

    app = Flask(__name__)
    app.config.from_pyfile('../config.py')

    db = SQLAlchemy(app)

    with app.app_context():
        from application import routes
        from application import models

    return app
