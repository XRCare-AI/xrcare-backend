""" Site content API: everything the frontend shows (model/site.py)

GET  /api/site                                  {settings, nav}: what every page needs
GET  /api/pages                                 every page {slug, title, url}
GET  /api/pages/<slug>                          one page with its sections, in order
PUT  /api/pages/<slug>                          Admin only: change {title}
PUT  /api/pages/<slug>/sections/<section>       Admin only: change {name, position, theme, background, content}
PUT  /api/site/settings                         Admin only: add or change settings {key: value, ...}
"""
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource

from api.jwt_authorize import token_required
from model.site import Page, Section, site, get_page, set_site_settings


site_api = Blueprint('site_api', __name__, url_prefix='/api')
api = Api(site_api)


class SiteAPI:
    class _Site(Resource):
        def get(self):
            return jsonify(site())

    class _Settings(Resource):
        @token_required("Admin")
        def put(self):
            body = request.get_json(silent=True)
            if not isinstance(body, dict) or not body:
                return {"message": "Send the settings to change as {key: value}"}, 400
            return jsonify(set_site_settings(body))

    class _Pages(Resource):
        def get(self):
            return jsonify([page.read(with_sections=False) for page in Page.query.order_by(Page.id).all()])

    class _Page(Resource):
        def get(self, slug):
            page = get_page(slug)
            if page is None:
                return {"message": "Page not found"}, 404
            return jsonify(page.read())

        @token_required("Admin")
        def put(self, slug):
            page = get_page(slug)
            if page is None:
                return {"message": "Page not found"}, 404
            return jsonify(page.update(request.get_json(silent=True) or {}).read())

    class _Section(Resource):
        @token_required("Admin")
        def put(self, slug, section):
            page = get_page(slug)
            target = page and Section.query.filter_by(_page_id=page.id, _slug=section).first()
            if not target:
                return {"message": "Section not found"}, 404
            try:
                return jsonify(target.update(request.get_json(silent=True) or {}).read())
            except (TypeError, ValueError):
                return {"message": "position must be a number"}, 400

    api.add_resource(_Site, '/site')
    api.add_resource(_Settings, '/site/settings')
    api.add_resource(_Pages, '/pages')
    api.add_resource(_Page, '/pages/<string:slug>')
    api.add_resource(_Section, '/pages/<string:slug>/sections/<string:section>')
