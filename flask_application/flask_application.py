""" This file holds the main flask application """

import os
from uuid import uuid4
from flask import Flask
from wsgiserver import WSGIServer
from routes import api
from database import db


DATABASE_URI = f"sqlite:///{os.path.join(os.getcwd(), 'tasks.db')}"


class APIServer:
    """ Main flask server """
    def __init__(self, ip='127.0.0.1', port=5000):
        self.ip = ip
        self.port = port
        self.debug = bool(os.getenv("debug") is not None)
        self.app = Flask(f'Flask Server running on port: {self.port}')
        self.server = None

    def config(self):
        """ Setup Flask application defaults """
        self.app.config['JSON_SORT_KEYS'] = True
        self.app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', str(uuid4()))
        self.app.config['SESSION_COOKIE_HTTPONLY'] = True
        self.app.config['REMEMBER_COOKIE_HTTPONLY'] = True
        self.app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
        self.app.config['DEBUG'] = self.debug

        # Configure SQLite database
        self.app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        # Bind and initialize database
        db.init_app(self.app)

    def create_tables(self):
        """ Create database tables """
        with self.app.app_context():
            db.create_all()

    def run(self):
        """ Start API server"""
        print(f'API: http://{self.ip}:{self.port}')
        self.config()
        self.app.register_blueprint(api)

        # Create database
        self.create_tables()

        self.server = WSGIServer(self.app, host=self.ip, port=self.port)
        self.server.start()

    def stop(self):
        """ Stop API server """
        try:
            self.server.stop()
        except AttributeError:
            if self.debug:
                print("'WorkerThread' object has no attribute 'isAlive'")
                print("NOTE: Your WSGI doesn't support the is_alive thread methods! (python >3.8)")
