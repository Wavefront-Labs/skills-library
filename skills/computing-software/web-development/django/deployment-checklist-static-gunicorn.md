---
id: computing-software.web-development.django.deployment-checklist-static-gunicorn
name: deployment-checklist-static-gunicorn
category: computing-software
field: web-development
product: django
tags: [django, deployment-checklist, whitenoise, gunicorn, collectstatic, check-deploy, production-settings, python, web-development]
level: practitioner
status: docs-checked
description: "Deploying Django to production: manage.py check --deploy, security settings, collectstatic with WhiteNoise or a CDN, gunicorn workers, proxies and health checks."
sources:
  - https://docs.djangoproject.com/en/stable/howto/deployment/checklist/
  - https://whitenoise.readthedocs.io/
  - https://docs.gunicorn.org/en/stable/design.html#how-many-workers
  - https://docs.djangoproject.com/en/stable/howto/static-files/deployment/
  - https://docs.djangoproject.com/en/stable/ref/middleware/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deployment checklist, static files and gunicorn

**Goal:** a production Django that passes `check --deploy`, serves static files efficiently and survives load.

## 1. Run the checks
```bash
DJANGO_SETTINGS_MODULE=config.settings.prod python manage.py check --deploy --fail-level WARNING
```
Fix every warning or document why it doesn't apply.

## 2. Core settings
```python
DEBUG = False
SECRET_KEY = env("SECRET_KEY")                       # unique, long, not in git
ALLOWED_HOSTS = ["example.com"]
CSRF_TRUSTED_ORIGINS = ["https://example.com"]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")   # only behind a proxy that sets it
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000; SECURE_HSTS_INCLUDE_SUBDOMAINS = True; SECURE_HSTS_PRELOAD = True  # ramp up from 3600
CONN_MAX_AGE = 60; CONN_HEALTH_CHECKS = True
LOGGING = {...}                                       # errors to stdout / Sentry
ADMINS / SERVER_EMAIL or Sentry for error reports
```
Start HSTS small (Django's docs suggest 3600 for testing, then increase; 31536000 is common) and read Django's HTTP Strict Transport Security notes before enabling `SECURE_HSTS_PRELOAD`.

## 3. Static files
```python
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")   # right after SecurityMiddleware
```
`python manage.py collectstatic --noinput` in the build. Manifest storage gives hashed filenames, which WhiteNoise treats as immutable files (see `WHITENOISE_MAX_AGE` and `WHITENOISE_IMMUTABLE_FILE_TEST`). A missing manifest entry raises at render time - run collectstatic in CI. Media (user uploads) is not served by WhiteNoise; use S3/object storage or nginx.

## 4. Gunicorn
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4 --threads 2 \
  --timeout 30 --graceful-timeout 30 --max-requests 1000 --max-requests-jitter 100 --access-logfile -
```
- Gunicorn's design docs give workers = (2 x CPU cores) + 1 as a starting point and say it typically needs only 4-12 workers for heavy traffic.
- `--max-requests` recycles workers to contain slow leaks.
- Behind nginx/a load balancer; gunicorn shouldn't face the internet directly (slow-client buffering).
- ASGI apps: Gunicorn has a native ASGI worker (`--worker-class asgi`) and also documents `-k uvicorn.workers.UvicornWorker`.

## 5. Migrations and release
Run `migrate` as a release step (one instance), not on every container start. Keep migrations backward-compatible with the running version.

## 6. Health and ops
A `/healthz` view that checks DB connectivity; exclude it from logs and auth. Set up error tracking, uptime monitoring and database backups with tested restores.

## Verify
- [ ] `check --deploy` clean in CI with production settings.
- [ ] `curl -I https://example.com/static/<hashed>.css` shows long `max-age` and compression.
- [ ] `DEBUG` is False in production (a 404 shows the custom page, not the debug page).

## Checked
Date: 2026-10-25. Documentation: Django documentation source (django/django main branch, 6.2 in development, commit of 2026-10-23; release notes 4.0 to 6.0) (howto/deployment/checklist, ref/settings, ref/middleware HSTS section, ref/django-admin check), WhiteNoise docs source (evansd/whitenoise main), Gunicorn docs source (benoitc/gunicorn master, design and settings pages).
Confirmed: `check --deploy` and `--fail-level` (default ERROR), `SECRET_KEY`, `ALLOWED_HOSTS`, `SECURE_HSTS_SECONDS` ramp-up guidance, `CONN_HEALTH_CHECKS`, WhiteNoise middleware placement after SecurityMiddleware and `CompressedManifestStaticFilesStorage`, manifest `ValueError`, media not served by WhiteNoise, Gunicorn `--timeout` default 30, `--graceful-timeout`, `--max-requests` and jitter, `--threads`, buffering-proxy guidance.
Corrected or removed: the unsupported "2-4 workers per container" figure, the "preload is hard to undo" wording, and the uvicorn-only ASGI line.
Method: documentation only; no commands were run.
