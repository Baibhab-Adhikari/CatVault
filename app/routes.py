from flask import render_template, redirect, url_for, request, flash, session
from app import app 


@app.route("/")
def index():
    return render_template("index.html")