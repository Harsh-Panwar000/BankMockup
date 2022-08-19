# Bank Mockup
Created a functioning mockup of a banking app from the user view (front-end, back-end, and database)

A user can sign-up, log in, create savings and checking accounts, modify savings/checking accounts (withdraw/deposit), invest in stocks, update number of stock shares, and modify personal information.

In order to run this locally, please install the following python packages with pip:

```python
pip install Flask
pip install Flask-Login
pip install Flask-SQLAlchemy
pip install Requests
pip install Yfinance
pip install Werkzeug
pip install Urllib3
```

A requirements.txt file is added for convenience. To install all dependecies run the following command:
```python
pip install -r requirements.txt
```

To run program, execute the following command in Terminal(Linux/Mac) or Command Prompt(Windows):
```python
python3 main.py
```

Once the development server is active, enter the url from the Terminal/CMD. It should look like:
```
http://127.0.0.1:5000/
```
