import os
from flask import Flask
from flask_cors import CORS
from flask_restplus import Api
from flask_fixtures import load_fixtures, loaders
from . import apis
from .dal import db

class Service(object):
    """Container for Flask application and extensions"""

    def __init__(self, app_name, root_path=None):
        """
        Initializes Flask application and extensions

        Attributes
        ----------
        app:flask.Flask
            Flask application instance

        db:flask_sqlalchemy.SQLAlchemy
            Flask-SQLAlchemy extension
        
        api:flask_restplus.Api
            Flask-RestPlus extension

        """
        self.app = init_app(app_name, root_path)
        self.db = init_db(self.app)
        self.api = init_api(self.app)

def init_app(name, root_path):
    """Creates Flask application"""
    app = Flask(name, root_path=root_path)
    app.config.from_pyfile(os.path.join(app.root_path, 'default.cfg'))
    return app

def init_db(app):
    """Initializes Flas-Alchemy extension"""
    db.init_app(app)

    with app.app_context():
        db.create_all()
        _load_fixtures(app, db)

    return db

def _load_fixtures(app, db):
    for fixture in app.config.get('STARTUP_FIXTURES', []):
        load_fixtures(db, loaders.load(os.path.join(app.root_path, 'fixtures', fixture)))

def init_api(app):
    """Initializes Flask-RestPlus extension"""
    api = Api(app)

    for ns in apis.namespaces:
        api.add_namespace(ns, '/api')
        
    return api