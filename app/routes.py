from flask import render_template, request, redirect, session, jsonify, flash, url_for
from flask.wrappers import Response
from typing import Union, Tuple
from app.helpers import apology, login_required, hash_password, check_password, check_email, generate_password, encrypt_password, decrypt_password  # type: ignore
from app import app, db


@app.errorhandler(404)
def page_not_found(e):
    """404 error handler"""
    return render_template('404.html'), 404


@app.route("/")
def index() -> str:
    """renders the home page"""
    logged_in = "user_id" in session  # bool flag to check if user is logged in
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

@app.route("/manager", methods=["GET", "POST"])
@login_required
def manager():
    """Enables the user to manage their passwords"""

    user_email = db.execute(
        "SELECT email FROM users WHERE id = ?", session["user_id"])
    user_email = user_email[0]["email"]

    # for POST
    if request.method == "POST":
        # check for user action:

        # for adding password
        if 'add' in request.form:

            # variables to store form data
            website = request.form.get("website")
            username = request.form.get("username")
            password = request.form.get("password")
            encrypted_pw = encrypt_password(password)

            # store the password in the database
            try:
                db.execute("INSERT INTO manager (user_email, website, username, password) VALUES (?, ?, ?, ?)",
                           user_email, website, username, encrypted_pw)
            except Exception as e:
                return apology(str(e), 400)

            flash("Password added successfully!")
            return redirect(url_for('manager'))
            # for editing password
        elif 'edit' in request.form:

            password_id = request.form.get("id")
            new_password = request.form.get("password")

            new_encrypted_pw = encrypt_password(new_password)

            # update the password in the database
            try:
                db.execute("UPDATE manager SET password = ? WHERE id = ? AND user_email = ?",
                           new_encrypted_pw, password_id, user_email)
            except Exception as e:
                return apology(str(e), 400)

            flash("Password updated successfully!")
            return redirect(url_for('manager'))
        # for deleting password
        elif 'delete' in request.form:
            password_id = request.form.get("id")

            # delete the password from the database
            try:
                db.execute("DELETE FROM manager WHERE id = ? AND user_email = ?",
                           password_id, user_email)
            except Exception as e:
                return apology(str(e), 400)

            flash("Password deleted successfully!")
            return redirect(url_for("manager"))  # Redirect to avoid form resubmission

    # fetch the user's passwords from the database (GET)

    data = db.execute(
        "SELECT id, website, username, password FROM manager WHERE user_email = ?", user_email)

    decrypted_passwords_list = []  # empty list to store decrypted passwords

    for row in data:
        decrypted_password = decrypt_password(row['password'])
        decrypted_passwords_list.append({
            'id': row['id'],
            'website': row['website'],
            'username': row['username'],
            'password': decrypted_password
        })

    return render_template("manage_password.html", passwords=decrypted_passwords_list)
