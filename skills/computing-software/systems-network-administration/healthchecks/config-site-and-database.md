---
id: computing-software.systems-network-administration.healthchecks.config-site-and-database
name: config-site-and-database
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, site-root, secret-key, db-settings, ping-body-limit-setting]
level: practitioner
status: docs-checked
description: "Self-hosted Healthchecks core settings: SITE_ROOT, SITE_NAME, SECRET_KEY, DEBUG, ALLOWED_HOSTS, ping endpoint and body limit, and the DB engine variables."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/self_hosted_configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Site:
- `SITE_ROOT` (default `http://localhost:8000`): base URL, used for absolute URLs and to derive other settings.
- `SITE_NAME` (default `Mychecks`), `SITE_LOGO_URL`, `MASTER_BADGE_LABEL` (overall status badge label).
- `ALLOWED_HOSTS` (default: domain from `SITE_ROOT`).
- `DEBUG` (default True): never in production. `ADMINS`: emails notified of errors when `DEBUG=False`.
- `SECRET_KEY` (placeholder default `---`): must be a unique unpredictable value; `SECRET_KEY_FILE` also supported.
- `REGISTRATION_OPEN` (default True): whether visitors can create accounts.
- `PING_ENDPOINT` (default `SITE_ROOT` + `/ping/`): base for displayed ping URLs.
- `PING_BODY_LIMIT` (default 10000): max bytes of ping bodies logged; `None` removes the limit.
- `USE_PAYMENTS` (default False): billing features.
- `http_proxy` / `https_proxy`: proxy for outgoing requests.

Database:
- `DB` (default `sqlite`): `sqlite`, `postgres` or `mysql`.
- `DB_HOST`, `DB_PORT`, `DB_NAME` (default `hc` or the SQLite path), `DB_USER`, `DB_PASSWORD` (or `DB_PASSWORD_FILE`).
- `DB_CONN_MAX_AGE` (default 0), `DB_SSLMODE` (default `prefer`), `DB_TARGET_SESSION_ATTRS` (default `read-write`).

## Checked

2026-11-04. Confirmed against the Healthchecks server configuration page: defaults for SITE_ROOT, SITE_NAME, ALLOWED_HOSTS, DEBUG, SECRET_KEY, REGISTRATION_OPEN, PING_ENDPOINT, PING_BODY_LIMIT, USE_PAYMENTS, DB, DB_NAME, DB_CONN_MAX_AGE, DB_SSLMODE and DB_TARGET_SESSION_ATTRS, plus ADMINS and the proxy variables. Nothing removed.

Method: documentation only; no commands were run.
