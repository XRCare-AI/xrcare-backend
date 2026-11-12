""" Contact API: the "Ready to Transform Your Care Team?" form (same pattern as api/user.py)

GET  /api/contact/form   the form's fields (model/contact.py FIELDS)
POST /api/contact        send {first_name, last_name, email, phone?, organization?, comment?}
GET  /api/contact        Admin only: every message, newest first
PUT  /api/contact        Admin only: mark a message handled {id, handled}
"""
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource

from __init__ import db
from api.jwt_authorize import token_required
from model.contact import ContactMessage, FIELDS, MAX_CHARS, DEFAULT_MAX_CHARS
from model.user import EMAIL_PATTERN


contact_api = Blueprint('contact_api', __name__, url_prefix='/api')
api = Api(contact_api)


class ContactAPI:
    class _CRUD(Resource):
        def post(self):
            """ Send a message; anyone can send one """
            body = request.get_json(silent=True) or {}
            values = {f['name']: str(body.get(f['name']) or '').strip() for f in FIELDS}
            for field in FIELDS:
                value = values[field['name']]
                if field['required'] and not value:
                    return {"message": f"{field['label']} is required"}, 400
                limit = MAX_CHARS.get(field['name'], DEFAULT_MAX_CHARS)
                if len(value) > limit:
                    return {"message": f"{field['label']} can be up to {limit} characters"}, 400
            if not EMAIL_PATTERN.match(values['email']):
                return {"message": "Please enter a valid email address"}, 400

            ContactMessage(**values).create()
            return {"message": "Thanks for contacting us! We will be in touch with you shortly."}, 201

        @token_required("Admin")
        def get(self):
            messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
            return jsonify([m.read() for m in messages])

        @token_required("Admin")
        def put(self):
            body = request.get_json(silent=True) or {}
            message = db.session.get(ContactMessage, body.get('id') or 0)
            if message is None:
                return {"message": "Message not found"}, 404
            return jsonify(message.set_handled(body.get('handled', True)).read())

    class _Form(Resource):
        def get(self):
            return jsonify(FIELDS)

    api.add_resource(_CRUD, '/contact')
    api.add_resource(_Form, '/contact/form')
