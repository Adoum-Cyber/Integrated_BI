#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
#  Build script exécuté par Render à chaque déploiement.
#  Utilise DJANGO_SETTINGS_MODULE=config.settings.production
# ─────────────────────────────────────────────────────────────────────────────
set -o errexit

echo "─── Installing Python dependencies ────────────────────────────────────"
pip install --upgrade pip
pip install -r requirements.txt

echo "─── Collecting static files ──────────────────────────────────────────"
python manage.py collectstatic --no-input

echo "─── Applying database migrations ─────────────────────────────────────"
python manage.py migrate --no-input

echo "─── Build terminé ✓ ───────────────────────────────────────────────────"
