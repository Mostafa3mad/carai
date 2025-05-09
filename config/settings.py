"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
# from decouple import config
import os
from datetime import timedelta



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = config('SECRET_KEY')
SECRET_KEY = 'django-insecure-hb(m^t+2m0*m+o5#z_em3m7&8*$dczjc8uayykog3t1)03ti1$'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = config('DEBUG', cast=bool)
DEBUG = True

ALLOWED_HOSTS = ['*']
CORS_ALLOW_ALL_ORIGINS = True










STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# CORS_ALLOWED_ORIGINS = [
#     "https://example.com",
#     "https://sub.example.com",
#     "http://localhost:8080",
#     "http://127.0.0.1:9000",
# ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'register_user',
    'django_filters',
    'rating',
    'appointments',
    # 'model_ai',




    'corsheaders',
    'drf_yasg',



    "rest_framework.authtoken",
    "rest_registration",
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',




]
AUTH_USER_MODEL = 'register_user.CustomUser'


# JAZZMIN_SETTINGS = {
#     "site_title": "Django Admin",
#     "site_header": "Admin Dashboard",
#     "site_brand": "My Site",
#     "welcome_sign": "Welcome to My Admin Panel",
#     "show_dashboard": True,
# }




MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('DB_NAME'),
#         'USER': config('DB_USER'),
#         'PASSWORD': config('DB_PASSWORD'),
#         'PORT': config('DB_PORT',cast=int),
#         'HOST': config('DB_HOST'),
#     }
# }

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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'




REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'register_user.auth_backend.JWTAuthentication',  # تأكد من إضافة المسار الصحيح إلى فئة `JWTAuthentication`
        "rest_framework.authentication.SessionAuthentication",
        # "rest_framework.authentication.TokenAuthentication",
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}




REST_REGISTRATION = {
    "REGISTER_VERIFICATION_ENABLED": False,
    "REGISTER_EMAIL_VERIFICATION_ENABLED": False,
    "RESET_PASSWORD_VERIFICATION_ENABLED": True,
    'LOGIN_RETRIEVE_TOKEN': True,
    'AUTH_TOKEN_MANAGER_CLASS': 'register_user.auth_backend.AuthJWTManager',
    'REGISTER_AUTHENTICATION_CLASSES': (
        'register_user.auth_backend.JWTAuthentication',
    ),
    'REGISTER_SERIALIZER_CLASS': 'register_user.serializers.CustomRegisterUserSerializer',
    'REGISTER_OUTPUT_SERIALIZER_CLASS': 'register_user.serializers.CustomRegisterUserSerializer',

    'USER_LOGIN_FIELDS': ['email'],
    'USER_LOGIN_FIELDS_UNIQUE_CHECK_ENABLED': True,





    #reset password
    "VERIFICATION_FROM_EMAIL": "ks0894976@gmail.com",

    # 🔹 صلاحية روابط إعادة تعيين كلمة المرور
    "RESET_PASSWORD_VERIFICATION_PERIOD": timedelta(minutes=20),
    "RESET_PASSWORD_VERIFICATION_ONE_TIME_USE": True,

    "RESET_PASSWORD_VERIFICATION_URL": "https://mostafa3mad.pythonanywhere.com/api/reset-password/",
    # ✅ **قوالب الإيميلات**
    'RESET_PASSWORD_VERIFICATION_EMAIL_TEMPLATES': {
        'body': 'rest_registration/reset_password/body.txt',
        'subject': 'rest_registration/reset_password/subject.txt'
    },


}



AUTHENTICATION_BACKENDS = (
    'register_user.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)



from datetime import timedelta
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
    'BLACKLIST_AFTER_ROTATION': True,

}
# CORS_ALLOW_CREDENTIALS = True



# ✅ **تأكد من إعدادات الإيميل**
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'ks0894976@gmail.com'
EMAIL_HOST_PASSWORD = 'oiyq qksu gvta obak'  # استخدم "App Password"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
