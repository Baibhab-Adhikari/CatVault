import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

uri = os.getenv("DATABASE_URI")

if not uri:
    raise ValueError("DATABASE_URI environment variable is not set.")

engine = create_engine(uri)
connection = engine.connect()
print("Connection successful!")
connection.close()
