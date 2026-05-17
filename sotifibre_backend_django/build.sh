#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
#  Build script exécuté par Render à chaque déploiement.
#  DJANGO_SETTINGS_MODULE=config.settings.production
# ─────────────────────────────────────────────────────────────────────────────
set -o errexit

echo "─── Installing Python dependencies ────────────────────────────────────"
pip install --upgrade pip
pip install -r requirements.txt

echo "─── Collecting static files ──────────────────────────────────────────"
python manage.py collectstatic --no-input --clear

echo "─── Applying database migrations ─────────────────────────────────────"
python manage.py migrate --no-input

# ─── Superuser bootstrap : créé une seule fois si les env vars sont set ────
# Render env vars à définir :
#   DJANGO_SUPERUSER_EMAIL
#   DJANGO_SUPERUSER_PASSWORD
#   DJANGO_SUPERUSER_USERNAME (optionnel)
if [[ -n "${DJANGO_SUPERUSER_EMAIL:-}" && -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]]; then
  echo "─── Ensuring superuser exists ────────────────────────────────────────"
  python manage.py shell <<PY
import os
from django.contrib.auth import get_user_model
User = get_user_model()
email = os.environ["DJANGO_SUPERUSER_EMAIL"]
password = os.environ["DJANGO_SUPERUSER_PASSWORD"]
username = os.environ.get("DJANGO_SUPERUSER_USERNAME", email)
user, created = User.objects.get_or_create(
    email=email,
    defaults={"username": username, "is_staff": True, "is_superuser": True, "is_active": True},
)
# Toujours (re)synchroniser le mot de passe et les flags admin
user.set_password(password)
user.is_staff = True
user.is_superuser = True
user.is_active = True
user.save()
print(f"Superuser {'créé' if created else 'mis à jour'} : {email}")
PY
else
  echo "─── Superuser bootstrap skipped (DJANGO_SUPERUSER_* non définis) ────"
fi

echo "─── Build terminé ✓ ───────────────────────────────────────────────────"
