# coding: utf-8
"""
Django settings for cafe_ole project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd-092_wt^8chq&6zip#e%p%bt^u0w=3*m5n)=@p!v#2*nee*21'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'api',
    'web',
    # 'devserver',
    # 'debug_toolbar',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'mobility.middleware.DetectMobileMiddleware',
    'mobility.middleware.XMobileMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INTERNAL_IPS = ('127.0.0.1',)

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'street_movie',  # Or path to database file if using sqlite3.
        'USER': 'street_movie',  # Not used with sqlite3.
        'PASSWORD': 'changeme',  # Not used with sqlite3.
        'HOST': 'localhost',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',  # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': {"init_command": "SET storage_engine=INNODB"},
        'ATOMIC_REQUEST': True,
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'ja-jp'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = ''

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(os.path.join(BASE_DIR, ''), '../static/street_movie/static/'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'street_movie/templates/'),
)

LOGGING_DEBUG = DEBUG

LOGIN_URL = '/backend/login/'
LOGIN_REDIRECT_URL = '/backend/'

# A regex for detecting mobile user agents.
MOBILE_USER_AGENTS = 'android|fennec|iemobile|iphone|opera (?:mini|mobi)'
# The name of the cookie to set if the user prefers the mobile site.
MOBILE_COOKIE = 'mobile'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the web admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/path/to/app.log',
            'maxBytes': 1024 * 1024 * 5 * 100,  # 500MB
            'backupCount': 10,
            'formatter': 'standard'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'api': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'libs': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'web': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'decorator': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'backend': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

MOVIE_DEST_PATH = '/path/to/temporary/movie/directory'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = 'aws_access_key'
AWS_SECRET_ACCESS_KEY = 'aws_secret_access_key'
AWS_STORAGE_BUCKET_NAME = 'bucket_name'
AWS_HEADERS = {
    'Expires': 'Thu, 15 Apr 2100 20:00:00 GMT',
    'Cache-Control': 'max-age=86400',
}

FFMPEG_COMMAND = '/path/to/ffmpeg -r 15 -i %s/%%05d.jpg -vcodec libx264 -qscale:v 0 %s'
STREET_VIEW_URL = 'http://maps.googleapis.com/maps/api/streetview?size=600x300&location=%s,%%20%s&key=%s&sensor=false%s'

GOOGLE_API_KEY = 'Your google api key'