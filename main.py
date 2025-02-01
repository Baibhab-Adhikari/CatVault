from app import create_app
from flask import Flask

flask_app: Flask = create_app()


if __name__ == "__main__":
    flask_app.run(debug=flask_app.config["DEBUG"])
