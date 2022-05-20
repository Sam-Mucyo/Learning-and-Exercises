# API Key to use:  export API_KEY=IEX_TOKEN
import os

from cs50 import SQL

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash


from helpers import apology, login_required, lookup, usd


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Get the user's cash
    data = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    cash = data[0]["cash"]
    total = cash

    row2 = db.execute("SELECT * FROM shares WHERE user_id = ?", session["user_id"])
    
    if not row2:
        assets = []
    else:
        # Get the users current assets
        assets = db.execute("SELECT * FROM shares WHERE user_id = ?", session["user_id"])
        # total_row = db.execute("SELECT TOTAL(total) FROM shares WHERE user_id = ?", session["user_id"])
        for asset in assets:
            total += asset["total"]

    return render_template("index.html", assets=assets, cash=cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # Are inputs empty
        if not request.form.get("symbol"):
            return apology("Missing Symbol", 400)
        if not request.form.get("shares"):
            return apology("Missing Shares", 400)
        
        if not request.form.get("shares").isdigit():
            return apology("Missing", 400)
    
        # Is the shares inputed valid?
        if not request.form.get("shares").isdigit() or int(request.form.get("shares")) < 0:
            return apology("Invalid Share Input", 400)

        # Check if the inputed symbol is valid
        results = lookup(request.form.get("symbol"))
        if not results:
            return apology("INVALID SYMBOL", 400)

        symbol = results["symbol"]
        price = results["price"]
        stock_name = results["name"]

        # Get users current amount
        user_id = session["user_id"]
        row = db.execute("SELECT * FROM users WHERE id = ?", user_id)
        user_amount = row[0]["cash"]

        # If the user cannot afford, let him/her know
        shares = float(request.form.get("shares"))
        if user_amount < shares*price: 
            return apology("CANNOT AFFORD", 400)

        # Save transaction in the database
        db.execute("INSERT INTO transactions (user_id, symbol, price, shares) VALUES (?, ?, ?, ?)",
                    user_id, symbol, price, shares)

        # Update the user's current cash
        balance = user_amount - (shares*price)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", balance, user_id)

        # Update shares table to represent user's current assets
        currentrow = db.execute("SELECT * FROM shares WHERE user_id = ? AND symbol = ?", user_id, symbol)

        if not currentrow:
            db.execute("INSERT INTO shares (user_id, symbol, stock_name, price, shares, total) VALUES (?, ?, ?, ?, ?, ?)",
             user_id, symbol, stock_name, price, shares, (shares*price))
        else:
            current_shares = currentrow[0]["shares"]
            current_total = currentrow[0]["total"]
            db.execute(
                "UPDATE shares SET shares = ?, total = ? WHERE user_id = ? AND symbol = ?", 
                current_shares+shares, current_total+(shares*price), user_id, symbol)
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ?", session["user_id"])
    return render_template("history.html", transactions=transactions)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout") 
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        results = lookup(request.form.get("symbol"))
        if not results:
            return apology("INVALID SYMBOL", 400)
        company_name = results["name"]
        price = usd(results["price"])

        return render_template("quoted.html", company_name=company_name, price=price)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username is not blank
        if not request.form.get("username"):
            return apology("Please put in the username", 400)

        # Ensure password is not blank
        elif not request.form.get("password"):
            return apology("Please put in the password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username is not already in the database 
        if len(rows) > 0:
            return apology("The username is already taken", 400)
        # Ensure passwords match
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords must match", 400)
        # Register the user
        hashed = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), hashed)
        
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        # Are inputs empty
        if not request.form.get("symbol"):
            return apology("Missing Symbol", 400)
        elif not request.form.get("shares"):
            return apology("Missing Shares", 400)

        # Check if the inputed symbol is valid
        results = lookup(request.form.get("symbol"))
        if not results:
            return apology("INVALID SYMBOL", 400)

        symbol = results["symbol"]
        price = results["price"]
        user_id = session["user_id"]

        # Check if the inputed symbol is already owned
        shares_row = db.execute("SELECT * FROM shares WHERE user_id = ? AND symbol = ?", user_id, symbol)
        if not shares_row:
            return apology("Sorry, you don't own shares from the inputed company", 400)

        # Get the shares user is selling
        selling_shares = float(request.form.get("shares"))

        # If the he's selling more than he owns, let him/her know
        owned_shares = shares_row[0]["shares"]
        if owned_shares < selling_shares: 
            return apology("INSUFFICIENT SHARES TO SELL", 400)

        # Get users current cash and update it
        row = db.execute("SELECT * FROM users WHERE id = ?", user_id)
        balance = row[0]["cash"] + (selling_shares*price)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", balance, user_id)

        # Save transaction in the database
        db.execute("INSERT INTO transactions (user_id, symbol, price, shares) VALUES (?, ?, ?, ?)",
                   user_id, symbol, price, selling_shares*-1.0)

        # Update shares table to represent user's current assets
        current_total = shares_row[0]["total"]

        db.execute(
            "UPDATE shares SET shares = ?, total = ? WHERE user_id = ? AND symbol = ?", 
            owned_shares - selling_shares, current_total - (selling_shares*price), user_id, symbol)
        return redirect("/")

    else:
        symbols_rows = db.execute("SELECT * FROM shares WHERE user_id = ?", session["user_id"])
        symbols = []
        for symbol in symbols_rows:
            symbols.append(symbol["symbol"])
            
        return render_template("sell.html", symbols=symbols)


@app.route("/load", methods=["GET", "POST"])
@login_required
def load():
    
    if request.method == "POST":
        # Get users current cash and update it
        loaded = float(request.form.get("amount"))
        row = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        balance = row[0]["cash"] + loaded
        db.execute("UPDATE users SET cash = ? WHERE id = ?", balance, session["user_id"])
        flash("Amount Added!")
        return redirect("/")
    else:
        return render_template("load.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)