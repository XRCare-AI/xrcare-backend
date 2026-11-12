""" Site content: every word, link and image path on the XRCare AI site (same pattern as model/user.py)

The frontend has no content of its own; it lays out what the API returns.

Tables:
  site_settings  key -> JSON value (logo, contact details, footer text, 404 page...)
  nav_links      the menu (slide-out menu and footer menu)
  pages          each page of the site (home, about-us, for-clinicalteams...) with its title
  sections       the full-screen sections of a page, in order. `content` holds the section's words
                 and images, shaped by its `layout` (see model/site_content.py for every layout)

Image paths ("/images/hero.jpg") are files in the frontend repo.
The seed content (model/site_content.py) is copied word for word from xrcare.ai. It is loaded on
first run only, so edits made through the API are kept.
"""
import json
from datetime import datetime, timezone

from __init__ import app, db
from model.site_content import SETTINGS, NAV, PAGES, CONTENT_VERSION, RESEED, RESEED_SETTINGS, RESEED_NAV


class SiteSetting(db.Model):
    """
    SiteSetting Model

    Attributes:
        id (Column): Primary key.
        _key (Column): Setting name, e.g. "phone".
        _value (Column): JSON-encoded value.
    """
    __tablename__ = 'site_settings'

    id = db.Column(db.Integer, primary_key=True)
    _key = db.Column(db.String(64), unique=True, nullable=False)
    _value = db.Column(db.Text, nullable=False)

    def __init__(self, key, value):
        self._key = key
        self._value = json.dumps(value)

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return json.loads(self._value)

    @value.setter
    def value(self, value):
        self._value = json.dumps(value)


class NavLink(db.Model):
    """
    NavLink Model

    Attributes:
        id (Column): Primary key.
        _label (Column): Text shown in the menu.
        _url (Column): Where it goes (site path such as "/about-us/", or a full URL).
        _position (Column): Order in the menu.
    """
    __tablename__ = 'nav_links'

    id = db.Column(db.Integer, primary_key=True)
    _label = db.Column(db.String(128), nullable=False)
    _url = db.Column(db.String(512), nullable=False)
    _position = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, label, url, position=0):
        self._label = label
        self._url = url
        self._position = position

    def read(self):
        return {"id": self.id, "label": self._label, "url": self._url, "position": self._position}


class Page(db.Model):
    """
    Page Model

    Attributes:
        id (Column): Primary key.
        _slug (Column): The page's address on the site ("home" is "/", "about-us" is "/about-us/").
        _title (Column): Browser tab title.
        sections (relationship): The page's sections, in order.
    """
    __tablename__ = 'pages'

    id = db.Column(db.Integer, primary_key=True)
    _slug = db.Column(db.String(64), unique=True, nullable=False)
    _title = db.Column(db.String(255), nullable=False)
    sections = db.relationship('Section', backref='page', cascade='all, delete-orphan',
                               order_by='Section._position')

    def __init__(self, slug, title):
        self._slug = slug
        self._title = title

    @property
    def slug(self):
        return self._slug

    def read(self, with_sections=True):
        data = {"id": self.id, "slug": self._slug, "title": self._title,
                "url": "/" if self._slug == "home" else f"/{self._slug}/"}
        if with_sections:
            data["sections"] = [section.read() for section in self.sections]
        return data

    def update(self, inputs):
        if 'title' in inputs:
            self._title = str(inputs['title']).strip()
        db.session.commit()
        return self


