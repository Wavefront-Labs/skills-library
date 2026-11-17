---
id: computing-software.web-development.django.settings-management-and-secrets
name: settings-management-and-secrets
category: computing-software
field: web-development
product: django
tags: [django, django-settings, django-environ, secrets, twelve-factor, settings-modules, python, web-development]
level: practitioner
status: docs-checked
description: "Organising Django settings: environment-driven config with django-environ, split settings modules, secret handling, typed defaults and safe production overrides."
sources:
  - https://django-environ.readthedocs.io/
  - https://docs.djangoproject.com/en/stable/topics/settings/
  - https://12factor.net/config
  - https://docs.djangoproject.com/en/stable/howto/deployment/checklist/
  - https://docs.djangoproject.com/en/stable/ref/settings/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Settings management and secrets

**Goal:** one codebase, config from the environment, secrets never in git, and impossible to run production with dev defaults.

## 1. django-environ
```python
# config/settings/base.py
import environ
env = environ.Env(DEBUG=(bool, False))
BASE_DIR = Path(__file__).resolve().parents[2]
environ.Env.read_env(BASE_DIR / ".env")          # dev convenience; real env vars win

SECRET_KEY = env("SECRET_KEY")                     # no default: fail fast if missing
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])
DATABASES = {"default": env.db("DATABASE_URL")}    # postgres://user:pass@host:5432/db
CACHES = {"default": env.cache("REDIS_URL", default="locmemcache://")}
EMAIL_CONFIG = env.email("EMAIL_URL", default="consolemail://")
vars().update(EMAIL_CONFIG)
```
Typed parsing (`env.bool`, `env.int`, `env.list`, `env.json`) avoids the `"False"` string truthiness bug.

## 2. Split modules (optional)
```
config/settings/base.py     shared
config/settings/dev.py      from .base import *; DEBUG = True; debug toolbar
config/settings/test.py     fast hashers, locmem email
config/settings/prod.py     security settings, logging, Sentry
```
`DJANGO_SETTINGS_MODULE=config.settings.prod`. Keep differences small; most should be env values, not code branches. Point `manage.py` and `wsgi.py`/`asgi.py` defaults at dev and set prod explicitly in deployment.

## 3. Secrets
- Never commit `.env`; commit `.env.example` with every key.
- Production: inject from the platform's secret store (Kubernetes Secrets, AWS Secrets Manager/SSM, Doppler, Vault). File-mounted secrets: django-environ's `FileAwareEnv` reads a value from the file named by `<NAME>_FILE`.
- Rotate `SECRET_KEY` with `SECRET_KEY_FALLBACKS` (4.1+) so sessions/password reset tokens stay valid during rotation.
- Don't print settings or `env` in logs; Django's debug page hides settings whose names contain API, KEY, PASS, SECRET, SIGNATURE or TOKEN, but `DEBUG` must still be off in production.

## 4. Guard rails
```python
# prod.py
assert not DEBUG, "DEBUG must be False in production"
```
`manage.py check --deploy` in CI for prod settings. Access settings via `django.conf.settings`, never by importing the settings module directly.

## 5. Feature flags and per-tenant config
Keep them out of settings when they change at runtime - use a DB-backed flag library (django-waffle) or config service.

## Verify
- [ ] Starting without `SECRET_KEY`/`DATABASE_URL` fails immediately with a clear error.
- [ ] `git log -p | grep -i "secret_key ="` shows no real keys ever committed (rotate if so).
- [ ] Prod settings pass `check --deploy`.

## Checked
Date: 2026-10-25. Documentation: Django documentation source (django/django main branch, 6.2 in development, commit of 2026-10-23; release notes 4.0 to 6.0) (ref/settings, howto/deployment/checklist, release 4.1), django-environ docs source and `environ/environ.py` (joke2k/django-environ main, commit of 2026-06-18).
Confirmed: `Env(...)` with scheme defaults, `read_env` not overriding real environment variables unless `overwrite=True`, `env.db`/`env.cache`/`env.email` aliases and their URL schemes (`locmemcache://`, `consolemail://`), `FileAwareEnv`, `SECRET_KEY_FALLBACKS` (4.1), debug-page masking rule, `check --deploy`.
Corrected or removed: the hand-rolled `_FILE` pattern (replaced by `FileAwareEnv`) and the imprecise debug-masking sentence.
Method: documentation only; no commands were run.
