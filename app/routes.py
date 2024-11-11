from flask import render_template, redirect, url_for, request, flash, session
from app import app


# homepage route

@app.route("/")
def index():
    return render_template("index.html")

# registration route


@app.route("/register", methods=["GET", "POST"])
def register():
    
    # for GET:
    if request.method == 'GET':
        return render_template("register.html")
    
    elif request.method == "POST":
        pass


# login route

@app.route("/login", methods=["GET", "POST"])
def login():
    
    # for GET 
    if request.method == "GET":
        return render_template("login.html")
    
    