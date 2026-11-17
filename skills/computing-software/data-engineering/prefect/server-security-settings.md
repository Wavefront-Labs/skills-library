---
id: computing-software.data-engineering.prefect.server-security-settings
name: server-security-settings
category: computing-software
field: data-engineering
product: prefect
tags: [auth-string, csrf, cors, reverse-proxy, custom-headers]
level: advanced
status: docs-checked
description: "Secure a self-hosted Prefect server: basic auth strings, reverse proxy UI URL, CSRF and CORS settings, and custom client headers."
sources:
  - https://docs.prefect.io/v3/advanced/security-settings
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: lock down a self-hosted server and its clients.

Basic authentication: `server.api.auth_string` (format `admin:pass`) on the server process; `api.auth_string` with the same value on every client. The UI prompts for the full string on first load.

```bash
PREFECT_SERVER_API_AUTH_STRING="admin:pass"
PREFECT_API_AUTH_STRING="admin:pass"
```

`PREFECT_API_KEY` is for Prefect Cloud only and takes precedence over `PREFECT_API_AUTH_STRING`; unset it on self-hosted setups to avoid `HTTP 401 Unauthorized`.

Reverse proxy: set `server.ui.api_url` to the external URL (falls back to `api.url`):

```toml
[server.ui]
api_url = "https://prefect-server.example.com/api"
```

CSRF: `server.api.csrf_protection_enabled` (default `False`, recommended in production), `server.api.csrf_token_expiration` (default 1 hour), `client.csrf_support_enabled` (default `True`; disable only if the server has CSRF off).

CORS: `server.api.cors_allowed_origins`, `server.api.cors_allowed_methods`, `server.api.cors_allowed_headers`.

Custom headers: `client.custom_headers` is a JSON object sent with every API request.

```bash
export PREFECT_CLIENT_CUSTOM_HEADERS='{"X-Corporate-ID": "your-corp-identifier"}'
```

Protected headers `User-Agent`, `Prefect-Csrf-Token` and `Prefect-Csrf-Client` cannot be overridden; attempts are ignored with a logged warning.

## Checked
2026-11-08. Confirmed against the security settings page: server.api.auth_string and api.auth_string, PREFECT_API_KEY precedence and 401 warning, server.ui.api_url with api.url fallback, CSRF settings and defaults, CORS settings, client.custom_headers and the three protected headers. Nothing removed.
Method: documentation only; no commands were run.
