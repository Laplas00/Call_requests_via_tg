import os
from pathlib import Path
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-&(9v#1oxj(knjv0*fd^ih__t(*$*#z785alv=l_e-ycfjr_7c('
DEBUG = True

ALLOWED_HOSTS = ['116.203.69.73', 'localhost',
                 'salesarm.multywhale.pro', 'www.salesarm.multywhale.pro']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'django_telegram_login',
    'register',
    'home',
]


TELEGRAM_BOT_NAME = 'Login_TGKitGroupBot'
TELEGRAM_BOT_TOKEN = '8106105403:AAHNSy5s0pfl9DLC-42nPdaHWoPx_KlwFNI'
TELEGRAM_LOGIN_REDIRECT_URL = 'http://0.0.0.0:8000'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'csp.middleware.CSPMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'register.csp_middleware.CSPMiddleware',
]

CSP_DEFAULT_SRC = ("'self'", '*')
CSP_FRAME_ANCESTORS = ("'self'", "*")
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"

ROOT_URLCONF = 'request_panel_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'request_panel_site/templates'],
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

WSGI_APPLICATION = 'request_panel_site.wsgi.application'

MESSAGE_TAGS = {
        messages.DEBUG: 'alert-secondary',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
 }

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


#----------------
#NICE!
STATIC_URL = 'static/'
STATICFILES_LOCATION = 'static'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'request_panel_site/static'),
]
# MEDIA_ROOT = '/home/req_panel_site/public_html/media/'
# MEDIA_URL = '/media/'
#----------------
# Ensure the security settings are appropriate for testing

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login/'
LOGIN_REDIRECT_URL = 'login'
LOGOUT_REDIRECT_URL = 'login'
