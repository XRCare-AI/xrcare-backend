# XRCare AI API

Flask backend for the [XRCare AI site](https://github.com/XRCare-AI/xrcare-frontend). It uses the same split as the Open Coding Society [pages](https://github.com/Open-Coding-Society/pages) (frontend) and [flask](https://github.com/Open-Coding-Society/flask) (backend) repos.

The backend holds all of the site's data: every heading, paragraph, menu link, image path, article, contact detail and contact form field. The frontend only lays out what the API returns.

## Run locally
```bash
make            # creates .venv, installs requirements, starts the API on http://localhost:8620
make stop       # stops it
```
Then run `make` in the xrcare-frontend repo and visit `http://localhost:4100`.

To run it by hand:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py      # creates instance/volumes/user_management.db and starts the API
```

## Accounts
`initUsers()` creates these accounts when the API starts. Admins are listed in `ADMINS` and users in `USERS` in `__init__.py`. Each starting password comes from `<UID>_PASSWORD` in `.env`:

| Name | Username | Role | Password in `.env` |
| --- | --- | --- | --- |
| Toby | `toby` | Admin | `TOBY_PASSWORD` |
| Adya Shipekar | `adyashipekar` | Admin | `ADYASHIPEKAR_PASSWORD` |
| Rohan Chandra | `rohanchandra` | User | `ROHANCHANDRA_PASSWORD` |

To add someone, add `('Name', 'username')` to `ADMINS` or `USERS` and a `USERNAME_PASSWORD=...` line to `.env`, then restart. Existing accounts keep their password; only their role is updated to match the list they are in.

- **Admins** can edit pages, sections, settings and articles through the API, and use the backend's own admin pages.
- **Users** can log in on the site (`/login/` on the frontend).

## Structure
- `main.py`: entry point. Registers the APIs, creates the database, accounts, site content and articles, and runs the server.
- `__init__.py`: Flask `app`, CORS (allowed frontend origins), accounts, settings, and `db`.
- `model/user.py`, `api/user.py`: `User` model, `initUsers()`, and the REST API for sign up, log in/out, profile and the first-login survey. `GET /api/id` includes `survey` and `needs_survey`; columns added since a database was made are added on start.
- `model/site_content.py`: `CONTENT_VERSION` with `RESEED` (pages), `RESEED_SETTINGS` (settings) and `RESEED_NAV` (menu) replace redesigned content in existing databases on start. Version 4: new home, About and Contact; Explore replaced For Clinical Teams and For Care Team Training; menu is Home / About Us / Explore / Contact; `account` and `survey` settings updated; `hub` setting added for My Hub.
- `api/jwt_authorize.py`: `@token_required` JWT cookie guard.
- `model/site.py`, `api/site.py`: site content. `SiteSetting` (logo, phone, footer text, labels...), `NavLink` (menu), `Page` and `Section` (each page's sections).
- `model/site_content.py`: the seed content for every page, copied word for word from xrcare.ai. Every section layout is listed at the top of this file.
- `model/article.py`, `api/article.py`: articles (blog posts) with categories, archives, search and popular posts.
- `model/contact.py`, `api/contact.py`: the "Ready to Transform Your Care Team?" form. `FIELDS` defines the form; messages are stored in `contact_messages`.
- `api/admin.py`, `templates/`: admin pages served by the backend (same home and login pages as OCS flask): users, page sections, site settings, articles, contact messages.
- `.env`: secret key and account passwords (not committed).
- `instance/volumes/user_management.db`: SQLite database (created on first run, not committed).
- `Dockerfile`, `docker-compose.yml`: production server (gunicorn on port 8620).

Images are files in the frontend repo (`images/`); the content stores their paths (`/images/hero.jpg`).

### Site content
On start, `initSite()` adds anything missing from `model/site_content.py`: settings, the menu (when empty) and pages that don't exist yet. Pages already in the database are left alone, so edits made through the API are kept. To reload the original content, delete `instance/volumes/user_management.db` and restart.

| Page | Frontend address | Sections (`layout`) |
| --- | --- | --- |
| `home` | `/` | `hero`, `hotspots`, `features`, `cards` |
| `about-us` | `/about-us/` | `about`, `team` |
| `for-clinicalteams` | `/for-clinicalteams/` | `intro` |
| `care-team-training` | `/care-team-training/` | `intro` |
| `contact` | `/contact/` | `banner` (then the contact form) |

The Articles pages, Log in and 404 take their wording from the `blog`, `login` and `not_found` settings.

## API
| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/api/site` | Settings and menu for every page: `{settings, nav}` |
| PUT | `/api/site/settings` | Admin only: add or change settings `{key: value, ...}` |
| GET | `/api/pages` | Every page `[{slug, title, url}]` |
| GET | `/api/pages/<slug>` | One page with its sections, in order |
| PUT | `/api/pages/<slug>` | Admin only: change `{title}` |
| PUT | `/api/pages/<slug>/sections/<section>` | Admin only: change `{name, position, theme, background, content}` |
| GET | `/api/articles` | Articles, newest first. Filter with `?category=<slug>`, `?author=<slug>`, `?month=YYYY-MM` or `?s=<words>` |
| GET | `/api/articles/sidebar` | `{recent, archives, categories, popular}` |
| GET | `/api/articles/<slug>` | One article with its `body`, plus the `newer` and `older` articles (counts a view) |
| POST | `/api/articles` | Admin only: add `{slug, title, author, body, excerpt, categories, tags, image, thumbnail, published}` |
| PUT | `/api/articles/<slug>` | Admin only: change any of those fields |
| DELETE | `/api/articles/<slug>` | Admin only: delete it |
| GET | `/api/contact/form` | The contact form's fields |
| POST | `/api/contact` | Send the contact form `{first_name, last_name, email, phone?, organization?, comment?}` (anyone) |
| GET | `/api/contact` | Admin only: every message, newest first |
| PUT | `/api/contact` | Admin only: mark a message handled `{id, handled}` |
| POST | `/api/authenticate` | Log in `{uid, password}` (uid can be the username or email); sets an httpOnly JWT cookie |
| DELETE | `/api/authenticate` | Log out |
| GET | `/api/id` | Current user's profile |
| POST | `/api/user` | Sign up `{name, uid, email?, phone?, password}` and log in |
| PUT | `/api/user` | Update `{name, uid, email, phone}` and/or `{current_password, new_password}` (accounts in ADMINS/USERS keep their username) |
| GET | `/api/user/survey` | Current user's first-login survey answers, and `needs_survey` |
| PUT | `/api/user/survey` | Save `{answers: {question_id: option_id or [option_ids]}}`; checked against the `survey` setting |
| GET | `/api/user` | Admin only: list every user |
| DELETE | `/api/user` | Admin only: delete a user `{uid}` |

### Admin pages
Log in at `http://localhost:8620/login` with an Admin account, then use the **Data** menu:
`/users/table2` (users), `/sections/` (page sections), `/settings/` (site settings and menu), `/articles/` (articles), `/contacts/` (contact messages).
