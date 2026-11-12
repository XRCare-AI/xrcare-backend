"""
XRCare AI API - app setup (same role as Open Coding Society flask __init__.py)

Creates the Flask app, CORS, and database objects that model/ and api/ import.
"""
import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


# Load environment variables from .env, no matter which folder main.py is run from
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# Setup of key Flask object (app); instance folder holds the database
app = Flask(__name__, instance_path=os.path.join(basedir, 'instance'))

# Configure Flask Port, default to 8620 (frontend runs on 4100)
app.config['FLASK_PORT'] = int(os.environ.get('FLASK_PORT') or 8620)

# Allowed servers for cross-origin resource sharing (CORS)
allowed_origins = [
    'http://localhost:4100',
    'http://127.0.0.1:4100',
    'https://xrcare-ai.github.io',  # Deployed frontend (xrcare-frontend repo on GitHub Pages)
]
# Any other deployed frontend(s), comma separated in .env
allowed_origins += [o.strip() for o in (os.environ.get('ALLOWED_ORIGINS') or '').split(',') if o.strip()]

cors = CORS(
    app,
    supports_credentials=True,
    origins=allowed_origins,
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
)

# Accounts created on start: (name, uid). Each starting password is read from <UID>_PASSWORD
# in .env (e.g. TOBY_PASSWORD), falling back to DEFAULT_PASSWORD.
# Admins can edit the site's content; users can log in to the site.
app.config['ADMINS'] = [
    ('Toby', 'toby'),
    ('Adya Shipekar', 'adyashipekar'),
]
app.config['USERS'] = [
    ('Rohan Chandra', 'rohanchandra'),
]
# Password for any seeded account without its own <UID>_PASSWORD
app.config['DEFAULT_PASSWORD'] = os.environ.get('DEFAULT_PASSWORD') or 'password'

# Browser settings
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'xrcare-flask-secret-key-set-SECRET_KEY-in-env'
# XRCare-specific cookie names so they never collide with other Flask apps on the same domain
app.config['JWT_TOKEN_NAME'] = os.environ.get('JWT_TOKEN_NAME') or 'xrcare_jwt'
app.config['JWT_TOKEN_MAX_AGE'] = int(os.environ.get('JWT_TOKEN_MAX_AGE') or 604800)  # 1 week
# Production = frontend on GitHub Pages + backend on its own HTTPS domain,
# which needs SameSite=None; Secure cookies (same switch OCS uses)
app.config['IS_PRODUCTION'] = (os.environ.get('IS_PRODUCTION') or 'false').lower() == 'true'
# Admin login page session cookie: HTTPS-only when deployed
app.config['SESSION_COOKIE_SECURE'] = app.config['IS_PRODUCTION']
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_NAME'] = 'xrcare_session'

# Database settings - SQLite in instance/volumes/ (OCS layout)
dbName = 'user_management'
os.makedirs(os.path.join(app.instance_path, 'volumes'), exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(app.instance_path, 'volumes', dbName + '.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
