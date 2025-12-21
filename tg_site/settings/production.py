from .base import *
import os

DEBUG = False

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

CSRF_TRUSTED_ORIGINS = [
    "https://tg-aprilov.com",
    "https://www.tg-aprilov.com",
]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
