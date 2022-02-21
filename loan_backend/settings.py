"""
Django settings for loan_backend project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from configurations import Configuration
from pathlib import Path
from datetime import timedelta
import os


class Base(Configuration):
    BASE_DIR = Path(__file__).resolve().parent.parent

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = os.getenv('DJANGO_SECRET_KEY_LOAN', '')

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    ALLOWED_HOSTS = []

    DJANGO_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]

    MY_APPS = [
        'app.users',
        'app.accounts',
        'app.api',
    ]

    THIRD_PARTY_APPS = [
        'rest_framework',
        'rest_framework.authtoken',
        'django_extensions',
        'phonenumber_field',
        'djmoney',
        'dj_rest_auth',
    ]

    INSTALLED_APPS = DJANGO_APPS + MY_APPS + THIRD_PARTY_APPS

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'loan_backend.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'loan_backend.wsgi.application'

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

    # Internationalization
    # https://docs.djangoproject.com/en/3.2/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/3.2/howto/static-files/

    STATIC_URL = '/static/'

    # Default primary key field type
    # https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

    # Custom settings
    AUTH_USER_MODEL = 'users.User'

    REST_USE_JWT = True
    JWT_AUTH_COOKIE = 'jwt'
    JWT_AUTH_REFRESH_COOKIE = 'jwt-refresh'

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
        )
    }


class Dev(Base):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'HOST': 'jelani.db.elephantsql.com',
            'NAME': os.getenv('LOAN_DB_NAME'),
            'USER': os.getenv('LOAN_DB_NAME'),
            'PASSWORD': os.getenv('LOAN_DB_PASSWORD'),
            'PORT': '5432',
        }
    }

    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
    AWS_S3_ACCESS_KEY_ID = os.getenv('DIMO_AWS_ACCESS_KEY')
    AWS_S3_SECRET_ACCESS_KEY = os.getenv('DIMO_AWS_SECRET_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('DIMO_BUCKET_NAME')

    SIMPLE_JWT = {
        'ACCESS_TOKEN_LIFETIME': timedelta(days=30)
    }
