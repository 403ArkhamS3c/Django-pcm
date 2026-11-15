
from pathlib import Path
import os

import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


# ==================================================
# SECURITY
# ==================================================

SECRET_KEY = os.getenv("SECRET_KEY", "")

DEBUG = os.getenv("DEBUG", "False").lower() in (
    "true", "1", "yes", "on"
)

if not SECRET_KEY:
    if not DEBUG:
        raise ValueError("SECRET_KEY wajib diatur ketika DEBUG=False.")

    SECRET_KEY = "django-insecure-kunci-sementara-untuk-lokal"

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        "ALLOWED_HOSTS",
        "127.0.0.1,localhost,.vercel.app"
    ).split(",")
    if host.strip()
]

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CSRF_TRUSTED_ORIGINS", ""
    ).split(",")
    if origin.strip()
]

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)

SECURE_SSL_REDIRECT = os.getenv(
    "SECURE_SSL_REDIRECT",
    "False" if DEBUG else "True"
).lower() == "true"

SESSION_COOKIE_SECURE = os.getenv(
    "SESSION_COOKIE_SECURE",
    "False" if DEBUG else "True"
).lower() == "true"

CSRF_COOKIE_SECURE = os.getenv(
    "CSRF_COOKIE_SECURE",
    "False" if DEBUG else "True"
).lower() == "true"

SECURE_HSTS_SECONDS = int(
    os.getenv("SECURE_HSTS_SECONDS", "0")
)


# ==================================================
# APPLICATION
# ==================================================

INSTALLED_APPS = [
    "unfold",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "core.apps.CoreConfig",
]

UNFOLD = {
    "SITE_TITLE": "PCM Grogol Admin",
    "SITE_HEADER": "PCM Grogol",
    "SITE_SUBHEADER": "Panel Pengelolaan Website",
    "SITE_URL": "/",
    "SITE_SYMBOL": "account_balance",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "COLORS": {
        "primary": {
            "50": "240 253 244",
            "100": "220 252 231",
            "200": "187 247 208",
            "300": "134 239 172",
            "400": "74 222 128",
            "500": "34 197 94",
            "600": "22 163 74",
            "700": "21 128 61",
            "800": "22 101 52",
            "900": "20 83 45",
            "950": "5 46 22",
        },
    },
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.tautan_footer",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# ==================================================
# DATABASE
# ==================================================

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=0,
            conn_health_checks=True,
        )
    }

    DATABASES["default"]["DISABLE_SERVER_SIDE_CURSORS"] = True

else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# ==================================================
# PASSWORD VALIDATION
# ==================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# ==================================================
# INTERNATIONALIZATION
# ==================================================

LANGUAGE_CODE = "id"

TIME_ZONE = "Asia/Jakarta"

USE_I18N = True
USE_TZ = True


# ==================================================
# STATIC FILES
# ==================================================

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"


# ==================================================
# MEDIA STORAGE - SUPABASE
# ==================================================

USE_SUPABASE_STORAGE = (
    os.getenv("USE_SUPABASE_STORAGE", "False").lower() == "true"
)

if USE_SUPABASE_STORAGE:
    AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
    AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
    AWS_STORAGE_BUCKET_NAME = os.environ["AWS_STORAGE_BUCKET_NAME"]
    AWS_S3_ENDPOINT_URL = os.environ["AWS_S3_ENDPOINT_URL"]
    AWS_S3_REGION_NAME = os.environ["AWS_S3_REGION_NAME"]

    AWS_S3_ADDRESSING_STYLE = "path"
    AWS_S3_SIGNATURE_VERSION = "s3v4"
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None

    # Bucket harus bersifat public untuk konfigurasi ini.
    AWS_QUERYSTRING_AUTH = False

    SUPABASE_PROJECT_URL = os.environ["SUPABASE_PROJECT_URL"]

    AWS_S3_CUSTOM_DOMAIN = (
        f"{SUPABASE_PROJECT_URL.removeprefix('https://')}"
        f"/storage/v1/object/public/{AWS_STORAGE_BUCKET_NAME}"
    )

    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

else:
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# ==================================================
# EMAIL
# ==================================================

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "localhost")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() == "true"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.getenv(
    "DEFAULT_FROM_EMAIL",
    EMAIL_HOST_USER
)


# ==================================================
# OTHER
# ==================================================

APPEND_SLASH = True
