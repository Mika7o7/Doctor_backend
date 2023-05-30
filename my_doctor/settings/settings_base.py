import os

import environ

env = environ.Env()

environ.Env.read_env()

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)


SECRET_KEY = env("SECRET_KEY")

DEBUG = env("DEBUG", default=False)

ALLOWED_HOSTS = env("ALLOWED_HOSTS", default="*").split()


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI_APPLICATION = "my_doctor.wsgi.application"

# Add path of asgi application.
ASGI_APPLICATION = "my_doctor.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

if env("USE_SQLITE", default=False):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": env("DATABASE_NAME"),
            "USER": env("DATABASE_USER"),
            "PASSWORD": env("DATABASE_PASSWORD"),
            "HOST": env("DATABASE_HOST", default="localhost"),
            "PORT": env("DATABASE_PORT", default="5432"),
        }
    }

VALIDATORS_PATH = "django.contrib.auth.password_validation"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": f"{VALIDATORS_PATH}.UserAttributeSimilarityValidator",
    },
    {
        "NAME": f"{VALIDATORS_PATH}.MinimumLengthValidator",
    },
    {
        "NAME": f"{VALIDATORS_PATH}.CommonPasswordValidator",
    },
    {
        "NAME": f"{VALIDATORS_PATH}.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "hy"

TIME_ZONE = "Asia/Yerevan"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (
    ("hy", "Armenian"),
    ("ru", "Russian"),
    ("en", "English"),
)

MODELTRANSLATION_DEFAULT_LANGUAGE = "hy"

MODELTRANSLATION_LANGUAGES = ("hy", "ru", "en")

STATIC_URL = "static/"

if DEBUG:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")

# STATIC_ROOT = os.path.join(BASE_DIR, "static")


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

DJANGORESIZED_DEFAULT_QUALITY = 70
DJANGORESIZED_DEFAULT_KEEP_META = False
DJANGORESIZED_DEFAULT_FORCE_FORMAT = "JPEG"
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {"JPEG": ".jpg"}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True

AUTH_USER_MODEL = "api.User"


# Email settings
# SMTP settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")


BACKEND_URL = env("BACKEND_URL")
FRONTEND_URL = env("FRONTEND_URL")
