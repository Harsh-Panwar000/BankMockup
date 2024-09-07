from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    """
    Initializes a Flask application, configures it with database settings, and
    sets up authentication and user loading functionalities. It also registers
    blueprints for views and auth, and creates the database schema by calling
    another function.

    Returns:
        Flask: A web application instance configured with various settings and
        components, including database, authentication, and views.

    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        """
        Loads a user from the database based on their ID. It queries the `User`
        table using SQLAlchemy's `query.get` method, passing the ID as an integer
        and returning the corresponding user object if found.

        Args:
            id (Union[int, str]): Required to be passed by Flask-Login's login
                manager. It represents the user ID for loading a user from the database.

        Returns:
            User|None: A user instance from database if found otherwise None
            indicating no such user was found.

        """
        return User.query.get(int(id))

    return app


def create_database(app):
    """
    Checks for the existence of a database file. If it does not exist, creates the
    database schema using Flask-Migrate (db) and applies it to the application.
    It then prints a success message. The function is called with an application
    instance as an argument.

    Args:
        app (Flask): Required for creating the database tables. It refers to an
            instance of a Flask application, which provides information necessary
            for the database to be created correctly within the context of the app.

    """
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
