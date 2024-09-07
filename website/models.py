from enum import unique
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    """
    Defines a model for database storage. It represents individual notes with
    attributes: a unique identifier (`id`), a long string data field (`data`),
    timestamp (`date`) automatically set to current time, and foreign key referencing
    the `user.id`. This enables linking of notes to specific users.

    Attributes:
        id (int|None): Declared as the primary key of the table. It uniquely
            identifies each note. It auto-increments with each new note created.
        data (str|None): 10000 characters long. It stores a string that represents
            note data, which can be up to 10,000 characters in length.
        date (datetime|None): Timezone-aware. It is set to the current date and
            time by default when a new note is created, thanks to SQLAlchemy's
            automatic execution of the func.now() function as part of the database
            schema creation.
        user_id (int|None): A foreign key referencing the primary key of the 'User'
            table. It establishes a relationship between notes and users, indicating
            which user created or owns each note.

    """
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    """
    Defines a database model for storing user data. It has columns for identifying
    information, such as SSN and email, as well as personal details like name and
    address. It also establishes relationships with three other tables: Checking,
    Savings, and Stock.

    Attributes:
        id (int): Declared as a primary key, which uniquely identifies each record
            in the table. It represents the unique identifier for each user.
        ssn (str|None): 150 characters or less in length. It represents a user's
            Social Security Number and is declared as unique to prevent duplicate
            SSNs within the database.
        email (str|None): 150 characters maximum long, ensuring uniqueness among
            users due to a unique constraint applied at database level.
        password (str|None): 150 characters long, indicating a database column to
            store user passwords.
        first_name (str): 150 characters long, representing a user's first name.
            It is stored as a column in the database with a maximum length of 150
            characters.
        last_name (str|None): 150 characters long. It represents the last name of
            a user and has no explicit constraints or validation applied to it.
        address (str): 250 characters long. It is likely used to store a user's
            physical address, but lacks any validation or formatting constraints.
        checking (RelationshipProxy): Referenced to the 'Checking' model, indicating
            a one-to-one relationship between the User and Checking models through
            a foreign key.
        savings (Savings): A relationship to the Savings model. It represents the
            savings account associated with a user, likely defined by a foreign
            key referencing the `id` column of the User table.
        stock (Stock|None): Linked to a relationship with the Stock model through
            a back-reference, indicating that each stock belongs to one user.

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
    Defines a database model for a checking account. It has columns to store unique
    identifiers (`id`, `balance`, and `overdraft`) and links each account to a
    user through foreign key `user_id`.

    Attributes:
        id (int|None): Primary key to uniquely identify each instance of the table
            in the database.
        balance (float): A column in a database table representing the current
            balance of a checking account.
        overdraft (float): Used to represent the amount by which a checking account
            can exceed its balance without incurring fees or penalties.
        user_id (int|None): A foreign key referencing the id column of the 'user'
            table, indicating that this checking account belongs to a user.

    """
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float)
    overdraft = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Savings(db.Model):
    """
    Defines a model for a savings account database table. It represents an entity
    with attributes such as balance, interest rate, user ID, opening date, last
    transaction date, and interest earned. These properties enable tracking of
    savings account information over time.

    Attributes:
        id (int|None): A primary key. It uniquely identifies each instance of the
            Savings model. This value will be auto-generated upon creation.
        balance (float): A column in the database table that stores the current
            balance of a savings account. It represents the amount of money available
            in the account.
        interest (float): A field that stores the current rate at which interest
            is being earned on a savings account.
        user_id (int|None): A foreign key referencing the id attribute in the User
            model, indicating that it represents the ID of a user associated with
            this savings account.
        opened (Date|None): A column that stores the date when the savings account
            was opened by a user. It is used to keep track of the creation time
            of each savings account instance.
        last (date): A column representing the most recent date when some operation
            or event occurred to the savings account.
        interest_earned (float): A measure of the amount of interest earned on a
            savings account, representing the total accumulated interest over time.

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
    Represents a stock holding with the following attributes: unique identifier,
    ticker symbol, purchase price, current price, number of shares owned, associated
    user ID, URL, and name. It serves as an object to store and manage stock data
    within a database.

    Attributes:
        id (int|None): A primary key. It uniquely identifies each record in the
            database table associated with this model, ensuring data integrity by
            allowing rows to be addressed individually.
        ticker (str|None): 150 characters long at most, it represents a unique
            identifier for each stock such as "AAPL" or "GOOG", stored uniquely
            within the database.
        price_bought (float): 150 digits long, representing the price at which
            shares were initially purchased. It has no constraints beyond its data
            type and length specifications.
        price_current (float): 150 decimal places long. It represents the current
            market price of a stock, capturing its value at any given time.
        shares (int): Part of a column named shares, used to store the quantity
            of stocks owned by a user.
        user_id (int|None): A foreign key referencing the `id` column of the 'User'
            table, establishing a relationship between a stock holding and its owner.
        url (str): 400 characters long. It represents a web address associated
            with a stock, but its specific purpose or usage in this context is
            unclear without additional information.
        name (str): 200 characters long, storing a string value representing the
            official company name for a stock. It is a database column with a
            specific maximum length.

    """
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(150),unique=True)
    price_bought = db.Column(db.Float(150))
    price_current = db.Column(db.Float(150))
    shares = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    url = db.Column(db.String(400))
    name = db.Column(db.String(200))


   





    
