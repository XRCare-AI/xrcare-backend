""" User model and default users (same role as Open Coding Society flask model/user.py) """
import json
import os
import re
from datetime import datetime, timezone

from sqlalchemy import inspect, text
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from __init__ import app, db


EMAIL_PATTERN = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')
PHONE_PATTERN = re.compile(r'^\+?[\d\s().-]{7,20}$')
UID_PATTERN = re.compile(r'^[A-Za-z0-9._-]{3,40}$')


class User(db.Model):
    """
    User Model

    Attributes:
        id (Column): Primary key.
        _name (Column): The user's full name.
        _uid (Column): Unique username, used to log in.
        _email (Column): Optional unique email address, can also be used to log in.
        _phone (Column): Optional phone number.
        _password (Column): Hashed password.
        _role (Column): "User" or "Admin".
        token_version (Column): Bumped on password change so older login tokens stop working.
        created_at (Column): When the account was created.
        _survey (Column): JSON answers to the first-login survey ({question_id: answer}), or None if not taken.
        survey_completed_at (Column): When the survey was answered.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _uid = db.Column(db.String(255), unique=True, nullable=False)
    _email = db.Column(db.String(255), unique=True, nullable=True)
    _phone = db.Column(db.String(32), unique=False, nullable=True)
    _password = db.Column(db.String(255), unique=False, nullable=False)
    _role = db.Column(db.String(20), default="User", nullable=False)
    token_version = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    _survey = db.Column(db.Text, nullable=True)
    survey_completed_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, name, uid, password=None, email=None, phone=None, role="User"):
        self._name = name
        self._uid = uid.strip().lower()
        self._email = email.strip().lower() if email else None
        self._phone = phone.strip() if phone else None
        self._role = role
        self.token_version = 0
        self.set_password(password or app.config['DEFAULT_PASSWORD'])

    @property
    def name(self):
        return self._name

    @property
    def uid(self):
        return self._uid

    @property
    def email(self):
        return self._email

    @property
    def phone(self):
        return self._phone

    @property
    def role(self):
        return self._role

    @property
    def survey(self):
        return json.loads(self._survey) if self._survey else None

    def save_survey(self, answers):
        self._survey = json.dumps(answers)
        self.survey_completed_at = datetime.now(timezone.utc)
        db.session.commit()
        return self

    def is_admin(self):
        return self._role == "Admin"

    def set_password(self, password):
        """ Hash the password and invalidate any login tokens issued before the change """
        self._password = generate_password_hash(password, "pbkdf2:sha256", salt_length=10)
        self.token_version = (self.token_version or 0) + 1

    def is_password(self, password):
        return check_password_hash(self._password, password)

    @staticmethod
    def validate(name=None, uid=None, email=None, phone=None, password=None):
        """ Returns an error message for the first invalid field supplied, or None """
        if name is not None and not name.strip():
            return 'Name is required'
        if uid is not None and not UID_PATTERN.match(uid.strip()):
            return 'Username must be 3-40 letters, numbers, dots, dashes or underscores'
        if email and not EMAIL_PATTERN.match(email.strip()):
            return 'Please enter a valid email address'
        if phone and not PHONE_PATTERN.match(phone.strip()):
            return 'Please enter a valid phone number'
        if password is not None and len(password) < 6:
            return 'Password must be at least 6 characters'
        return None

    def create(self):
        """ Add the user to the database; returns None if the username or email is taken """
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.rollback()
            return None

    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "uid": self.uid,
            "email": self.email or "",
            "phone": self.phone or "",
            "role": self.role,
            "is_admin": self.is_admin(),
            "username_locked": self.is_seeded(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "survey": self.survey,
            "needs_survey": self._survey is None,
        }

    def is_seeded(self):
        """ Accounts listed in ADMINS/USERS (__init__.py) are recreated by username on every start,
        so their username cannot change (renaming would bring back a second account with the old name) """
        return any(uid == self._uid for _, uid in app.config['ADMINS'] + app.config['USERS'])

    def update(self, inputs):
        """ Update name, username, email and/or phone from a dict; returns None if the username or email is taken """
        if 'uid' in inputs:
            self._uid = inputs['uid'].strip().lower()
        if 'name' in inputs:
            self._name = inputs['name'].strip()
        if 'email' in inputs:
            self._email = inputs['email'].strip().lower() or None
        if 'phone' in inputs:
            self._phone = inputs['phone'].strip() or None
        try:
            db.session.commit()
            return self
        except IntegrityError:
            db.session.rollback()
            return None

    def delete(self):
        db.session.delete(self)
        db.session.commit()


def add_missing_columns():
    """ create_all() never changes an existing table: add columns introduced after the database was made """
    existing = {column['name'] for column in inspect(db.engine).get_columns('users')}
    added = {'_survey': 'TEXT', 'survey_completed_at': 'DATETIME'}
    with db.engine.begin() as connection:
        for name, sql_type in added.items():
            if name not in existing:
                connection.execute(text(f'ALTER TABLE users ADD COLUMN {name} {sql_type}'))


def initUsers():
    """
    Create the database tables and the accounts listed in ADMINS and USERS (__init__.py).
    New accounts get their starting password from <UID>_PASSWORD in .env; existing accounts keep
    their password and profile, but get the role from the list they are in.
    """
    with app.app_context():
        db.create_all()
        add_missing_columns()
        seeds = [(name, uid, 'Admin') for name, uid in app.config['ADMINS']]
        seeds += [(name, uid, 'User') for name, uid in app.config['USERS']]
        for name, uid, role in seeds:
            user = User.query.filter_by(_uid=uid).first()
            if user is None:
                password = os.environ.get(uid.upper() + '_PASSWORD') or app.config['DEFAULT_PASSWORD']
                User(name=name, uid=uid, password=password, role=role).create()
            elif user.role != role:
                user._role = role
                db.session.commit()
