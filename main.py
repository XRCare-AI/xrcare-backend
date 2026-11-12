"""
XRCare AI API - entry point (same role as Open Coding Society flask main.py)

Run it with:
    python main.py

On start it creates the database (instance/volumes/user_management.db), adds the default users,
fills in the site content and articles, and serves the API on http://localhost:8620
"""
from flask import render_template

from __init__ import app
from api.admin import admin
from api.article import article_api
from api.contact import contact_api
from api.site import site_api
from api.user import user_api
from model.article import initArticles
from model.contact import initContacts
from model.site import initSite
from model.user import initUsers


# Register URIs for API endpoints
app.register_blueprint(admin)
app.register_blueprint(user_api)
app.register_blueprint(site_api)
app.register_blueprint(contact_api)
app.register_blueprint(article_api)


@app.route('/')
def index():
    # Same home page as Open Coding Society flask, with Login in the navbar for admin access
    return render_template('index.html')


# Create the database, default users, site content and articles whenever the app starts (python main.py or gunicorn)
initUsers()
initSite()
initContacts()
initArticles()

if __name__ == "__main__":
    print(f"Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"Server running: http://localhost:{app.config['FLASK_PORT']}")
    app.run(debug=True, host="0.0.0.0", port=app.config['FLASK_PORT'], use_reloader=False)
