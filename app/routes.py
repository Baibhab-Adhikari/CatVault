from flask import render_template, redirect, url_for, request, flash, session
from app import app


# error handler route (suggested by chatgpt)
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 400


# homepage route

@app.route("/")
def index():
    """route for the homepage"""

    return render_template("index.html")

# registration route


@app.route("/register", methods=["GET", "POST"])
def register():
    """Registration for new user"""
    # for GET:
    if request.method == 'GET':
        return render_template("register.html")

    # for POST:
    elif request.method == "POST":

        # variables to store info
        first_name = request.form.get("firstname")
        last_name = request.form.get("lastname")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmpassword")

    return redirect("/")


# login route

@app.route("/login", methods=["GET", "POST"])
def login():

    # for GET
    if request.method == "GET":
        return render_template("login.html")
