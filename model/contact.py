""" Contact message model (same pattern as model/user.py)

Messages sent from the "Ready to Transform Your Care Team?" form at the bottom of every page.
FIELDS describes that form (labels, order, widths) so the frontend draws it from here.
"""
from datetime import datetime, timezone

from __init__ import app, db


# The form on xrcare.ai, in order. width is the share of a row: "third", "two-thirds" or "full";
# first starts a new row. type is the input type ("textarea" for a multi-line box).
# (xrcare.ai's form also has a hidden "Organization First Phone" field: a spam trap, not a real field.)
FIELDS = [
    {'name': 'first_name', 'label': 'First Name', 'type': 'text', 'required': True, 'width': 'third', 'first': True},
    {'name': 'last_name', 'label': 'Last Name', 'type': 'text', 'required': True, 'width': 'third'},
    {'name': 'phone', 'label': 'Phone Number', 'type': 'text', 'required': False, 'width': 'third'},
    {'name': 'organization', 'label': 'Organization', 'type': 'text', 'required': False, 'width': 'two-thirds', 'first': True},
    {'name': 'email', 'label': 'Email', 'type': 'email', 'required': True, 'width': 'third'},
    {'name': 'comment', 'label': 'Comment', 'type': 'textarea', 'required': False, 'width': 'full', 'first': True},
]
MAX_CHARS = {'comment': 2000}
DEFAULT_MAX_CHARS = 255


class ContactMessage(db.Model):
    """
    ContactMessage Model

    Attributes:
        id (Column): Primary key.
        _first_name, _last_name (Column): Sender's name.
        _phone (Column): Optional phone number.
        _organization (Column): Optional organization.
        _email (Column): Email to reply to.
        _comment (Column): Optional message.
        _handled (Column): Set by an admin once the message has been answered.
        created_at (Column): When it was sent.
    """
    __tablename__ = 'contact_messages'

    id = db.Column(db.Integer, primary_key=True)
    _first_name = db.Column(db.String(255), nullable=False)
    _last_name = db.Column(db.String(255), nullable=False)
    _phone = db.Column(db.String(64), nullable=True)
    _organization = db.Column(db.String(255), nullable=True)
    _email = db.Column(db.String(255), nullable=False)
    _comment = db.Column(db.Text, nullable=True)
    _handled = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __init__(self, first_name, last_name, email, phone=None, organization=None, comment=None):
        self._first_name = first_name.strip()
        self._last_name = last_name.strip()
        self._email = email.strip().lower()
        self._phone = (phone or '').strip() or None
        self._organization = (organization or '').strip() or None
        self._comment = (comment or '').strip() or None

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def set_handled(self, handled):
        self._handled = bool(handled)
        db.session.commit()
        return self

    def read(self):
        return {
            "id": self.id,
            "first_name": self._first_name,
            "last_name": self._last_name,
            "name": f"{self._first_name} {self._last_name}",
            "phone": self._phone or "",
            "organization": self._organization or "",
            "email": self._email,
            "comment": self._comment or "",
            "handled": self._handled,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


def initContacts():
    """ Create the contact_messages table """
    with app.app_context():
        db.create_all()
