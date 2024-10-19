from enum import unique
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    """
    Defines a database model for storing notes. It has four attributes:
    - `id`: a unique identifier for each note.
    - `data`: the content of the note, with a maximum length of 10,000 characters.
    - `date`: the timestamp when the note was created, set to the current time by
    default.
    - `user_id`: a foreign key referencing the `id` of the user who created the note.

    Attributes:
        id (int): Designated as the primary key of the table, uniquely identifying
            each note.
        data (str): Limited to a maximum length of 10,000 characters.
        date (datetime): Indexed to the timezone, meaning the date is stored with
            the timezone information.
        user_id (int): A foreign key referencing the `id` of the `User` model.

    """
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    """
    Defines a database model for users, including attributes such as Social Security
    Number, email, password, name, and address. It also establishes relationships
    with `Checking`, `Savings`, and `Stock` models.

    Attributes:
        id (int): Designated as the primary key of the table, meaning it uniquely
            identifies each record.
        ssn (str): Indexed to ensure uniqueness among all users in the database.
        email (str): Defined with a maximum length of 150 characters, indicating
            that it can store email addresses of up to 150 characters. It is also
            declared as unique, preventing duplicate email addresses for different
            users.
        password (str): Limited to 150 characters.
        first_name (str): Defined within the `User` class, representing the first
            name of a user. It has a maximum length of 150 characters.
        last_name (str): Defined as a column in the database with a maximum length
            of 150 characters.
        address (str): Defined with a maximum length of 250 characters.
        checking (Any): Established through a relationship with the `Checking`
            model, indicating that a user can have multiple checking accounts.
        savings (Any): Represented by a relationship with the `Savings` model,
            indicating a connection between a user and their savings account.
        stock (Dict[str,Stock]): Represented by a relationship with the `Stock`
            class, indicating that a user can have multiple stock accounts.

    """
    id = db.Column(db.Integer, primary_key=True)
    ssn = db.Column(db.String(150),unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    address = db.Column(db.String(250))
    checking = db.relationship('Checking')
    savings = db.relationship('Savings')
    stock = db.relationship('Stock')

class Checking(db.Model):
    """
    Represents a checking account in a database. It has attributes for unique
    account ID, current balance, overdraft limit, and a foreign key referencing
    the associated user ID. This class likely inherits from a base database model,
    allowing it to interact with the database.

    Attributes:
        id (int): A primary key, meaning it uniquely identifies each instance of
            the `Checking` class in the database.
        balance (float): Used to store the current balance of a checking account.
        overdraft (float): Used to represent the maximum amount by which a checking
            account can be overdrawn.
        user_id (int): A foreign key referencing the `id` column of the `User`
            model in the database.

    """
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float)
    overdraft = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Savings(db.Model):
    """
    Represents a savings account in a database, storing its attributes such as
    balance, interest rate, user ID, opening and last update dates, and interest
    earned.

    Attributes:
        id (int): Primary key, which uniquely identifies each instance of the
            `Savings` class in the database.
        balance (float): Stored in the database to represent the current amount
            of money in the savings account.
        interest (float): Represented by a column in the database. It stores the
            interest rate associated with the savings account.
        user_id (int): Foreign-keyed to the `id` attribute of the `User` model in
            the database.
        opened (date): Used to store the date when the savings account was created.
        last (date): Representing the date when the savings account was last
            accessed or updated.
        interest_earned (float): A measure of the interest earned on the savings
            account since its opening.

    """
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float)
    interest = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    opened = db.Column(db.Date())
    last = db.Column(db.Date())
    interest_earned = db.Column(db.Float)



class Stock(db.Model):
    """
    Represents a financial stock in a database. It stores information such as the
    stock's identifier, ticker symbol, purchase price, current price, number of
    shares, associated user, URL, and name.

    Attributes:
        id (int): Designated as the primary key of the table, uniquely identifying
            each stock entry.
        ticker (str): Unique, indicating that each stock in the database must have
            a unique ticker symbol.
        price_bought (float): Used to store the price at which the stock was
            initially purchased.
        price_current (float): Bounded by a maximum value of 150. It represents
            the current market price of a stock.
        shares (int): Represented as a column in the database with a data type of
            `Integer`, which stores the number of shares of a particular stock
            owned by a user.
        user_id (int): Referenced as a foreign key to the `id` attribute of the
            `User` model.
        url (str): Limited to a maximum length of 400 characters. It appears to
            store a web address associated with the stock, possibly the stock's
            official website.
        name (str): Limited to a maximum length of 200 characters.

    """
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(150),unique=True)
    price_bought = db.Column(db.Float(150))
    price_current = db.Column(db.Float(150))
    shares = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    url = db.Column(db.String(400))
    name = db.Column(db.String(200))


   





    
