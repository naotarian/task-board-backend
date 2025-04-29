import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY")


DEBUG = True

ALLOWED_HOSTS = ['backend', 'nginx', ".localhost", ".tskb"]

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'users',
    'projects',
    'storages',
    'organizations',
    'shared',
]
REST_FRAMEWORK = {
    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #     'rest_framework_simplejwt.authentication.JWTAuthentication',
    # )
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'shared.middleware.subdomain_middleware.SubdomainMiddleware'
]
# CORS_ALLOWED_ORIGIN_REGEXES = [
#     r"^http:\/\/([a-zA-Z0-9-]+)\.localhost:3000$",
#     r"^http:\/\/localhost:3000$",]
# クロスオリジンでCookie送信許可（credentials: 'include'対応）
CORS_ALLOW_CREDENTIALS = True

# 許可するオリジンリスト（開発環境用）
# CORS_ALLOWED_ORIGINS = [
# #   '*'
#     "http://localhost:3000",
#     "http://test1.localhost:3000/",
# ]
CORS_ALLOW_ALL_ORIGINS = True

# 許可するオリジンパターン（サブドメイン付き localhost用）
# CORS_ALLOWED_ORIGIN_REGEXES = [
#     r"^http:\/\/([a-zA-Z0-9-]+)\.localhost:3000$",
# ]

# 許可するカスタムヘッダー
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "x-subdomain",
    'x-csrftoken',
    'x-requested-with',
    'access-control-allow-origin',
]

# CSRF対策（Cookieベース認証を守るために必要）
CSRF_TRUSTED_ORIGINS = [
    "https://localhost",
    "https://test1.localhost",
]
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'None'

ROOT_URLCONF = 'config.urls'
LANGUAGE_CODE = 'ja-jp'
LANGUAGE_COOKIE_SECURE = True
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
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'app_db'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'secret'),
        'HOST': os.getenv('DB_HOST', 'db'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CORS_ALLOW_ALL_ORIGINS = True

LOG_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'django.log'),
        },
        'console': {  # ← consoleハンドラー追加！
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',  # 見やすくする
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
        'development': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],  # consoleハンドラーにする
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
# SIMPLE_JWT = {
#     "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
#     "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
#     "ROTATE_REFRESH_TOKENS": False,
#     "BLACKLIST_AFTER_ROTATION": False,
# }


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mailhog'
EMAIL_PORT = 1025
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'no-reply@example.com'
AUTH_USER_MODEL = "users.User"


# Storage
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL")  # MinIO用
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME", "ap-northeast-1")

# MinIO用のアドレッシングスタイル
AWS_S3_ADDRESSING_STYLE = os.getenv("AWS_S3_ADDRESSING_STYLE", "path")

# 開発用に署名付きURLを使わない設定（必要なら）
AWS_QUERYSTRING_AUTH = False
