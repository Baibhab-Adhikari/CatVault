from flask import render_template, request, redirect, session, jsonify, flash
from flask.wrappers import Response
from typing import Union, Tuple
from app.helpers import apology, login_required, hash_password, check_password, check_email, generate_password  # type: ignore
from app import app, db


@app.errorhandler(404)
def page_not_found(e):
    """404 error handler"""
    return render_template('404.html'), 404


@app.route("/")
def index() -> str:
    """renders the home page"""
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register() -> Union[str, tuple[str, int], Response]:
    """Registration for new user"""

    # for GET:
    if request.method == 'GET':
        return render_template("register.html")

    # for POST:
    elif request.method == "POST":

        # Variables to store info with correct type annotations
        first_name: Union[str, None] = request.form.get("firstname")
        last_name: Union[str, None] = request.form.get("lastname")
        email: Union[str, None] = request.form.get("email")
        password: Union[str, None] = request.form.get("password")
        confirm_password: Union[str, None] = request.form.get(
            "confirmpassword")

        # Input validation
        if not first_name or not last_name or not email:
            return apology("Please enter details correctly!", 400)

        # Password validation
        if not password or not confirm_password:
            return apology("Please enter a password!", 400)

        # Check if the passwords match
        if password != confirm_password:
            return apology("Passwords do not match!", 400)

        # email validation
        if not check_email(email):
            return apology("Please enter a valid email address!", 400)

        # hash the password
        hash = hash_password(password)

        # try to store the user in the database
        try:
            db.execute("INSERT INTO users (first_name, last_name, email, hashed_password) VALUES (?, ?, ?, ?)",
                       first_name, last_name, email, hash)
        except Exception as e:
            return apology(str(e), 400)

    return redirect("/login")  # type: ignore


# login route

@app.route("/login", methods=["GET", "POST"])
def login() -> Union[Tuple[str, int], Response]:

    # for POST
    if request.method == "POST":

        # variables to store form data
        email: Union[str, None] = request.form.get("email")
        password: Union[str, None] = request.form.get("password")

        # input validation

        if not email or not password:
            return apology("Please enter email and password!", 400)

        # fetching the user by their email
        try:
            user = db.execute("SELECT * from users WHERE email = ?", email)
            if not user:
                return apology("Invalid email or password!", 400)
            hashed_pw = user[0]["hashed_password"]
        except Exception:
            return apology("An error occurred, please try again later.", 400)

        # check for password match
        if not check_password(password, hashed_pw):
            return apology("Invalid password!", 400)

        session["user_id"] = user[0]["id"]  # store user in the session

        flash("You have been logged in!")  # flash user to update them

        return redirect("/")  # type: ignore

    # for GET

    return render_template("login.html")  # type: ignore


# password generator route
@app.route("/generate", methods=["GET", "POST"])
@login_required
def generate() -> Union[str, Response, Tuple[str, int]]:
    """Generates a random password"""

    # for POST
    if request.method == "POST":
        # variables to store form data

        length = request.form.get("rangevalue")
        uppercase = request.form.get("uppercase")
        lowercase = request.form.get("lowercase")
        numbers = request.form.get("numbers")
        symbols = request.form.get("symbols")

        # generate the password based on the user specification

        generated_password = generate_password(
            length, uppercase, lowercase, numbers, symbols)

        # return the password as a json response to the client
        return jsonify(password=generated_password)

    # for GET
    return render_template("generate_password.html")

# logout route


@app.route("/logout")
@login_required
def logout() -> Response:
    """Logs out the user"""
    session.clear()
    flash("You have been logged out.")  # flash user to update them
    return redirect("/login")  # type: ignore


# route for password manager

@app.route("/manager")
@login_required
def manager():
    """Enables the user to manage their passwords"""