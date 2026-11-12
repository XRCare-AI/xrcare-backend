""" User API: sign up, log in/out, profile, admin user list (same role as Open Coding Society flask api/user.py) """
from datetime import datetime, timedelta, timezone

import jwt
from flask import Blueprint, request, current_app, g, jsonify
from flask_restful import Api, Resource

from api.jwt_authorize import token_required
from model.site import site_settings
from model.user import User


user_api = Blueprint('user_api', __name__, url_prefix='/api')
api = Api(user_api)


def set_token_cookie(resp, token, max_age):
    if current_app.config["IS_PRODUCTION"]:
        resp.set_cookie(current_app.config["JWT_TOKEN_NAME"], token, max_age=max_age,
                        secure=True, httponly=True, path='/', samesite='None')
    else:
        resp.set_cookie(current_app.config["JWT_TOKEN_NAME"], token, max_age=max_age,
                        secure=False, httponly=True, path='/', samesite='Lax')
    return resp


def login_response(user, status=200):
    token = jwt.encode(
        {
            "_uid": user.uid,
            "token_version": user.token_version,
            "exp": datetime.now(timezone.utc) + timedelta(seconds=current_app.config["JWT_TOKEN_MAX_AGE"]),
        },
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )
    resp = jsonify({"message": f"Authentication for {user.uid} successful", "user": user.read()})
    resp.status_code = status
    return set_token_cookie(resp, token, current_app.config["JWT_TOKEN_MAX_AGE"])


def validate_survey(survey, answers):
    """ Every question needs a valid answer: one option id, or a list of ids for multiple-choice questions """
    for question in survey.get('questions', []):
        options = {option['id'] for option in question['options']}
        answer = answers.get(question['id'])
        if question.get('multiple'):
            limit = question.get('max') or len(options)
            if not isinstance(answer, list) or not answer or not set(answer) <= options or len(set(answer)) > limit:
                return f"Please answer: {question['title']}"
        elif answer not in options:
            return f"Please answer: {question['title']}"
    unknown = set(answers) - {question['id'] for question in survey.get('questions', [])}
    if unknown:
        return f"Unknown question: {sorted(unknown)[0]}"
    return None


class UserAPI:
    class _ID(Resource):  # Current user identification
        @token_required()
        def get(self):
            return jsonify(g.current_user.read())

    class _CRUD(Resource):  # Users API operation for Create, Read, Update, Delete
        def post(self):
            """ Sign up: create a new account and log it in """
            body = request.get_json(silent=True) or {}
            fields = {k: (body.get(k) or '').strip() for k in ('name', 'uid', 'email', 'phone')}
            password = body.get('password') or ''

            error = User.validate(password=password, **fields)
            if error:
                return {"message": error}, 400

            user = User(password=password, **fields).create()
            if user is None:
                return {"message": "That username or email is already registered"}, 409
            return login_response(user, 201)

        @token_required("Admin")
        def get(self):
            """ Admin only: list every user """
            return jsonify([user.read() for user in User.query.order_by(User.id).all()])

        @token_required()
        def put(self):
            """ Update the current user's name, username, email, phone and/or password """
            user = g.current_user
            body = request.get_json(silent=True) or {}
            updates = {k: str(body[k]) for k in ('name', 'uid', 'email', 'phone') if k in body}
            if updates.get('uid', '').strip().lower() == user.uid:
                del updates['uid']   # unchanged
            if 'uid' in updates and user.is_seeded():
                return {"message": "This account's username can't be changed"}, 400

            error = User.validate(**updates)
            if error:
                return {"message": error}, 400

            new_password = body.get('new_password')
            if new_password:
                if not user.is_password(body.get('current_password') or ''):
                    return {"message": "Current password is incorrect"}, 403
                error = User.validate(password=new_password)
                if error:
                    return {"message": error}, 400
                user.set_password(new_password)

            if user.update(updates) is None:
                return {"message": "That username or email is already taken"}, 409
            # The login cookie names the user and its token_version, so a new username or password needs a fresh one
            return login_response(user) if new_password or 'uid' in updates else jsonify(user.read())

        @token_required("Admin")
        def delete(self):
            """ Admin only: delete a user by uid """
            body = request.get_json(silent=True) or {}
            user = User.query.filter_by(_uid=(body.get('uid') or '').lower()).first()
            if user is None:
                return {"message": "User not found"}, 404
            if user.id == g.current_user.id:
                return {"message": "Admins cannot delete their own account"}, 400
            user.delete()
            return {"message": f"Deleted user {user.uid}"}

    class _Security(Resource):  # Login and logout
        def post(self):
            """ Log in with username (or email) and password """
            body = request.get_json(silent=True) or {}
            uid = (body.get('uid') or '').strip().lower()
            if not uid:
                return {"message": "User ID is missing"}, 401
            password = body.get('password')
            if not password:
                return {"message": "Password is missing"}, 401

            user = User.query.filter((User._uid == uid) | (User._email == uid)).first()
            if user is None or not user.is_password(password):
                return {"message": "Invalid user id or password"}, 401
            return login_response(user)

        def delete(self):
            """ Log out by expiring the token cookie """
            return set_token_cookie(jsonify({"message": "Logged out"}), '', 0)

    class _Survey(Resource):  # First-login survey (questions are the "survey" site setting)
        @token_required()
        def get(self):
            return jsonify({"survey": g.current_user.survey, "needs_survey": g.current_user.survey is None})

        @token_required()
        def put(self):
            """ Save the current user's answers: {answers: {question_id: option_id | [option_id, ...]}} """
            body = request.get_json(silent=True) or {}
            answers = body.get('answers')
            if not isinstance(answers, dict):
                return {"message": "Send your answers as {answers: {question: choice}}"}, 400
            error = validate_survey(site_settings().get('survey', {}), answers)
            if error:
                return {"message": error}, 400
            return jsonify(g.current_user.save_survey(answers).read())

    api.add_resource(_ID, '/id')
    api.add_resource(_Survey, '/user/survey')
    api.add_resource(_CRUD, '/user')
    api.add_resource(_Security, '/authenticate')
