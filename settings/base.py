import environ

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
env.read_env(BASE_DIR / ".env")

SECRET_KEY = "default-secret-key"
DEBUG = False

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "jazzmin",  # django-jazzmin
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # custom apps,
    "apps.core",
    "apps.account",
    "apps.htmx",
    # plugins
    "tailwind",
    "theme",
    "crispy_forms",
    "crispy_tailwind",
    "django_filters",
    # "django_ckeditor_5",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.htmx.middleware.HtmxMessagesMiddleware",
]

ROOT_URLCONF = "settings.urls.base"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.breadcrumbs",
            ],
        },
    },
]

WSGI_APPLICATION = "configs.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "vi-vn"
TIME_ZONE = "Asia/Saigon"

USE_I18N = True
USE_TZ = False

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles" / "static"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom base
AUTH_USER_MODEL = "account.UserCustom"
LOGIN_URL = "/account/sign_in"
X_FRAME_OPTIONS = "SAMEORIGIN"

# Django-Tailwind
TAILWIND_APP_NAME = "theme"

# Crispy-form
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

# Django-jazzmin
JAZZMIN_SETTINGS = {
    "site_logo": "imgs/logo.jpg",
    "site_brand": "Sanbongssc",
    "user_avatar": "avatar",
    "related_modal_active": True,
    "search_model": ["account.UserCustom", "core.Booking", "core.Payment"],
    "icons": {
        "account.UserCustom": "fas fa-user",
        "account.UserAddress": "fas fa-map-marker-alt",
        "auth.Group": "fas fa-users",
        "core.Payment": "fas fa-cash-register",
        "core.Pitch": "fas fa-futbol",
        "core.Booking": "fas fa-hand-holding-usd",
    },
}


# Django-filter
def FILTERS_VERBOSE_LOOKUPS():
    from django_filters.conf import DEFAULTS

    verbose_lookups = DEFAULTS["VERBOSE_LOOKUPS"].copy()
    verbose_lookups.update(
        {
            "lt": "thấp hơn",
            "gt": "lớn hơn",
        }
    )
    return verbose_lookups


# Django-ckeditor-5
# CKEDITOR_5_ALLOW_ALL_FILE_TYPES = True
# CKEDITOR_5_UPLOAD_FILE_TYPES = ["jpeg", "jpg", "png", "webp"]
# CKEDITOR_5_FILE_UPLOAD_PERMISSION = "staff"
# customColorPalette = [
#     {"color": "hsl(4, 90%, 58%)", "label": "Red"},
#     {"color": "hsl(340, 82%, 52%)", "label": "Pink"},
#     {"color": "hsl(291, 64%, 42%)", "label": "Purple"},
#     {"color": "hsl(262, 52%, 47%)", "label": "Deep Purple"},
#     {"color": "hsl(231, 48%, 48%)", "label": "Indigo"},
#     {"color": "hsl(207, 90%, 54%)", "label": "Blue"},
# ]

# CKEDITOR_5_CONFIGS = {
#     "default": {
#         "toolbar": [
#             "heading",
#             "|",
#             "outdent",
#             "indent",
#             "|",
#             "bold",
#             "italic",
#             "link",
#             "underline",
#             "strikethrough",
#             "sourceEditing",
#             "highlight",
#             "|",
#             "insertImage",
#             "blockQuote",
#             "|",
#             "bulletedList",
#             "numberedList",
#             "todoList",
#             "|",
#             "fontSize",
#             "fontFamily",
#             "fontColor",
#             "fontBackgroundColor",
#             "|",
#             "mediaEmbed",
#             "removeFormat",
#             "insertTable",
#         ],
#         "language": "vi",
#     }
# }
