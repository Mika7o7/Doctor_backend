from .settings_base import *  # noqa

INSTALLED_APPS = [
    "daphne",
    "channels",
    "django_cleanup",
    "modeltranslation",
    "rest_framework.authtoken",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "drf_yasg",
    "rest_framework",
    "corsheaders",
    "api.apps.ApiConfig",
    "django.contrib.sites",
    "django_celery_results",
    "chat",
    "evants",
    "blog",
]

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "my_doctor.urls"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "my_doctor.authentication.CustomTokenAuthentication",
    ],
}


CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"


CELERY_RESULT_BACKEND = "django-db"


# celery setting.
CELERY_CACHE_BACKEND = "default"

# django setting.
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
    }
}

ALLOWED_HOSTS = ["*"]

CORS_ORIGIN_ALLOW_ALL = True
