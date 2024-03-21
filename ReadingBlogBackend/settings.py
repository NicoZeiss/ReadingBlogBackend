import os

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-r6j1w5f1kc=v=0d8$l+f3pgyt6b&5dg#ew&bf=v+jsj7#qrv_u'

DEBUG = True

ALLOWED_HOSTS = ['localhost']


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_ckeditor_5',

    'rb_books',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ReadingBlogBackend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'ReadingBlogBackend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'rb_db',
        'USER': 'rb_db_user',
        'PASSWORD': 'rb_db_user_password',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'

if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
    ]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Jazzmin config
# Available icons https://fontawesome.com/v5/search
X_FRAME_OPTIONS = 'SAMEORIGIN'

JAZZMIN_SETTINGS = {
    'show_ui_builder': True,
    'site_title': 'LVDK - Admin',
    'site_header': 'Les Victimes de Kelith',
    "site_brand": "Les Victimes de Kelith",
    'site_logo': 'img/lvdk_logo.png',
    "welcome_sign": "Bienvenue",
    "copyright": "NicoZeiss",
    "search_model": [
        "rb_books.Book",
        "rb_books.Collection",
        "rb_books.Author",
        "rb_books.Editor"
    ],
    "topmenu_links": [
        {
            "name": "Vers le site",
            "url": "https://lesvictimesdekelith.blogspot.com/",
            "new_window": True
        },
    ],
    "usermenu_links": [
        {
            "name": "Facebook",
            "icon": "fab fa-facebook",
            "url": "https://www.facebook.com/LesVictimesdeKelith/",
            "new_window": True
        },
        {
            "name": "Twitter",
            "icon": "fab fa-twitter",
            "url": "https://twitter.com/ladykelith",
            "new_window": True
        },
        {
            "name": "Livraddict",
            "icon": "fas fa-blog",
            "url": "https://www.livraddict.com/profil/kelith/",
            "new_window": True
        },
        {
            "name": "Blogger",
            "icon": "fas fa-blog",
            "url": "https://www.blogger.com/profile/09384048323067180573",
            "new_window": True
        },
    ],
    "order_with_respect_to": [
        "rb_books.Book",
        "rb_books.Collection",
        "rb_books.Volume",
        "rb_books.Author",
        "rb_books.Editor",
        "rb_books.Category",
        "rb_books.Genre",
        "rb_books.Audience",
        "rb_books.Rating",
    ],
    "icons": {
        "rb_books.Book": "fas fa-book",
        "rb_books.Collection": "fas fa-sitemap",
        "rb_books.Volume": "fas fa-sort-numeric-down",
        "rb_books.Author": "fas fa-feather-alt",
        "rb_books.Editor": "fas fa-glasses",
        "rb_books.Category": "fas fa-thumbtack",
        "rb_books.Genre": "fas fa-dragon",
        "rb_books.Audience": "fas fa-bullseye",
        "rb_books.Rating": "fas fa-star-half-alt",
    },
    "custom_links": {},
    "related_modal_active": True,
    "changeform_format": "horizontal_tabs",
}
