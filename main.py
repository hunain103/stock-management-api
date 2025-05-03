import os
import socket
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
# create the app
app = Flask(__name__)
# setup a secret key, required by sessions
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a secret key"
# configure the database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
# initialize the app with the extension, flask-sqlalchemy >= 3.0.x
db.init_app(app)

with app.app_context():
    # Create all database tables
    db.create_all()

@app.route('/')
def hello():
    return 'Hello from Flask! Visit /django to access the Django application.'

# Try to run on port 5001 first, if that fails, try 5002, and so on
def find_available_port(start_port=5001, max_attempts=10):
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('0.0.0.0', port))
                return port
            except socket.error:
                continue
    # If all attempts fail, return None
    return None

if __name__ == '__main__':
    port = find_available_port()
    if port:
        print(f"Flask server running on port {port}")
        app.run(host='0.0.0.0', port=port, debug=True)
    else:
        print("Could not find an available port. Flask server not started.")

