import os
from app import app, db, Violation

# Get the folder path where app.py is located
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'traffic_violations.db')

with app.app_context():
    # This command creates the .db file
    db.create_all()

    # Check if we created it successfully
    if os.path.exists(db_path):
        print(f"SUCCESS: Database created at {db_path}")
    else:
        print("ERROR: Database file was not created.")