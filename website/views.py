from flask import Blueprint, redirect, render_template, request, flash, jsonify, session, url_for
from flask_login import login_required, current_user
from .models import Checking, Stock,Savings, User
from . import db
import json, random
from datetime import date, datetime
import yfinance as yf
from hashlib import sha256
from werkzeug.security import generate_password_hash, check_password_hash

views = Blueprint('views', __name__)

@views.route('/')
def bank():
    return render_template("welcome.html", user = current_user)


@views.route('/checking', methods=['GET', 'POST'])
@login_required
def checking():
    if request.method == 'POST':
        if request.form['submit'] == 'newAcc':
            deposit = request.form.get('deposit')
            if len(deposit) < 1:
                flash("Please Enter valid amount", category='error')
            else:
                new_checking = Checking(balance = deposit, user_id = current_user.id, overdraft = random.randrange(100,200) )
                db.session.add(new_checking)
                db.session.commit()
                flash('New Account Created!', category='success')
                return redirect(url_for('views.checking'))
        if request.form['submit'] == 'withdraw':
            amount = float(request.form.get('withdraw'))
            id1 = int(request.form.get("id"))
            if amount <= 0:
                flash("Please Enter valid amount", category='error')
            else:
                account = Checking.query.filter_by(user_id = current_user.id, id = id1).first()
                account.balance -= amount
                if account.balance < 0:
                    account.balance -= account.overdraft
                    flash("Withdrew too many funds. Overdraft fee of "+str(account.overdraft)+" has been charged", category='error')
                db.session.commit()
                return redirect(url_for('views.checking'))
        
        if request.form['submit'] == 'deposit':
            amount = float(request.form.get('deposit'))
            id1 = int(request.form.get("id"))
            if amount <= 0:
                flash("Please Enter valid amount", category='error')
            else:
                account = Checking.query.filter_by(user_id = current_user.id, id = id1).first()
                account.balance += amount
                db.session.commit()
                return redirect(url_for('views.checking'))
                
    return render_template("checking.html", user=current_user)

@views.route('/savings', methods=['GET', 'POST'])
@login_required
def savings():               
    if request.method == 'POST':
        if request.form['submit'] == 'newAcc':
            deposit = request.form.get('add')
            if len(deposit) < 1:
                flash("Please Enter valid amount", category='error')
            else:
                new_savings = Savings(balance = deposit, user_id = current_user.id, interest = round(random.uniform(.1,.2),2 ), opened = date.today(), interest_earned=0, last = date.today())
                db.session.add(new_savings)
                db.session.commit()
                flash('New Account Created!', category='success')
                return redirect(url_for('views.savings'))
        if request.form['submit'] == 'withdraw':
            amount = float(request.form.get('withdraw'))
            id1 = int(request.form.get("id"))
            if amount <= 0:
                flash("Please Enter valid amount", category='error')
            else:
                account = Savings.query.filter_by(user_id = current_user.id, id = id1).first()
                account.balance -= amount
                db.session.commit()
                return redirect(url_for('views.savings'))
        if request.form['submit'] == 'deposit':
            amount = float(request.form.get('deposit'))
            id1 = int(request.form.get("id"))
            if amount <= 0:
                flash("Please Enter valid amount", category='error')
            else:
                account = Savings.query.filter_by(user_id = current_user.id, id = id1).first()
                account.balance += amount
                db.session.commit()
                return redirect(url_for('views.savings'))
    today = date.today() 
    for savings in current_user.savings:
        if ((today - savings.last).days / 30 > 1):
            if (type(savings.interest_earned) == float):
                savings.interest_earned+=savings.balance*(.01*savings.interest)
                savings.last = today
                savings.balance*=(1+savings.interest*.01)
                db.session.commit()
    return render_template("savings.html", user=current_user, date = today)

@views.route('/portfolio', methods=['GET', 'POST'])
@login_required
def portfolio(): 
    if request.method == 'POST':
        if request.form['submit'] == 'ticker':
            ticker = request.form.get('ticker')
            return redirect(url_for("views.stock", tick= ticker))
        elif request.form['submit'] == 'buy':
            shares = int(request.form.get('buy'))
            id = int(request.form.get('id'))
            stock = Stock.query.filter_by(user_id = current_user.id, id = id).first()
            stock.shares += shares
            db.session.commit()
        elif request.form['submit'] == 'sell':
            shares = int(request.form.get('sell'))
            id = int(request.form.get('id'))
            stock = Stock.query.filter_by(user_id = current_user.id, id = id).first()
            stock.shares -= shares
            db.session.commit()
    for stock in current_user.stock:
        new = yf.Ticker(stock.ticker).info
        stock.price_current = new['currentPrice']
        db.session.commit()
    return render_template("portfolio.html", user = current_user)

@views.route('/personal', methods=['GET', 'POST'])
@login_required
def personal():
    if request.method=='POST':
        newEmail = request.form.get('newEmail')
        newAddress = request.form.get('newAddress')
        oldpass = request.form.get('oldpass')
        newpass = request.form.get('newpass')
        user = User.query.filter_by(id = current_user.id).first()
        if (len(newEmail)> 0):
            user.email = newEmail
        if(len(newAddress)>0):
            user.address = newAddress
        if(len(newpass) > 0):
            if not check_password_hash(user.password,oldpass):
                flash("Current password is incorrect!", category='error')
                return redirect(url_for('views.personal'))
            if not len(newpass) > 6:
                flash("New password must be at least 7 characters", category='error')
                return redirect(url_for('views.personal'))
            user.password = generate_password_hash(newpass,method='sha256')
        db.session.commit()
        flash('Update was successful!', category='success')
        return redirect(url_for('views.personal'))
    return render_template('personal.html', user= current_user)

@views.route('/stock/<tick>', methods=['GET', 'POST'])
@login_required
def stock(tick):
    stock = yf.Ticker(tick)
    dict = stock.info
    try: 
        name = dict['longName']
    except:
        flash('Ticker does not exist', category='error')
        return redirect(url_for('views.portfolio'))
    curr = dict['currentPrice']
    prof = dict['grossProfits']
    rev = dict['totalRevenue']
    cap = dict['marketCap']
    try:
        div = dict['fiveYearAvgDividendYield']
    except:
        div = "0"
    try:
        url = dict['logo_url']
    except:
        url = "https://st4.depositphotos.com/14953852/22772/v/450/depositphotos_227725020-stock-illustration-image-available-icon-flat-vector.jpg"
 
    l = [curr, prof, rev, cap, div]
    p = []
    for metric in l:
        if (type(metric) not in [int,float]):
            metric = 0
        metric = "${:,.2f}".format(metric)
        p.append(metric)
    curr, prof, rev, cap, div = p
    if request.method == 'POST':
        shares = request.form.get('shares')
        new_stock = Stock(ticker = tick, shares = shares, price_bought = dict['currentPrice'], price_current= dict['currentPrice'], user_id = current_user.id,name = name, url = url)
        db.session.add(new_stock)
        db.session.commit()
        return redirect(url_for('views.portfolio'))
    return render_template("stock.html",user = current_user,t = tick, name = name, price = curr, prof = prof, rev = rev, cap = cap, dividend = div) 
