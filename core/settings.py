from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent


# =========================
# SECURITY
# =========================

SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-!b4lyffhc6)vo4fj)9)hu!)dmp(er=kj4pk)_02g4o&83k4f=5")

DEBUG = True

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    ".onrender.com"
]


# =========================
# APPLICATIONS
# =========================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_ckeditor_5',
    'tutorials',
]


# =========================
# MIDDLEWARE
# =========================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'core.urls'


# =========================
# TEMPLATES
# =========================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'tutorials.context_processors.extras',
                'tutorials.context_processors.global_subjects',
            ],
        },
    },
]


WSGI_APPLICATION = 'core.wsgi.application'


# =========================
# DATABASE (RENDER POSTGRES)
# =========================

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get("postgresql://copahub_db_4abr_user:4TI8co9E1RkrSEaLVzchMcVYeqUuhx1B@dpg-d7uehtegvqtc73fbk7f0-a/copahub_db_4abr")
    )
}


# =========================
# PASSWORD VALIDATION
# =========================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# =========================
# INTERNATIONALIZATION
# =========================

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# =========================
# STATIC FILES (IMPORTANT FOR RENDER)
# =========================

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# =========================
# MEDIA FILES
# =========================

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# =========================
# DEFAULT PRIMARY KEY
# =========================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =========================
# CKEDITOR CONFIG
# =========================

CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_5_CONFIGS = {
    'extends': {
        'toolbar': [
            'heading', '|',
            'bold', 'italic', 'link',
            'bulletedList', 'numberedList', 'blockQuote',
            'imageUpload',
        ],
    },
}


# =========================
# SECURITY HEADERS (OPTIONAL BUT GOOD)
# =========================

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')



import dj_database_url
import os

DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"
    )
}