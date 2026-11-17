---
id: computing-software.web-development.django.logging-configuration
name: logging-configuration
category: computing-software
field: web-development
product: django
tags: [django-logging, logging-config, structured-logging, python-logging, django]
level: practitioner
status: verified
description: "Configuring Django LOGGING: dictConfig structure, django.request and db.backends loggers, JSON console output for containers, and keeping secrets out."
sources:
  - https://docs.djangoproject.com/en/stable/topics/logging/
  - https://docs.djangoproject.com/en/stable/ref/logging/
  - https://docs.python.org/3/library/logging.config.html#logging-config-dictschema
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Django LOGGING configuration

## 1. A production-ready baseline
```python
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,           # keep Django's and libraries' loggers
    "formatters": {
        "json": {"()": "pythonjsonlogger.json.JsonFormatter",
                 "format": "%(asctime)s %(levelname)s %(name)s %(message)s %(request_id)s"},
        "plain": {"format": "%(asctime)s %(levelname)s %(name)s: %(message)s"},
    },
    "filters": {"request_id": {"()": "core.logging.RequestIdFilter"}},
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "json" if not DEBUG else "plain", "filters": ["request_id"]},
    },
    "root": {"handlers": ["console"], "level": env("LOG_LEVEL", default="INFO")},
    "loggers": {
        "django.request": {"level": "WARNING"},      # 4xx at WARNING, 5xx at ERROR with traceback
        "django.security": {"level": "WARNING"},     # DisallowedHost, CSRF failures
        "django.db.backends": {"level": "WARNING"},  # DEBUG logs every SQL query (only with DEBUG=True)
        "myapp": {"level": "DEBUG" if DEBUG else "INFO"},
    },
}
```
- Containers/PaaS: log to stdout/stderr and let the platform ship logs; avoid file handlers with rotation inside containers.
- `disable_existing_loggers: True` silently drops logging from libraries configured before settings - almost never what you want (a logger created before `dictConfig` showed `disabled = True`).
- `pythonjsonlogger.json.JsonFormatter` is the import path of python-json-logger 3.1+ (4.2.0 tested); older releases used `pythonjsonlogger.jsonlogger.JsonFormatter`. `extra=` keys appear as JSON fields.

## 2. Using loggers
```python
logger = logging.getLogger(__name__)
logger.info("order paid", extra={"order_id": order.id, "amount": str(order.total)})
logger.exception("payment provider failed")   # inside except: includes traceback
```
- Use `%s` args or `extra`, not f-strings, so aggregation groups messages and formatting is lazy.
- Add a request id: middleware sets a contextvar from `X-Request-ID` (or generates one); a logging Filter injects it into records.

## 3. Useful Django loggers
`django.request` (5xx/4xx), `django.server` (runserver), `django.template` (missing variables at DEBUG), `django.db.backends` (SQL; only logged when `DEBUG = True`, measured: a query logged nothing with DEBUG off), `django.security.*` (per-check names like `django.security.csrf`), `django.channels.*` (Channels registers `django.channels.worker`, daphne `django.channels.server`), `celery`.

## 4. Sensitive data
Never log passwords, tokens, full card numbers or session ids. Use `sensitive_post_parameters`/`sensitive_variables` for error reports; scrub `Authorization` headers in custom request logging.

## 5. structlog
For richer structured logs, `django-structlog` adds request binding and JSON rendering on top of stdlib logging.

## Verify
- [ ] Production logs are JSON on stdout with level, logger and request id; 5xx tracebacks appear once; no SQL or secrets logged in production.

## Checked
Django 6.1.2, DRF 3.18.3 (Python 3.14, Windows, scratch venv, SQLite) with a scratch project that reproduces the skill's snippets. Packages: python-json-logger 4.2.0, sentry-sdk 2.72.0, django-structlog 10.1.0 (existence only).
- Run: the LOGGING dict (JSON formatter with a contextvar `RequestIdFilter`, console handler, root INFO, `django.request` WARNING): output lines were JSON with `levelname`, `name`, `request_id` and `extra` fields; DEBUG records from `myapp` were suppressed at INFO.
- Run: a 404 logged `Not Found: /nope/` at WARNING; an unhandled exception logged `Internal Server Error: /boom/` at ERROR with `exc_info`, once, and also emailed ADMINS through `mail_admins`.
- Run: `django.db.backends` set to DEBUG captured no SQL while `settings.DEBUG` was False (schema SQL goes to the separate `django.db.backends.schema` logger).
- Run: `disable_existing_loggers: True` disabled a pre-existing logger; `False` did not.
- Grep: Channels registers `django.channels.worker` and daphne `django.channels.server`; Fetched: ref/logging.txt (`django.request`, `django.server`, `django.template`, `django.db.backends`, `django.security.*` and `django.db.backends.schema`); `pip index` shows django-structlog exists.
