import os
from flask import Flask
from flask_cors import CORS
from flask_restplus import Api
from flask_fixtures import load_fixtures, loaders
from . import apis
from .dal import db

def bootstrap(name):
    return _boot(bootstrap_app(name), bootsrap_db, bootsrap_api, CORS)

def _boot(app, *modules):
    for module in modules:
        module(app)

    return app

def bootstrap_app(name):
    app = Flask(name)
    app.config.from_pyfile('default.cfg')
    return app

def bootsrap_db(app):
    db.init_app(app)

    with app.app_context():
        db.create_all()
        _load_fixtures(app, db)

    return db

def _load_fixtures(app, db):
    for fixture in app.config['STARTUP_FIXTURES']:
        load_fixtures(db, loaders.load(os.path.join(app.root_path, '..', 'fixtures', fixture)))

def bootsrap_api(app):
    api = Api(app)

    for ns in apis.namespaces:
        api.add_namespace(ns, '/api')
        
    return api