---
id: computing-software.systems-network-administration.netbox.security-settings-sessions-hsts
name: security-settings-sessions-hsts
category: computing-software
field: systems-network-administration
product: netbox
tags: [login-timeout, hsts, csrf-trusted-origins]
level: advanced
status: docs-checked
description: "Tune login, session, HSTS, CSRF, CORS and password validator settings."
sources: ["https://netboxlabs.com/docs/netbox/configuration/security/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Security settings

Goal: set the login, transport and password parameters.

**Sessions and login**

- `LOGIN_TIMEOUT`: seconds of the auth cookie; default `None` uses Django's two weeks (1,209,600).
- `LOGIN_PERSISTENCE` (default False): reset the session lifetime on every valid request; this writes the session each request, which may add overhead.
- `LOGIN_REQUIRED` is a legacy parameter, deprecated and to be removed in v5.0 (default True).
- `LOGIN_FORM_HIDDEN`: hide the login form when only SSO is used. If the SSO provider is unreachable, the only recourse is to disable it in the configuration and restart.
- `LOGOUT_REDIRECT_URL` default `'home'`.

**HTTPS**: `SECURE_SSL_REDIRECT` (False), `SECURE_HSTS_SECONDS` (0), `SECURE_HSTS_INCLUDE_SUBDOMAINS`, `SECURE_HSTS_PRELOAD`, `CSRF_COOKIE_SECURE` (False). Make sure the frontend forwards the HTTP scheme correctly before enabling the redirect or you may create a loop.

**CSRF and CORS**: `CSRF_TRUSTED_ORIGINS` entries must include the scheme (`https://netbox.local`). `CORS_ORIGIN_ALLOW_ALL` defaults False; otherwise use `CORS_ORIGIN_WHITELIST` or `CORS_ORIGIN_REGEX_WHITELIST`.

**Passwords**: `AUTH_PASSWORD_VALIDATORS` defaults to at least 12 characters plus one uppercase, one lowercase and one digit. `[]` disables it, which is not recommended.

**Checklist**

1. HTTPS settings after proxy test.
2. Schemes in CSRF origins.
3. Timeout chosen deliberately.

## Checked

2026-11-03: confirmed against the cited NetBox documentation: Security configuration page: LOGIN_TIMEOUT default None, LOGIN_PERSISTENCE and its per-request session write overhead, LOGIN_REQUIRED legacy/deprecated for v5.0 with default True, the HSTS/CSRF/CORS parameter names and defaults, AUTH_PASSWORD_VALIDATORS. Removed: The claim that LOGIN_REQUIRED is already removed (page says it will be removed in v5.0).

Method: documentation only; no commands were run.
