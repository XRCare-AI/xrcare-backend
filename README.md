# XRCare AI API

Flask backend for the [XRCare AI site](https://github.com/XRCare-AI/xrcare-frontend). It uses the same split as the Open Coding Society [pages](https://github.com/Open-Coding-Society/pages) (frontend) and [flask](https://github.com/Open-Coding-Society/flask) (backend) repos.

The backend holds the site's **data**: user accounts, first-login survey answers, articles and contact messages. The site's own content (pages, wording, menu, images) lives in the frontend (`_data/`), so the frontend works on its own; only log in / sign up, the survey, My Hub, articles and the contact form need this API.

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

- **Admins** can manage articles and contact messages through the API, and use the backend's own admin pages.
- **Users** can log in on the site (`/login/` on the frontend).

## Structure
- `main.py`: entry point. Registers the APIs, creates the database, accounts and articles, and runs the server.
- `__init__.py`: Flask `app`, CORS (allowed frontend origins), accounts, settings, and `db`.
- `model/user.py`, `api/user.py`: `User` model, `initUsers()`, and the REST API for sign up, log in/out, profile and the first-login survey. `GET /api/id` includes `survey` and `needs_survey`; columns added since a database was made are added on start.
- `model/survey.py`: the first-login survey's questions (`QUESTIONS`, served at `GET /api/survey`) and `validate_survey()` for a user's answers.
- `api/jwt_authorize.py`: `@token_required` JWT cookie guard.
- `model/article.py`, `api/article.py`: articles (blog posts) with categories, archives, search and popular posts.
- `model/contact.py`, `api/contact.py`: the "Ready to Transform Your Care Team?" form. `FIELDS` defines the form; messages are stored in `contact_messages`.
- `api/admin.py`, `templates/`: admin pages served by the backend (same home and login pages as OCS flask): users, articles, contact messages.
- `.env`: secret key and account passwords (not committed).
- `instance/volumes/user_management.db`: SQLite database (created on first run, not committed).
- `Dockerfile`, `docker-compose.yml`: production server (gunicorn on port 8620).

Images are files in the frontend repo (`images/`); articles store their paths (`/images/articles/...`).

Databases made before the site content moved to the frontend still have `site_settings`, `nav_links`, `pages` and `sections` tables. Nothing uses them any more; they can be dropped or left alone.

## API
| Method | Endpoint | Purpose |
| --- | --- | --- |
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
| GET | `/api/survey` | The first-login survey's questions (anyone) |
| GET | `/api/user/survey` | Current user's first-login survey answers, and `needs_survey` |
| PUT | `/api/user/survey` | Save `{answers: {question_id: option_id or [option_ids]}}`; checked against `model/survey.py` |
| GET | `/api/user` | Admin only: list every user |
| DELETE | `/api/user` | Admin only: delete a user `{uid}` |

### Admin pages
Log in at `http://localhost:8620/login` with an Admin account, then use the **Data** menu:
`/users/table2` (users), `/articles/` (articles), `/contacts/` (contact messages).
