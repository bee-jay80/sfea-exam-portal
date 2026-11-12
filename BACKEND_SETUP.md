# SFEA Exam Portal Backend Setup

This document explains how to install and configure the Django backend for the SFEA examination portal.

## 1. Prerequisites

Before you start, make sure the following are installed:

- Python 3.12+
- Git
- PostgreSQL (for production and later staging)
- Redis (for Celery/async jobs)
- A mail provider or SMTP service for email delivery

## 2. Install backend dependencies

From the project root:

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# or
.venv\Scripts\activate       # Windows PowerShell

python -m pip install --upgrade pip
pip install -e .
```

If you prefer to install dependencies manually:

```bash
pip install django djangorestframework djangorestframework-simplejwt python-dotenv psycopg[binary] gunicorn celery redis
```

## 3. Environment variables

Create a `.env` file in the project root using `.env.example` as the template:

```bash
cp .env.example .env
```

Then fill in the values for your environment. The main keys are:

- `SECRET_KEY`: Django secret key
- `DEBUG`: `True` for local development, `False` for production
- `ALLOWED_HOSTS`: comma-separated hosts such as `localhost,127.0.0.1,your-domain.com`
- `DB_ENGINE`: usually `django.db.backends.postgresql`
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`: PostgreSQL credentials
- `JWT_SECRET_KEY`: separate secret for JWT signing
- `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`: SMTP credentials
- `REDIS_URL`, `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`: Redis settings
- `CODE_EXECUTION_URL`: isolated code execution service endpoint
- `CODE_EXECUTION_API_KEY`: service-to-service auth key

## 4. Database setup

For local development with SQLite, the project already defaults to a local `db.sqlite3` file.

For PostgreSQL, set the relevant database values in `.env` and run:

```bash
python manage.py migrate
```

If you are starting with a fresh database, create the database first in PostgreSQL and then run the migrate command.

## 5. Create a superuser

```bash
python manage.py createsuperuser
```

Use the admin email and password you want for the first administrative account.

## 6. Run the backend locally

```bash
python manage.py runserver
```

The API is exposed under:

- `http://127.0.0.1:8000/api/v1/auth/register/`
- `http://127.0.0.1:8000/api/v1/auth/login/`
- `http://127.0.0.1:8000/api/v1/auth/me/`
- `http://127.0.0.1:8000/admin/`

## 7. Email setup

The backend is configured to use Django email settings from the environment. You can switch between SMTP, console, or file-based backends depending on your environment.

For example:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.mailtrap.io
EMAIL_PORT=2525
EMAIL_HOST_USER=your-user
EMAIL_HOST_PASSWORD=your-password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=no-reply@example.com
```

When you have the real credentials, replace the placeholder values in `.env` and the system will send mail through your provider.

## 8. Celery and Redis setup

The backend is prepared to use Redis and Celery later. Add the credentials in `.env` and then configure the worker in your deployment environment.

Example keys:

```env
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

## 9. Production notes

- Turn `DEBUG=False` in production.
- Set `ALLOWED_HOSTS` to your domain names.
- Use a real Postgres database instead of SQLite.
- Store all secrets in a secure environment or secret manager.
- Use HTTPS in production.
- Keep the code execution service isolated from the main application server and database.

## 10. Common commands

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py test
python manage.py createsuperuser
python manage.py runserver
```
