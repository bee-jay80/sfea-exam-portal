import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv


# BASE CONFIGURATION

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


def env_bool(name: str, default: bool = False) -> bool:
    """Read a boolean environment variable."""
    return os.getenv(name, str(default)).strip().lower() in {
        "true",
    }


def env_list(name: str, default: str = "") -> list[str]:
    """Read a comma-separated environment variable."""
    return [
        value.strip()
        for value in os.getenv(name, default).split(",")
        if value.strip()
    ]


# SECURITY

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    if not env_bool("DEBUG", True):
        raise ValueError("SECRET_KEY must be configured in production.")

    SECRET_KEY = "django-insecure-local-development-key"

DEBUG = env_bool("DEBUG", True)

ALLOWED_HOSTS = env_list(
    "ALLOWED_HOSTS",
    "localhost,127.0.0.1,*,[::1]",
)

CSRF_TRUSTED_ORIGINS = env_list("CSRF_TRUSTED_ORIGINS")


# APPLICATIONS

INSTALLED_APPS = [
    # Django applications
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party applications
    "rest_framework",
    "rest_framework_simplejwt",

    # Local applications
    "apps.accounts",
    "apps.organizations",
]


# MIDDLEWARE

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# URLS AND APPLICATION ENTRY POINTS

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"

ASGI_APPLICATION = "config.asgi.application"


# TEMPLATES

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# DATABASE

DB_ENGINE = os.getenv(
    "DB_ENGINE",
    "django.db.backends.sqlite3",
)

DATABASES = {
    "default": {
        "ENGINE": DB_ENGINE,
        "NAME": os.getenv(
            "DB_NAME",
            str(BASE_DIR / "db.sqlite3"),
        ),
        "USER": os.getenv("DB_USER", ""),
        "PASSWORD": os.getenv("DB_PASSWORD", ""),
        "HOST": os.getenv("DB_HOST", ""),
        "PORT": os.getenv("DB_PORT", ""),
        "CONN_MAX_AGE": int(os.getenv("DB_CONN_MAX_AGE", "60")),
        "CONN_HEALTH_CHECKS": True,
    }
}

# Optional PostgreSQL SSL configuration.
DB_SSLMODE = os.getenv("DB_SSLMODE")

if DB_ENGINE == "django.db.backends.postgresql" and DB_SSLMODE:
    DATABASES["default"]["OPTIONS"] = {
        "sslmode": DB_SSLMODE,
    }


# PASSWORD VALIDATION

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# INTERNATIONALIZATION

LANGUAGE_CODE = "en-us"

TIME_ZONE = os.getenv("TIME_ZONE", "Africa/Lagos")

USE_I18N = True

USE_TZ = True


# STATIC AND MEDIA FILES

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
] if (BASE_DIR / "static").exists() else []

MEDIA_URL = "media/"

MEDIA_ROOT = BASE_DIR / "media"


# DEFAULT MODEL PRIMARY KEY

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# CUSTOM USER MODEL

AUTH_USER_MODEL = "accounts.User"


# DJANGO REST FRAMEWORK

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),

    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),

    "DEFAULT_PAGINATION_CLASS": (
        "rest_framework.pagination.PageNumberPagination"
    ),

    "PAGE_SIZE": 20,
}


# JWT CONFIGURATION

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),

    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),

    "ROTATE_REFRESH_TOKENS": True,

    "BLACKLIST_AFTER_ROTATION": True,

    "UPDATE_LAST_LOGIN": True,

    "ALGORITHM": "HS256",

    "SIGNING_KEY": os.getenv("JWT_SECRET_KEY", SECRET_KEY),

    "AUTH_HEADER_TYPES": ("Bearer",),

    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",

    "USER_ID_FIELD": "id",

    "USER_ID_CLAIM": "user_id",

    "TOKEN_TYPE_CLAIM": "token_type",
}


# EMAIL CONFIGURATION (DJANGO 6.1+)

EMAIL_HOST = os.getenv("EMAIL_HOST", "localhost")

EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))

EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", True)

EMAIL_USE_SSL = env_bool("EMAIL_USE_SSL", False)

if EMAIL_USE_TLS and EMAIL_USE_SSL:
    raise ValueError(
        "EMAIL_USE_TLS and EMAIL_USE_SSL cannot both be True."
    )

# Local development uses the console backend.
# Production uses SMTP.

EMAIL_BACKEND = (
    "django.core.mail.backends.console.EmailBackend"
    if DEBUG
    else "django.core.mail.backends.smtp.EmailBackend"
)

MAILERS = {
    "default": {
        "BACKEND": EMAIL_BACKEND,

        "OPTIONS": {
            "host": EMAIL_HOST,
            "port": EMAIL_PORT,
            "username": os.getenv("EMAIL_HOST_USER", ""),
            "password": os.getenv("EMAIL_HOST_PASSWORD", ""),
            "use_tls": EMAIL_USE_TLS,
            "use_ssl": EMAIL_USE_SSL,
            "timeout": int(os.getenv("EMAIL_TIMEOUT", "30")),
        },
    },
}

DEFAULT_FROM_EMAIL = os.getenv(
    "DEFAULT_FROM_EMAIL",
    "no-reply@example.com",
)

SERVER_EMAIL = os.getenv(
    "SERVER_EMAIL",
    DEFAULT_FROM_EMAIL,
)

EMAIL_SUBJECT_PREFIX = os.getenv(
    "EMAIL_SUBJECT_PREFIX",
    "[Application] ",
)


# AUTHENTICATION URL

LOGIN_URL = "/api/v1/auth/login/"

PASSWORD_RESET_TIMEOUT = 60 * 60  # 1 hour


# SECURITY SETTINGS

SECURE_SSL_REDIRECT = env_bool(
    "SECURE_SSL_REDIRECT",
    not DEBUG,
)

SESSION_COOKIE_SECURE = not DEBUG

CSRF_COOKIE_SECURE = not DEBUG

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_REFERRER_POLICY = "same-origin"

X_FRAME_OPTIONS = "DENY"

# Configure this only when your hosting proxy sets
# X-Forwarded-Proto correctly.
if env_bool("USE_X_FORWARDED_PROTO", False):
    SECURE_PROXY_SSL_HEADER = (
        "HTTP_X_FORWARDED_PROTO",
        "https",
    )

# HSTS should only be enabled after HTTPS is working correctly.
SECURE_HSTS_SECONDS = (
    int(os.getenv("SECURE_HSTS_SECONDS", "31536000"))
    if not DEBUG
    else 0
)

SECURE_HSTS_INCLUDE_SUBDOMAINS = (
    not DEBUG and env_bool("SECURE_HSTS_INCLUDE_SUBDOMAINS", False)
)

SECURE_HSTS_PRELOAD = (
    not DEBUG and env_bool("SECURE_HSTS_PRELOAD", False)
)


# LOGGING

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "verbose": {
            "format": (
                "{levelname} {asctime} {name} "
                "{message}"
            ),
            "style": "{",
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },

    "root": {
        "handlers": ["console"],
        "level": os.getenv("LOG_LEVEL", "INFO"),
    },
}
