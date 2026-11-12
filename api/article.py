""" Articles API: the Articles page, each article's page and its sidebar (model/article.py)

GET    /api/articles                  newest first; filter with ?category=<slug> ?author=<slug> ?month=YYYY-MM ?s=<words>
GET    /api/articles/sidebar          {recent, archives, categories, popular}
GET    /api/articles/<slug>           one article with its body and the {newer, older} articles (counts a view)
POST   /api/articles                  Admin only: add {slug, title, author, body, excerpt, categories, tags, image, thumbnail, published}
PUT    /api/articles/<slug>           Admin only: change any of those fields
DELETE /api/articles/<slug>           Admin only: delete it
"""
from datetime import date

from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource

from api.jwt_authorize import token_required
from model.article import Article, slugify


article_api = Blueprint('article_api', __name__, url_prefix='/api')
api = Api(article_api)


def newest_first():
    return Article.query.order_by(Article._published.desc(), Article.id.desc()).all()


def month_label(month):
    return date(int(month[:4]), int(month[5:7]), 1).strftime('%B %Y')


class ArticleAPI:
    class _List(Resource):
        def get(self):
            articles = newest_first()
            category, author = request.args.get('category'), request.args.get('author')
            month, words = request.args.get('month'), (request.args.get('s') or '').strip()
            heading = None
            if category:
                articles = [a for a in articles if category in (c['slug'] for c in a.read()['categories'])]
                name = next((c['name'] for a in articles for c in a.read()['categories'] if c['slug'] == category), category)
                heading = {"type": "category", "label": name}
            if author:
                articles = [a for a in articles if slugify(a._author) == author]
                heading = {"type": "author", "label": articles[0]._author if articles else author}
            if month:
                articles = [a for a in articles if a.published.isoformat()[:7] == month]
                try:
                    heading = {"type": "archive", "label": month_label(month)}
                except ValueError:
                    return {"message": "month must be YYYY-MM"}, 400
            if words:
                needle = words.lower()
                articles = [a for a in articles if needle in (a._title + ' ' + a._excerpt + ' ' + a._body).lower()]
                heading = {"type": "search", "label": words}
            return jsonify({"articles": [a.read() for a in articles], "heading": heading})

        @token_required("Admin")
        def post(self):
            body = request.get_json(silent=True) or {}
            error = Article.validate(body, creating=True)
            if error:
                return {"message": error}, 400
            fields = {k: body[k] for k in Article.FIELDS if k in body and k != 'views'}
            if 'published' in fields:
                fields['published'] = date.fromisoformat(str(fields['published']))
            article = Article(**fields).create()
            if article is None:
                return {"message": "An article with that slug already exists"}, 409
            return article.read(with_body=True), 201

    class _Sidebar(Resource):
        def get(self):
            articles = newest_first()
            months = sorted({a.published.isoformat()[:7] for a in articles}, reverse=True)
            categories = {}
            for a in articles:
                for c in a.read()['categories']:
                    categories[c['slug']] = c
            popular = sorted(articles, key=lambda a: a._views, reverse=True)
            return jsonify({
                "recent": [{"slug": a.slug, "title": a._title} for a in articles[:5]],
                "archives": [{"month": m, "label": month_label(m)} for m in months],
                "categories": sorted(categories.values(), key=lambda c: c['name']),
                "popular": [{"slug": a.slug, "title": a._title, "thumbnail": a.read()['thumbnail'],
                             "published": a.published.isoformat()} for a in popular[:5]],
            })

    class _One(Resource):
        def get(self, slug):
            article = Article.query.filter_by(_slug=slug).first()
            if article is None:
                return {"message": "Article not found"}, 404
            article.add_view()
            articles = newest_first()
            i = articles.index(article)
            short = lambda a: {"slug": a.slug, "title": a._title, "image": a.read()['image']} if a else None
            data = article.read(with_body=True)
            data["newer"] = short(articles[i - 1] if i > 0 else None)
            data["older"] = short(articles[i + 1] if i + 1 < len(articles) else None)
            return jsonify(data)

        @token_required("Admin")
        def put(self, slug):
            article = Article.query.filter_by(_slug=slug).first()
            if article is None:
                return {"message": "Article not found"}, 404
            body = request.get_json(silent=True) or {}
            error = Article.validate(body)
            if error:
                return {"message": error}, 400
            if article.update(body) is None:
                return {"message": "An article with that slug already exists"}, 409
            return jsonify(article.read(with_body=True))

        @token_required("Admin")
        def delete(self, slug):
            article = Article.query.filter_by(_slug=slug).first()
            if article is None:
                return {"message": "Article not found"}, 404
            article.delete()
            return {"message": f"Deleted article {slug}"}

    api.add_resource(_List, '/articles')
    api.add_resource(_Sidebar, '/articles/sidebar')
    api.add_resource(_One, '/articles/<string:slug>')