class Section(db.Model):
    """
    Section Model

    Attributes:
        id (Column): Primary key.
        _page_id (Column): The page it is on.
        _slug (Column): Anchor in the page URL (/#features), unique on its page.
        _name (Column): Name shown beside the section's dot in the side navigation.
        _position (Column): Order on the page.
        _layout (Column): How the frontend draws it (see model/site_content.py).
        _theme (Column): "light" (white text) or "dark" section.
        _background (Column): JSON {color, image, overlay_color, overlay_opacity}.
        _content (Column): JSON, shaped by layout.
        updated_at (Column): Last change.
    """
    __tablename__ = 'sections'
    __table_args__ = (db.UniqueConstraint('_page_id', '_slug'),)

    id = db.Column(db.Integer, primary_key=True)
    _page_id = db.Column(db.Integer, db.ForeignKey('pages.id', ondelete='CASCADE'), nullable=False)
    _slug = db.Column(db.String(64), nullable=False)
    _name = db.Column(db.String(128), nullable=False)
    _position = db.Column(db.Integer, nullable=False, default=0)
    _layout = db.Column(db.String(32), nullable=False)
    _theme = db.Column(db.String(16), nullable=False, default='light')
    _background = db.Column(db.Text, nullable=False, default='{}')
    _content = db.Column(db.Text, nullable=False, default='{}')
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    def __init__(self, page, slug, name, position, layout, theme='light', background=None, content=None):
        self.page = page
        self._slug = slug
        self._name = name
        self._position = position
        self._layout = layout
        self._theme = theme
        self._background = json.dumps(background or {})
        self._content = json.dumps(content or {})

    @property
    def slug(self):
        return self._slug

    def read(self):
        return {
            "id": self.id,
            "page": self.page.slug,
            "slug": self._slug,
            "name": self._name,
            "position": self._position,
            "layout": self._layout,
            "theme": self._theme,
            "background": json.loads(self._background),
            "content": json.loads(self._content),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def update(self, inputs):
        """ Update name, position, theme, background and/or content from a dict """
        if 'name' in inputs:
            self._name = str(inputs['name']).strip()
        if 'position' in inputs:
            self._position = int(inputs['position'])
        if 'theme' in inputs and inputs['theme'] in ('light', 'dark'):
            self._theme = inputs['theme']
        if 'background' in inputs and isinstance(inputs['background'], dict):
            self._background = json.dumps(inputs['background'])
        if 'content' in inputs and isinstance(inputs['content'], dict):
            self._content = json.dumps(inputs['content'])
        db.session.commit()
        return self


def site_settings():
    return {s.key: s.value for s in SiteSetting.query.order_by(SiteSetting.id).all()}


def set_site_settings(values):
    """ Add or replace settings from a dict """
    for key, value in values.items():
        setting = SiteSetting.query.filter_by(_key=key).first()
        if setting is None:
            db.session.add(SiteSetting(key, value))
        else:
            setting.value = value
    db.session.commit()
    return site_settings()


def nav_links():
    return [link.read() for link in NavLink.query.order_by(NavLink._position, NavLink.id).all()]


def site():
    """ What every page needs: settings and menu """
    return {"settings": site_settings(), "nav": nav_links()}


def get_page(slug):
    return Page.query.filter_by(_slug=slug).first()


def initSite():
    """ Create the content tables and add any missing settings, menu and pages from model/site_content.py """
    with app.app_context():
        db.create_all()
        existing = {s.key for s in SiteSetting.query.all()}
        for key, value in SETTINGS.items():
            if key not in existing:
                db.session.add(SiteSetting(key, value))
        # Pages redesigned since this database was filled are replaced with the new seed
        version_setting = SiteSetting.query.filter_by(_key='content_version').first()
        version = version_setting.value if version_setting else 1
        for v in range(version + 1, CONTENT_VERSION + 1):
            for slug in RESEED.get(v, []):
                old = get_page(slug)
                if old is not None:
                    db.session.delete(old)
            for key in RESEED_SETTINGS.get(v, []):
                if key in SETTINGS:
                    set_site_settings({key: SETTINGS[key]})
            if v in RESEED_NAV:
                NavLink.query.delete()
        db.session.flush()
        if version_setting is None:
            db.session.add(SiteSetting('content_version', CONTENT_VERSION))
        else:
            version_setting.value = CONTENT_VERSION
        if NavLink.query.first() is None:
            for position, (label, url) in enumerate(NAV):
                db.session.add(NavLink(label, url, position))
        for seed in PAGES:
            if get_page(seed['slug']) is not None:
                continue
            page = Page(seed['slug'], seed['title'])
            db.session.add(page)
            for position, s in enumerate(seed['sections']):
                db.session.add(Section(page, s['slug'], s['name'], position, s['layout'], s.get('theme', 'light'),
                                       s.get('background'), s.get('content')))
        db.session.commit()
