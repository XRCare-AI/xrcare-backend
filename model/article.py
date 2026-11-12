""" Articles (blog posts) model (same pattern as model/user.py)

The Articles page lists them; each one has its own page. Seeded on first run with the two posts on
xrcare.ai, copied word for word. `body` is HTML limited to <p> <h2> <h3> <ul> <ol> <li> <b> <strong>
<i> <em> <br> <a>; the frontend removes anything else.
"""
import json
import re
from datetime import date, datetime, timezone

from sqlalchemy.exc import IntegrityError

from __init__ import app, db


SLUG_PATTERN = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')


def slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', str(text).lower()).strip('-')


class Article(db.Model):
    """
    Article Model

    Attributes:
        id (Column): Primary key.
        _slug (Column): Address of the article (/articles/post/?slug=xrcare-ai).
        _title (Column): Headline.
        _author (Column): Byline.
        _categories (Column): JSON list of category names.
        _tags (Column): JSON list of tags.
        _image (Column): Featured image path (frontend repo).
        _thumbnail (Column): Smaller image for the Popular Posts list (optional).
        _excerpt (Column): Summary on the Articles page.
        _body (Column): The article (HTML).
        _published (Column): Date published.
        _views (Column): How many times it has been opened (orders Popular Posts).
        updated_at (Column): Last change.
    """
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    _slug = db.Column(db.String(128), unique=True, nullable=False)
    _title = db.Column(db.String(255), nullable=False)
    _author = db.Column(db.String(128), nullable=False)
    _categories = db.Column(db.Text, nullable=False, default='[]')
    _tags = db.Column(db.Text, nullable=False, default='[]')
    _image = db.Column(db.String(512), nullable=True)
    _thumbnail = db.Column(db.String(512), nullable=True)
    _excerpt = db.Column(db.Text, nullable=False, default='')
    _body = db.Column(db.Text, nullable=False, default='')
    _published = db.Column(db.Date, nullable=False, default=date.today)
    _views = db.Column(db.Integer, nullable=False, default=0)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    FIELDS = ('slug', 'title', 'author', 'categories', 'tags', 'image', 'thumbnail', 'excerpt', 'body', 'published', 'views')

    def __init__(self, slug, title, author, body='', excerpt='', categories=None, tags=None,
                 image=None, thumbnail=None, published=None, views=0):
        self._slug = slug
        self._title = title
        self._author = author
        self._body = body
        self._excerpt = excerpt
        self._categories = json.dumps(categories or [])
        self._tags = json.dumps(tags or [])
        self._image = image
        self._thumbnail = thumbnail
        self._published = published or date.today()
        self._views = views

    @property
    def slug(self):
        return self._slug

    @property
    def categories(self):
        return json.loads(self._categories)

    @property
    def published(self):
        return self._published

    @staticmethod
    def validate(inputs, creating=False):
        """ Returns an error message for the first invalid field supplied, or None """
        if creating:
            for field in ('slug', 'title', 'author'):
                if not str(inputs.get(field) or '').strip():
                    return f'{field} is required'
        if 'slug' in inputs and (not SLUG_PATTERN.match(str(inputs['slug'])) or inputs['slug'] == 'sidebar'):
            return 'slug must be lowercase letters, numbers and dashes'
        for field in ('categories', 'tags'):
            if field in inputs and not (isinstance(inputs[field], list) and all(isinstance(v, str) for v in inputs[field])):
                return f'{field} must be a list of names'
        if 'published' in inputs:
            try:
                date.fromisoformat(str(inputs['published']))
            except ValueError:
                return 'published must be a date (YYYY-MM-DD)'
        return None

    def create(self):
        """ Add the article; returns None if the slug is taken """
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.rollback()
            return None

    def update(self, inputs):
        """ Update any of FIELDS from a dict (validate first); returns None if the new slug is taken """
        for field in ('slug', 'title', 'author', 'image', 'thumbnail', 'excerpt', 'body'):
            if field in inputs:
                setattr(self, '_' + field, str(inputs[field]).strip() if inputs[field] is not None else None)
        for field in ('categories', 'tags'):
            if field in inputs:
                setattr(self, '_' + field, json.dumps(inputs[field]))
        if 'published' in inputs:
            self._published = date.fromisoformat(str(inputs['published']))
        try:
            db.session.commit()
            return self
        except IntegrityError:
            db.session.rollback()
            return None

    def add_view(self):
        self._views = (self._views or 0) + 1
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def read(self, with_body=False):
        data = {
            "id": self.id,
            "slug": self._slug,
            "title": self._title,
            "author": self._author,
            "author_slug": slugify(self._author),
            "categories": [{"name": c, "slug": slugify(c)} for c in self.categories],
            "tags": json.loads(self._tags),
            "image": self._image or "",
            "thumbnail": self._thumbnail or self._image or "",
            "excerpt": self._excerpt,
            "published": self._published.isoformat(),
            "views": self._views,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        if with_body:
            data["body"] = self._body
        return data


ARTICLES = [
    {
        'slug': 'xrcare-ai',
        'title': 'XRCare AI: How Technology is Transforming Healthcare Through Intelligent XR',
        'author': 'Amin Barhoush',
        'published': date(2025, 8, 8),
        'views': 108,
        'categories': ['Healthcare Technology', 'Medical Education'],
        'tags': ['AI in Healthcare', 'Care Team Collaboration', 'Immersive Simulations', 'Nursing Education',
                 'Patient Safety', 'Pharmacy Training', 'XR in Medical Training'],
        'image': '/images/articles/xrcare-ai.png',
        'excerpt': 'XRCare AI combines artificial intelligence and immersive XR technology to transform healthcare '
                   'training, improve patient safety, and enhance team collaboration.',
        'body': """<p>Healthcare is entering a new era where immersive technology and intelligent systems work hand in hand. <a href="http://xrcare.ai"><b>XRCare.ai</b></a>  integrates the power of artificial intelligence with extended reality (XR) to improve accuracy, efficiency and collaboration across the healthcare industry. From pharmacy operations to nursing practice to care team training, XRCare AI provides tailored, adaptive, and measurable solutions that enhance both safety and patient outcomes.</p>
<h2><b>USE CASE 1: Pharmacy – Precision and Safety at Scale</b></h2>
<p>Pharmacists play a critical role in patient safety, yet medication errors remain one of healthcare’s most persistent challenges. XRCare AI brings intelligence and immersion together to minimize risk.</p>
<ul>
<li><b>AI-Powered Safety Checks:</b> Real-time verification of medication selection and dosage during XR training scenarios.</li>
<li><b>Immersive Workflows:</b> Pharmacists practice in simulated environments where errors trigger adaptive AI prompts, teaching corrective actions before they happen in real life.</li>
<li><b>Patient Interaction Training:</b> XR simulations prepare pharmacists to counsel patients with diverse needs, while AI tracks tone, clarity, and compliance messaging.</li>
</ul>
<p><b>Impact:</b> Reduced dispensing errors, standardized training across pharmacy teams, and stronger pharmacist–patient communication.</p>
<h2><b>USE CASE 2: Nursing – Adaptive Learning for a Dynamic Role</b></h2>
<p>Nurses must respond quickly to unpredictable situations, and traditional training doesn’t always capture the complexity of real care environments. XRCare AI creates realistic, data-driven practice opportunities that improve clinical judgment.</p>
<ul>
<li><b>Scenario Adaptation:</b> AI adjusts XR patient vitals and conditions in real-time based on nursing interventions, creating dynamic, lifelike simulations.</li>
<li><b>Skill Reinforcement:</b> From IV insertion to wound care, immersive practice sessions are supported by AI feedback to correct techniques instantly.</li>
<li><b>Emotional Intelligence Training:</b> Nurses encounter challenging patient or family interactions in XR, while AI evaluates communication strategies and suggests improvements.</li>
</ul>
<p><b>Impact:</b> Higher confidence, improved decision-making under stress and stronger bedside communication.</p>
<h2><b>USE CASE 3: Care Team Training – Building Collaboration and Reducing Errors</b></h2>
<p>Healthcare is team-based, but miscommunication in handoffs and multidisciplinary care remains a top cause of medical errors. XRCare AI strengthens collaboration by simulating real-world team dynamics.</p>
<ul>
<li><b>Collaborative XR Scenarios:</b> Doctors, nurses, and allied professionals train together in immersive environments.</li>
<li><b>AI-Coached Handoffs:</b> AI analyzes communication during patient transfers, highlighting missed details and reinforcing best practices.</li>
<li><b>Performance Analytics:</b> Teams receive objective, data-backed insights into coordination, role clarity, and responsiveness.</li>
</ul>
<p><b>Impact:</b> Fewer handoff-related errors, stronger collaboration across disciplines, and measurable improvements in patient safety.</p>
<h2><b>Why XRCare AI Matters</b></h2>
<p>By merging <b>AI’s intelligence</b> with <b>XR’s immersive power</b>, XRCare AI ensures that healthcare professionals aren’t just learning — they’re practicing, adapting and improving in ways that can directly translate to safer, more effective patient care.</p>""",
    },
    {
        'slug': 'extended-intelligence',
        'title': 'The CEO’s Perspective: Extended Intelligence and the Future of Healthcare Training',
        'author': 'Amin Barhoush',
        'published': date(2025, 9, 28),
        'views': 121,
        'categories': ['Healthcare Technology', 'Medical Education'],
        'tags': ['AI in Healthcare Training', 'Extended Intelligence (XI)', 'Nursing Education', 'Pharmacy Training',
                 'Virtual Simulations', 'XR in Medical Education'],
        'image': '/images/articles/extended-intelligence.jpg',
        'thumbnail': '/images/articles/extended-intelligence-thumb.jpg',
        'excerpt': 'Discover how Extended Intelligence (XI)—the fusion of AI and XR—is transforming healthcare '
                   'training by enhancing pharmacy and nursing education, building empathy through virtual '
                   'simulations, and preparing care teams with human-centered…',
        'body': """<h3><b>The CEO’s Perspective: Extended Intelligence and the Future of Healthcare Training</b></h3>
<p>At XRCare, our mission has always been simple but powerful: to put people at the center of technology. Every innovation we pursue and every partnership we develop is designed with one goal in mind—helping healthcare professionals feel more confident, connected and capable in delivering care. We are aiming to empower individuals to improve their efficiency across healthcare verticals. </p>
<p>In recent years, we’ve seen the rapid convergence of artificial intelligence (AI) and extended reality (XR) into something far more powerful: what experts are now calling <b>Extended Intelligence (XI)</b>. This isn’t just a buzzword—it’s a meaningful shift in how we prepare the next generation of pharmacists, nurses and care training teams to meet the challenges of modern healthcare.</p>
<p>Research confirms what we are already witnessing in practice. As Dr. Baichuan Zeng observed in a 2025 analysis on arXiv, XI represents a new landscape where AI-driven insights and spatially intelligent XR environments come together to create richer, more effective learning experiences [1]. At XRCare, we are witnessing firsthand how this shift translates into <b>safer training, stronger collaboration, and more confident care delivery</b>.</p>
<p>Take pharmacy training, for example. Traditional classroom and clinical education often leave gaps between theory and practice. With XI, students can step into virtual simulations where they safely navigate complex patient histories, medication interactions and even teamwork scenarios. They’re not just memorizing protocols—they’re <b>living the experience</b> of making real-time decisions, without the risk of patient harm. This builds both competence and confidence.</p>
<p>Nursing education benefits in equally profound ways. Using XR-powered patient simulations, nurses can practice everything from assessments to communication skills in lifelike environments. One of the most striking outcomes we’ve seen is how these simulations foster <b>empathy</b>. Role-playing as a patient, for example, allows nursing students to truly feel what it’s like to be on the other side of care. That shift in perspective can’t be taught in a textbook—it can only be experienced.</p>
<p>And for care training teams, XI is transforming onboarding and readiness. Instead of reading manuals or shadowing under pressure, new staff can walk through hospital layouts virtually, practice emergency protocols, and rehearse teamwork drills before ever stepping onto the floor. This doesn’t just prepare them faster—it makes them <b>feel like part of the team from day one</b>.</p>
<p>As Siddiqui and Jabeen note in their 2025 study, the integration of AI and XR in healthcare education is about more than just technical skills; it’s about cultivating the <b>human skills—empathy, communication, adaptability—that define great caregivers</b> [2]. This philosophy is what excites me most. XI isn’t replacing the human touch; it’s reinforcing it.</p>
<p>At XRCare, we believe technology should never stand between a caregiver and a patient. Instead, it should empower caregivers to bring their best selves to every interaction. The promise of Extended Intelligence is that it makes training <b>consistent, personalized, and deeply human</b>—so when the moment comes to deliver care, professionals are ready not just with skills, but with heart.</p>
<p>The future of healthcare is being written right now, and XI is playing a central role. For us at XRCare, it’s not just about the technology. It’s about the people—the pharmacist double-checking a prescription, the nurse listening to a patient’s fears, the care team responding to a crisis with calm precision. By bringing AI and XR together, we’re helping those professionals learn, grow, and, ultimately, care better. And that’s a mission worth leading.</p>
<p><b>Citations</b><b><br>
</b> [1] Zeng, Baichuan. <i>Recent Advances and Future Directions in Extended Reality (XR): Exploring AI-Powered Spatial Intelligence.</i> (2025).<br>
 [2] Faizan Siddiqui, Mohd, et al. <i>Integration of Augmented Reality, Virtual Reality, and Extended Reality in Healthcare and Medical Education: A Glimpse into the Emerging Horizon in LMICs—A Systematic Review.</i> Journal of Medical Education and Curricular Development 12 (2025)</p>""",
    },
]


def initArticles():
    """ Create the articles table and add the xrcare.ai posts when it is empty """
    with app.app_context():
        db.create_all()
        if Article.query.first() is None:
            for seed in ARTICLES:
                Article(**seed).create()
