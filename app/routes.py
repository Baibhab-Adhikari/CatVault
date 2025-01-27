from typing import Union, Tuple

from flask import render_template, request, redirect, session, jsonify, flash, url_for
from flask.wrappers import Response
from flask_mail import Message  # type: ignore
from sqlalchemy.exc import IntegrityError

from app import mail  # type: ignore
from app.helpers import login_required, hash_password, check_password, check_email, generate_password, \
    encrypt_password, decrypt_password  # type: ignore

from app.models import Users, Manager  # type: ignore


def register_routes(app, db):
    @app.errorhandler(404)
    def page_not_found(e):
        """404 error handler"""
        return render_template('404.html'), 404

    @app.route("/")
    def index() -> str:
        """renders the home page"""
        # flash("Welcome to the password manager!")
        return render_template("index.html")

    @app.route("/register", methods=["GET", "POST"])
    def register() -> Union[str, tuple[str, int], Response]:  # type: ignore
        """Registration for new user"""

        # for GET:
        if request.method == 'GET':
            return render_template("register.html")

        # for POST:
        elif request.method == "POST":

            # Variables to store info
            first_name: Union[str, None] = request.form.get("firstname")
            last_name: Union[str, None] = request.form.get("lastname")
            email: Union[str, None] = request.form.get("email")
            password: Union[str, None] = request.form.get("password")
            confirm_password: Union[str, None] = request.form.get(
                "confirmpassword")

            # Input validation
            if not first_name or not last_name or not email:
                flash("Please fill in all fields!")

            # Password validation
            if not password or not confirm_password:
                flash("Please enter a password!")

            # Check if the passwords match
            if password != confirm_password:
                flash("Passwords do not match!")

            # email validation
            if not check_email(email):  # type: ignore
                flash("Please enter a valid email address!")

            # hash the password
            hashed_pw: str = hash_password(password)  # type: ignore

            # create a new User instance
            new_user = Users(
                first_name=first_name,
                last_name=last_name,
                email=email,
                hashed_password=hashed_pw

            )

            # Try to add the user to the database
        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Email already in use!")
            return redirect("/register")  # type: ignore

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
                flash("Please enter email and password!")
                # redirect users to login route again
                return redirect("/login")  # type: ignore

            # fetching the user by their email
            user = Users.query.filter_by(email=email).first()

            if not user:
                flash("Invalid email or password!")
                return redirect("/login")  # type: ignore

            # check for password match
            if not check_password(password, user.hashed_password):  # type: ignore
                flash("Invalid password!")
                return redirect("/login")  # type: ignore

            session["user_id"] = user.id  # store user in the session

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

    # # logout route

    # @app.route("/logout")
    # @login_required
    # def logout() -> Response:
    #     """Logs out the user"""
    #     session.clear()
    #     flash("You have been logged out.")  # flash user to update them
    #     return redirect("/login")  # type: ignore

    # # route for password manager

    # @app.route("/manager", methods=["GET", "POST"])
    # @login_required
    # def manager():
    #     """Enables the user to manage their passwords"""

    #     user_email = db.execute(
    #         "SELECT email FROM users WHERE id = ?", session["user_id"])
    #     user_email = user_email[0]["email"]

    #     # for POST
    #     if request.method == "POST":
    #         # check for user action:

    #         # for adding password
    #         if 'add' in request.form:

    #             # variables to store form data
    #             website = request.form.get("website")
    #             username = request.form.get("username")
    #             password = request.form.get("password")
    #             encrypted_pw = encrypt_password(password)

    #             # store the password in the database
    #             try:
    #                 db.execute("INSERT INTO manager (user_email, website, username, password) VALUES (?, ?, ?, ?)",
    #                            user_email, website, username, encrypted_pw)
    #             except Exception as e:
    #                 flash(str(e), 400)

    #             flash("Password added successfully!")
    #             return redirect(url_for('manager'))
    #             # for editing password
    #         elif 'edit' in request.form:

    #             password_id = request.form.get("id")
    #             new_password = request.form.get("password")

    #             new_encrypted_pw = encrypt_password(new_password)

    #             # update the password in the database
    #             try:
    #                 db.execute("UPDATE manager SET password = ? WHERE id = ? AND user_email = ?",
    #                            new_encrypted_pw, password_id, user_email)
    #             except Exception as e:
    #                 flash(str(e), 400)

    #             flash("Password updated successfully!")
    #             return redirect(url_for('manager'))
    #         # for deleting password
    #         elif 'delete' in request.form:
    #             password_id = request.form.get("id")

    #             # delete the password from the database
    #             try:
    #                 db.execute("DELETE FROM manager WHERE id = ? AND user_email = ?",
    #                            password_id, user_email)
    #             except Exception as e:
    #                 flash(str(e), 400)

    #             flash("Password deleted successfully!")
    #             # Redirect to avoid form resubmission
    #             return redirect(url_for("manager"))

    #     # fetch the user's passwords from the database (GET)

    #     data = db.execute(
    #         "SELECT id, website, username, password FROM manager WHERE user_email = ?", user_email)

    #     decrypted_passwords_list = []  # empty list to store decrypted passwords

    #     for row in data:
    #         decrypted_password = decrypt_password(row['password'])
    #         decrypted_passwords_list.append({
    #             'id': row['id'],
    #             'website': row['website'],
    #             'username': row['username'],
    #             'password': decrypted_password
    #         })

    #     return render_template("manage_password.html", passwords=decrypted_passwords_list)
