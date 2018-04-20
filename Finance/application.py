from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *
import datetime

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

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    id = session["user_id"]
    user = db.execute("SELECT * FROM users WHERE id=:id", id=id)
    name = user[0]["username"]
    cashBalance = round(user[0]["cash"],2)
    stocksAr = []
    totalStockValue = 0;
    
    try:
        stocks = db.execute("SELECT stock, sum(shares) as total_shares, AVG(price) as price FROM transactions WHERE userid=:id GROUP BY stock ORDER BY stock", id=id)
    except:
        return apology("This user owns no stocks")
    
    stocksAr = getStocks(id)
    totalStockValue = getStockValue(id, stocksAr)
    totalWorth = round(totalStockValue + cashBalance, 2)

    return render_template("index.html", name= "Username: " + name, stocks=stocksAr, cash= "Cash balance: " + str(cashBalance),  total= "Total value: " + str(totalWorth))

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
        stockPrice = round(stock.get("price"), 2)
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

@app.route("/cash", methods=["GET", "POST"])
def cash():
    #add cash to account
    if request.method == "POST":
        if not request.form.get("cash"):
            return apology("must provide amount")
        id = session["user_id"]
        user = db.execute("SELECT * FROM users WHERE id=:id", id=id)
        currentCash = user[0]["cash"]
        addedCash = int(request.form.get("cash"))
        cash = round(currentCash + addedCash,2)
        db.execute("UPDATE users SET cash = :total WHERE id = :id", total=cash, id=session["user_id"])
        
        return render_template("cash.html", message= str(cash) + " is your new balance")
    
    return render_template("cash.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    id = session["user_id"]
    user = db.execute("SELECT * FROM users WHERE id=:id", id=id)
    name = user[0]["username"]
    history = getHistory(id)
    
    return render_template("history.html", name=name, stocks=history)

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
    if request.method == "POST":
        id = session["user_id"]
        user = db.execute("SELECT * FROM users WHERE id=:id", id=id)
        name = user[0]["username"]
        cashBalance = user[0]["cash"]
        stocksAr = getStocks(id)
        hasStock = False
        hasEnoughStock = False
        stockToSell = {}
        
        if not request.form.get("symbol"):
            return apology("must provide stock symbol")
        
        if not request.form.get("shares"):
            return apology("must provide shares amount")
            
        for i in stocksAr:
            if i["symbol"] == request.form.get("symbol").upper():
                hasStock = True
                if i["totalShares"] >= int(request.form.get("shares")):
                    hasEnoughStock = True
                    stockToSell = i
                    
        if hasStock and hasEnoughStock:
            print("has stock and shares")
            print(stockToSell)
            shares = int(request.form.get("shares")) * -1
            price = stockToSell["currentPrice"]
            total = cashBalance + (round(shares * price, 2))
            sellTime = datetime.datetime.now()
            symbol = stockToSell["symbol"]
            
            #add cash to users table  
            db.execute("UPDATE users SET cash = :total WHERE id = :id", total=total, id=session["user_id"])
            #add transaction with negative shares for that user
            db.execute("INSERT INTO transactions (userid, stock, price, shares, purchaseprice, time) VALUES (:userid, :stock, :price, :shares, :sellprice, :time)", 
                    userid=session["user_id"], stock=symbol, price=price, shares=shares, sellprice=total, time=sellTime)
    
            return render_template("sell.html", message="Stock sold successfully")
        else:
            apology("Incorrect stock symbol or user does not own enough")

    else:
        return(render_template("sell.html"))
    
def getStocks(id):
    stocksAr = []
    try:
        stocks = db.execute("SELECT stock, sum(shares) as total_shares, AVG(price) as price FROM transactions WHERE userid=:id GROUP BY stock ORDER BY stock", id=id)
    except:
        return apology("This user owns no stocks")
    
    for i in stocks:
        #currentPrice = lookup(i["stock"]) - Price lookup taking to long because yahoo finance is deprecated
        #if currentPrice == None:
        currentPrice = i["price"]
        #else:
            #currentPrice = currentPrice.get("price")

        stockObject = {
            "symbol": i["stock"],
            "totalShares": i["total_shares"],
            "currentPrice": round(currentPrice,2),
            "totalValue": round(currentPrice * i["total_shares"],2)
        }
        
        stocksAr.append(stockObject)
    return stocksAr

def getHistory(id):
    stocksAr = []
    try:
        stocks = db.execute("SELECT stock, shares, price, purchaseprice, time FROM transactions WHERE userid=:id ORDER BY time", id=id)
    except:
        return apology("This user owns no stocks")
    
    for i in stocks:
        currentPrice = i["price"]

        stockObject = {
            "stock": i["stock"],
            "shares": i["shares"],
            "price": round(i["price"],2),
            "purchaseprice": round(currentPrice * i["purchaseprice"],2),
            "time": i["time"]
        }
        
        stocksAr.append(stockObject)
    return stocksAr
    
def getStockValue(id, stocksAr):
    totalStockValue = 0
    for i in stocksAr:
        print(i)
        totalStockValue += i["totalValue"]
        print(totalStockValue)
    return totalStockValue
