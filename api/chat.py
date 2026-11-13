""" Chat API: the site's chat bubble (same pattern as api/contact.py). Routes only; the work is in model/.

GET  /api/chat   the bubble's wording, and whether the assistant can answer (any API key set)
POST /api/chat   send {messages: [{role: "user"|"assistant", content}]}, get {reply, provider}
                 Public (no login), limited to model/rate_limit.py's LIMIT messages per minute per visitor.
"""
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource

from model.chat import WIDGET, ChatError, get_reply, is_available
from model.rate_limit import seconds_until_allowed


chat_api = Blueprint('chat_api', __name__, url_prefix='/api')
api = Api(chat_api)


class ChatAPI:
    class _Chat(Resource):
        def get(self):
            return jsonify({**WIDGET, 'available': is_available()})

        def post(self):
            """ Anyone can chat, logged in or not, like the contact form """
            # The visitor's IP address. Once the backend is deployed behind a proxy (e.g. nginx), every request
            # would come from the proxy's IP, so the proxy must be trusted with Werkzeug's ProxyFix first.
            wait = seconds_until_allowed(request.remote_addr or 'unknown')
            if wait:
                # Same reply as OCS's throttled(): 429 Too Many Requests, plus how long to wait
                return {"message": f"Too many messages. Please wait {wait} seconds and try again."}, 429, \
                    {'Retry-After': str(wait)}

            body = request.get_json(silent=True) or {}
            try:
                return jsonify(get_reply(body.get('messages')))
            except ChatError as error:
                return {"message": str(error)}, error.status

    api.add_resource(_Chat, '/chat')
