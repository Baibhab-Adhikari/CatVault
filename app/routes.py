from typing import Union, Tuple

from flask import render_template, request, redirect, session, jsonify, flash, url_for
from flask.wrappers import Response
from flask_mail import Message  # type: ignore
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from app import mail  # type: ignore
from app.helpers import login_required, hash_password, check_password, check_email, generate_password, decrypt_password, encrypt_password  # type: ignore
from app.models import Users, Manager, Contact  # type: ignore


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
                flash("Please fill in all fields!", 'danger')

            # Password validation
            if not password or not confirm_password:
                flash("Please enter a password!", 'danger')

            # Check if the passwords match
            if password != confirm_password:
                flash("Passwords do not match!", 'danger')

            # email validation
            if not check_email(email):  # type: ignore
                flash("Please enter a valid email address!", 'danger')

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
            flash("Email already in use!", 'warning')
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
                flash("Please enter email and password!", 'danger ')
                # redirect users to login route again
                return redirect("/login")  # type: ignore

            # fetching the user by their email
            user = Users.query.filter_by(email=email).first()

            if not user:
                flash("Invalid email or password!", 'danger')
                return redirect("/login")  # type: ignore

            # check for password match
            if not check_password(password, user.hashed_password):  # type: ignore
                flash("Invalid password!", 'danger')
                return redirect("/login")  # type: ignore

            session["user_id"] = user.id  # store user in the session

            # flash user to update them
            flash("You have been logged in!", 'success')

            return redirect("/")  # type: ignore

        # for GET

        return render_template("login.html")  # type: ignore

    # password generator route / API
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
        # flash user to update them
        flash("You have been logged out.", 'success')
        return redirect("/login")  # type: ignore

    # route for password manager

    @app.route("/manager", methods=["GET", "POST"])
    @login_required
    def manager():
        """Enables the user to manage their passwords"""

        # check if user is logged in

        user_id = session.get("user_id")

        if not user_id:
            flash("Please login to view your stored passwords!", 'warning')
            return redirect("/login")

        # fetch the user's data from the database
        user = Users.query.get(user_id)

        if not user:
            flash("User not found!", 'danger')
            return redirect("/login")

        user_email = user.email

        # for POST
        try:
            # Adding a new password
            if "add" in request.form:
                website = request.form.get("website")
                username = request.form.get("username")
                password = request.form.get("password")

                # validating the inputs
                if not website or not username or not password:
                    flash('Please fill in all fields!', 'danger')
                    return redirect('/manager')

                encrypted_pw = encrypt_password(password)

                new_entry = Manager(
                    user_email=user_email,
                    website=website,
                    username=username,
                    password=encrypted_pw
                )
                db.session.add(new_entry)
                db.session.commit()
                flash("Password added successfully!", "success")

            # Editing an existing password
            elif "edit" in request.form:
                password_id = request.form.get("id")
                new_password = request.form.get("password")

                entry = Manager.query.filter_by(id=password_id, user_email=user_email).first()
                if entry:
                    entry.password = encrypt_password(new_password)
                    db.session.commit()
                    flash("Password updated successfully!", "success")
                else:
                    flash("Password entry not found!", "danger")

            # Deleting a password
            elif "delete" in request.form:
                password_id = request.form.get("id")

                entry = Manager.query.filter_by(id=password_id, user_email=user_email).first()
                if entry:
                    db.session.delete(entry)
                    db.session.commit()
                    flash("Password deleted successfully!", "success")
                else:
                    flash("Password entry not found!", "danger")

        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", "danger")

            return redirect("/manager")

        # Fetch user's saved passwords
        stored_passwords = Manager.query.filter_by(user_email=user_email).all()

        decrypted_passwords_list = [
            {
                "id": row.id,
                "website": row.website,
                "username": row.username,
                "password": decrypt_password(row.password),
            }
            for row in stored_passwords
        ]

        return render_template("manage_password.html", passwords=decrypted_passwords_list)

    # route for Account Dashboard
    @app.route('/account')
    @login_required
    def account_dashboard():
        """Displays the user's account dashboard"""

        # check if user is logged in

        user_id = session.get("user_id")

        if not user_id:
            flash("Please login to view your account!", 'warning')
            return redirect("/login")

        # fetch the user's data from the database
        user = Users.query.filter_by(id=user_id).first()

        if not user:
            flash("User not found!", 'danger')
            return redirect("/login")

        return render_template('account.html', user=user)

    @app.route('/contactus', methods=["GET", "POST"])
    def contactus() -> Union[str, Response]:
        """Contact us form"""

        if request.method == "POST":
            name = request.form.get("name")
            email = request.form.get("email")
            message = request.form.get("message")

            if not name or not email or not message:
                flash("Please fill in all the fields!", 'danger')
                return redirect("/contactus")  # type: ignore

            try:
                # start the transaction
                db.session.begin()
                # create a new contact instance
                new_contact = Contact(
                    name=name,
                    email=email,
                    message=message
                )
                db.session.add(new_contact)
                db.session.commit()  # commit the transaction

            except Exception as e:
                db.session.rollback()  # rollback transaction in case of error
                flash(str(e), 'danger')  # type: ignore
                return redirect("/contactus")  # type: ignore

            # Send email with the message
            msg = Message("New Contact Us Message - CatVault", recipients=[
                app.config['MAIL_USERNAME']])
            msg.body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            mail.send(msg)

            db.session.commit()  # commit transaction

            flash("Message sent successfully!", 'success')
            return redirect("/contactus")  # type: ignore

        return render_template("contactus.html")  # for GET request

    # route for profile details display
    @app.route('/profile')
    @login_required
    def profile():
        """Fetches user's profile"""

        user_id = session.get("user_id")

        if not user_id:
            flash("Please login to view your profile!", 'warning')
            return redirect("/login")

        user = Users.query.filter_by(id=user_id).first()

        if not user:
            flash("User not found!", 'danger')
            return redirect("/login")

        return render_template("profile.html", user=user)

    # route for updating user profile
    # noinspection SqlNoDataSourceInspection
    @app.route('/update_profile', methods=['POST'])
    def update_profile():
        """Update profile route to update user's profile"""

        # check for user in the session
        user_id = session.get("user_id")
        if not user_id:
            flash("Please login to update your profile!", 'warning')
            return redirect("/login")

        # get new details from the form
        new_first_name = request.form.get("firstname")
        new_last_name = request.form.get("lastname")
        new_email = request.form.get("email")
        new_password = request.form.get("new_password")
        confirm_new_password = request.form.get("confirm_password")

        # email validation
        if not new_email and check_email(new_email):
            flash("Please enter a valid email address!", 'danger')
            return redirect("/profile")
        # password validation if provided
        if new_password and new_password != confirm_new_password:
            flash("Passwords do not match!", 'danger')
            return redirect("/profile")

        # try to update user details in the database
        try:
            db.session.begin()  # begin transaction
            update_fields = {}
            if new_first_name:
                update_fields['first_name'] = new_first_name
            if new_last_name:
                update_fields['last_name'] = new_last_name
            if new_email:
                update_fields['email'] = new_email
            if new_password:
                update_fields['hashed_password'] = hash_password(new_password)

            if update_fields:
                set_clause = ", ".join(
                    [f"{key} = :{key}" for key in update_fields.keys()])
                update_fields['id'] = user_id
                db.session.execute(
                    text(f'UPDATE users SET {set_clause} WHERE id = :id'),
                    update_fields
                )

            db.session.commit()  # Commit transaction
            flash("Profile updated successfully!", 'success')
            return redirect('/profile')

        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}", 'danger')
            return redirect("/profile")
