"""
Production settings for Render deployment.

Variables d'environnement requises sur Render :
- SECRET_KEY                (auto-generate via render.yaml)
- DATABASE_URL              (auto-injecté par le service Postgres de Render)
- ALLOWED_HOSTS             (ex: "monapp.onrender.com,api.mondomaine.com")
- CORS_ALLOWED_ORIGINS      (ex: "https://mon-front.onrender.com")
- CSRF_TRUSTED_ORIGINS      (ex: "https://mon-front.onrender.com")
- FRONTEND_URL              (URL publique du front)
- DJANGO_SETTINGS_MODULE    = "config.settings.production"

Optionnelles (selon les modules utilisés) :
- REDIS_URL, CELERY_BROKER_URL, CELERY_RESULT_BACKEND
- EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, SENDGRID_API_KEY
- TWILIO_*, SLACK_*, GROK_API_KEY
"""
import os
import dj_database_url

from .base import *  # noqa

# ─── Sécurité ────────────────────────────────────────────────────────────────
DEBUG = False

# SECRET_KEY : obligatoire en prod, pas de fallback insecure
SECRET_KEY = env("SECRET_KEY")

# ALLOWED_HOSTS : injecter via env. Render fournit RENDER_EXTERNAL_HOSTNAME.
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])
_render_host = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if _render_host and _render_host not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(_render_host)

# ─── Base de données : DATABASE_URL injecté par Render ──────────────────────
DATABASES = {
    "default": dj_database_url.config(
        default=env("DATABASE_URL", default=""),
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=True,
    )
}

# ─── CORS / CSRF ─────────────────────────────────────────────────────────────
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

# ─── Static files (whitenoise est déjà dans MIDDLEWARE via base.py) ─────────
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ─── Sécurité HTTP ───────────────────────────────────────────────────────────
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = "DENY"

# ─── Channels : pas de Redis local en prod, on bascule sur InMemory ──────────
# Si tu as un Redis sur Render, surcharge avec REDIS_URL.
_redis_url = os.environ.get("REDIS_URL")
if _redis_url:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {"hosts": [_redis_url]},
        },
    }
else:
    CHANNEL_LAYERS = {
        "default": {"BACKEND": "channels.layers.InMemoryChannelLayer"},
    }

# ─── Email : pas de SendGrid forcé si pas configuré ─────────────────────────
if os.environ.get("SENDGRID_API_KEY"):
    EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# ─── Logging : stdout uniquement (Render capte stdout) ──────────────────────
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
