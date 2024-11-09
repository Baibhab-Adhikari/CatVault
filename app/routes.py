from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


# homepage route

@app.route('/')
def index():
    return render_template("/CatVault/templates/index.html")

# login route

@app.route('/login', methods=["GET", "POST"])
def login():
    pass
