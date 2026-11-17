---
id: computing-software.data-science-and-analytics.apache-superset.securing-superset-sessions
name: securing-superset-sessions
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [securing-superset, session-server-side, cookies, disallowed-sql-functions, hardening]
level: advanced
status: docs-checked
description: "Harden Superset: SESSION_SERVER_SIDE, session lifetime, cookie flags, Talisman, DISALLOWED_SQL_FUNCTIONS, JWT secrets and secret rotation."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/security/securing_superset.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: apply the documented hardening settings (the guide applies to Superset 4.0 and later). Run behind a reverse proxy or load balancer that terminates HTTPS, enforce TLS 1.2 or higher, and use HSTS (in the proxy or in Talisman settings).

Secret key: `SECRET_KEY` (from env var `SUPERSET_SECRET_KEY`) signs session cookies and encrypts stored database credentials. Generate a unique, strong key per instance (the guide's example is `openssl rand -base64 42`), keep it in an environment variable or secrets manager rather than `superset_config.py` or version control, and never reuse it across environments or instances. Rotating it invalidates all user sessions and must follow the official rotation procedure in the Superset configuration docs.

Sessions:
- The default stateless cookie sessions make immediate invalidation on logout hard. For production the guide strongly recommends a server-side backend (Redis, Memcached or a database): `SESSION_SERVER_SIDE = True`, `SESSION_TYPE` (`'redis'`, `'memcached'`, `'filesystem'`, `'sqlalchemy'`) and, for Redis, `SESSION_REDIS`.
- `PERMANENT_SESSION_LIFETIME`: the default is 31 days, not recommended for production; the guide's example is `timedelta(hours=8)`.
- Cookie flags: `SESSION_COOKIE_SECURE = True` (HTTPS only), `SESSION_COOKIE_HTTPONLY = True` (not readable by scripts), `SESSION_COOKIE_SAMESITE = 'Lax'`. For iframe embedding use `'None'`, which requires `SESSION_COOKIE_SECURE = True` and disables some browser CSRF protection.

Headers: Talisman is disabled by default from Superset 4.0 (`TALISMAN_ENABLED = False`); enable it with a strict content security policy for `TALISMAN_CONFIG` to apply.

Database: Superset is not a database firewall. Use a dedicated limited-privilege database user (for example SELECT on needed schemas only). `DISALLOWED_SQL_FUNCTIONS` is a defence-in-depth measure, not a substitute for database permissions.

Secrets register (suggested rotation quarterly and after incidents): `SUPERSET_SECRET_KEY`, `GUEST_TOKEN_JWT_SECRET` (signs embedded guest tokens), `WEBSOCKET_JWT_SECRET` (signs the websocket JWT cookie). Rotating the guest-token or websocket secret invalidates outstanding tokens of that type. `PREVIOUS_JWT_SECRET` is documented only for the websocket secret: set the outgoing value on the websocket server so old cookies still verify, then remove it. SMTP and database passwords are also on the register.

Also recommended: enterprise IdP via OAuth or LDAP, least-privilege roles, delete or disable the default admin once another admin exists, `DEBUG` false, a WAF, centralised logs with alerts (failed logins, role changes, high-privilege user changes, disallowed SQL function attempts), updates to the latest major or minor version, and quarterly access reviews.

## Checked

Confirmed against the Superset docs page "Securing Your Superset Installation for Production": all settings, defaults and examples above. Corrected the claim that `PREVIOUS_JWT_SECRET` rotates any JWT secret (the page ties it to the websocket secret) and removed the unsourced advice to review roles after upgrades.

Method: docs-only read of cited pages, 2026-11-08
