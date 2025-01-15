from app import create_app, db
from app.models import Users, Manager


app = create_app()  # create the app


with app.app_context():
    """Create the tables in the database"""
    db.create_all()
    
    print("Tables created successfully")
