"""
Django settings for socialmedia project.
"""

import os
from pathlib import Path

# BASE DIR
BASE_DIR = Path(__file__).resolve().parent.parent


# ========================
# SECURITY
# ========================

# SECRET KEY (Render me baad me env variable bana sakte ho)
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-change-this-in-production'
)

DEBUG = False   # ✅ production ke liye

ALLOWED_HOSTS = ['*']   # ✅ free hosting ke liye


# ========================
# APPLICATIONS
# ========================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'userauth',
]


# ========================
# MIDDLEWARE
# ========================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # ✅ Static files ke liye (IMPORTANT)
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ========================
# URL / TEMPLATES
# ========================

ROOT_URLCONF = 'socialmedia.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],   # templates folder
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

WSGI_APPLICATION = 'socialmedia.wsgi.application'


# ========================
# DATABASE
# ========================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',   # free deploy ke liye OK
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ========================
# PASSWORD VALIDATION
# ========================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ========================
# INTERNATIONALIZATION
# ========================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ========================
# STATIC FILES
# ========================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

# WhiteNoise storage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ========================
# MEDIA FILES (Uploads)
# ========================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ========================
# SESSIONS
# ========================

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_EXPIRE_AT_BROWSER_CLOSE = False


# ========================
# DEFAULT FIELD
# ========================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
