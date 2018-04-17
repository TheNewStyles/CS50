from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    return apology("TODO")

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    if request.method == "POST":
        # ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide a stock symbol")
        # ensure shares was submitted
        elif not int(request.form.get("shares")):
            return apology("must provide shares amount")
        
        stock = lookup(request.form.get("symbol"))
        if stock == None:
            return apology("Could not find stock")

        shares = int(request.form.get("shares"))
        stockPrice = stock.get("price")
        stockName = stock.get("name")
        totalPrice = stockPrice * shares;
        purchaseTime = datetime.datetime.now()
        
        try:
            cash =  db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        except:
            apology("sql exception")
            
        cash = int(cash[0]["cash"])
        if totalPrice > cash:
            return apology("Too broke")
        remaining = round(cash,2) - round(totalPrice,2)

        try:
            db.execute("UPDATE users SET cash = :remaining WHERE id = :id", remaining=remaining, id=session["user_id"])
            db.execute("INSERT INTO transactions (userid, stock, price, shares, purchaseprice, time) VALUES (:userid, :stock, :price, :shares, :purchaseprice, :time)", 
                    userid=session["user_id"], stock=stockName, price=stockPrice, shares=shares, purchaseprice=totalPrice, time=purchaseTime)
        except:
            apology("sql expection")
    
        return render_template("buy.html")
    else:
        return render_template("buy.html")



@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    return apology("TODO")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""
    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        # call helper lookup
        symbol = request.form.get("quote")
        stock = lookup(symbol)

        return render_template("quoted.html", stock=stock)
    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    if request.method == "POST":
        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")
        
        userName = request.form.get("username")
        hashPwd = pwd_context.hash(request.form.get("password"))
        
        try:
            db.execute("INSERT INTO users (username, hash) VALUES(:name, :password)", name=userName, password=hashPwd)
        except :
            return apology("SQL exception")
            
        # redirect user to home page
        return redirect(url_for("index"))
    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    return apology("TODO")
