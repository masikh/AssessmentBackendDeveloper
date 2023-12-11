""" This file holds the main flask application """

import os
from uuid import uuid4
from wsgiserver import WSGIServer
from routes import doc, api, auth
from database import db
from models.users_model import Group
from flask_application import app

DATABASE_URI = f"sqlite:///{os.path.join(os.getcwd(), 'tasks.db')}"


class APIServer:
    """ Main flask server """
    def __init__(self, ip='127.0.0.1', port=5000):
        self.ip = ip
        self.port = port
        self.debug = bool(os.getenv("debug") is not None)
        self.app = app
        self.wsgi_server = None

    def config(self):
        """ Setup Flask application defaults """

        # Configuration parameters for tuning Flasks behaviour to our needs
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

    @staticmethod
    def create_users_group():
        """Create the 'users' group if it doesn't exist"""
        group = Group.query.filter_by(name='users').first()
        if not group:
            group = Group(name='users')
            db.session.add(group)
            db.session.commit()

    def create_tables(self):
        """ Create database tables """

        # If the tables already exist it will silently continue
        with self.app.app_context():  # <- Is this really needed?
            db.create_all()
            self.create_users_group()

    def run(self):
        """ Start API server"""

        # Friendly CLI message
        print(f'API: http://{self.ip}:{self.port}')

        # Setup Flask configuration parameters
        self.config()

        # Register blueprints (routes)
        self.app.register_blueprint(doc)
        self.app.register_blueprint(api)
        self.app.register_blueprint(auth)

        # Create database upon initialization
        self.create_tables()

        # Start the Flask application
        self.wsgi_server = WSGIServer(self.app, host=self.ip, port=self.port)
        self.wsgi_server.start()

    def stop(self):
        """ Stop API server """

        # server.stop() is wrapped in a try except. Reasoning is that WSGI is not up to par with is_alive
        # thread. It still uses the obsoleted isAlive(). Since the server is being stopped this error is
        # annoying but not 'fatal'.
        try:
            self.wsgi_server.stop()
        except AttributeError:
            print("'WorkerThread' object has no attribute 'isAlive'")
            print("NOTE: Your WSGI doesn't support the is_alive thread methods! (python >3.8)")
