from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    """
    Initializes a Flask application, configures its settings, and sets up database
    connections. It also registers blueprints for views and authentication, defines
    a user loader for the login manager, and initializes the login manager.

    Returns:
        Flaskapplicationinstance: An instance of the Flask application, configured
        and initialized with various components such as database, authentication,
        and views.

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
        Loads a user from the database based on their ID, using the `User.query.get`
        method to retrieve the user object from the database. The `int(id)`
        conversion ensures the ID is treated as an integer.

        Args:
            id (str | int): Passed to the `User.query.get` method, which expects
                an integer.

        Returns:
            UserorNone: The result of the database query executed by `User.query.get(int(id))`.

        """
        return User.query.get(int(id))

    return app


def create_database(app):
    """
    Checks if a database file exists. If not, it creates the database using
    Flask-SQLAlchemy's `create_all` method and prints a success message.

    Args:
        app (FlaskApp): Required to be passed to the `db.create_all` method. It
            is typically the instance of the Flask application, used to bind the
            database to the application.

    """
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
