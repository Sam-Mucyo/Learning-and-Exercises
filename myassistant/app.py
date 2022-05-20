from unicodedata import numeric
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, Response, jsonify
from flask_session import Session
from sqlalchemy import NUMERIC

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
# db = SQL("sqlite:///classes.db")

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/multiplechoices')
def multiplechoices():
    return render_template('multiplechoices.html')

@app.route('/flashcards')
def flashcards():
    return render_template('flashcards.html')
