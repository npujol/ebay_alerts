"""
Django settings for ebay_alerts project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

import environ
from celery.schedules import crontab

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# reading .env file
environ.Env.read_env()

# False if not in os.environ
DEBUG = env("DEBUG")

# Raises django's ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = env("SECRET_KEY")
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

DEFAULT_BASE_URL = "http://localhost:8000"

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])


CORS_ALLOW_ALL_ORIGINS = True

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "drf_yasg",
    "django_celery_results",
    "apps.alerts.apps.AlertsConfig",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "ebay_alerts.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "tamplates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "ebay_alerts.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    # read os.environ['DATABASE_URL'] and raises ImproperlyConfigured exception if not found
    "default": env.db(default="sqlite://:memory:")
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static_files")]
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")


REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "rest_framework.views.exception_handler",
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_PARSER_CLASSES": ["rest_framework.parsers.JSONParser"],
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": [],
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}

SWAGGER_SETTINGS = {"USE_SESSION_AUTH": False}


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = env("MAILGUN_SMTP_SERVER", default="smtp.mailgun.org")
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = env("MAILGUN_SMTP_LOGIN", default="email")
EMAIL_HOST_PASSWORD = env("MAILGUN_SMTP_PASSWORD", default="password")

EBAY_APPID = env("EBAY_APPID", default="ebay_appid")


CELERY_BROKER_URL = env("REDIS_URL", default="redis://redis:6379")
CELERY_RESULT_BACKEND = env("REDIS_URL", default="redis://redis:6379")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"
CELERY_BEAT_SCHEDULE = {
    "send-alert-email-every-two-minutes-task": {
        "task": "send_alert_email_every_x_minutes_task",
        "schedule": crontab(minute="*/2"),
        "args": (2,),
    },
    "send-alert-email-every-ten-minutes-task": {
        "task": "send_alert_email_every_x_minutes_task",
        "schedule": crontab(minute="*/10"),
        "args": (10,),
    },
    "send-alert-email-every-thirty-minutes-task": {
        "task": "send_alert_email_every_x_minutes_task",
        "schedule": crontab(minute="*/30"),
        "args": (30,),
    },
}
