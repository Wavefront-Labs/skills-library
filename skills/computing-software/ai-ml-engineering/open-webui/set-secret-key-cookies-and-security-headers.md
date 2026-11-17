---
id: computing-software.ai-ml-engineering.open-webui.set-secret-key-cookies-and-security-headers
name: set-secret-key-cookies-and-security-headers
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [env-configuration, security, webui-secret-key, cookies, cors, mfa, security-headers]
level: advanced
status: docs-checked
description: "Set a persistent WEBUI_SECRET_KEY, cookie flags, CORS origins, MFA, password rules and HTTP security headers for an Open WebUI deployment."
sources:
  - https://docs.openwebui.com/reference/env-configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: configure the security-related environment variables correctly, avoiding the lock-outs the docs warn about.

## Secret key
`WEBUI_SECRET_KEY` signs JWTs and encrypts data at rest (OAuth tokens for MCP, app API keys). Docker (`start.sh`), `open-webui serve` and the Windows script auto-generate one into `.webui_secret_key` (override the file with `WEBUI_SECRET_KEY_FILE`; `open-webui serve` ignores that and uses the working directory). Development launches (`open-webui dev`, direct `uvicorn`) do not. If the container is recreated without that file persisted, a new key is generated: sessions and OAuth sessions break, MCP tools fail with `Error decrypting tokens`, installed apps stop connecting, and startup is refused while MFA is on. So set it explicitly: `openssl rand -hex 32`. Multi-replica deployments must use the same value everywhere. `WEBUI_SECRET_KEY_LENGTH` (default 24) is bytes on Docker and `serve` but characters on Windows; avoid values giving a 44-character key.
- `ENABLE_VALVE_ENCRYPTION=true` encrypts plugin Valve values with a key derived from the secret key; rotating it forces re-entering valves.
- MFA: `ENABLE_MFA` requires an authenticator code for all users and needs `WEBUI_AUTH` and `ENABLE_PERSISTENT_CONFIG` on. Set `MFA_ENCRYPTION_KEY` (Fernet: `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`) before users enroll, so the secret key can rotate. Changing `ENABLE_MFA`, `MFA_ALLOW_OAUTH_BYPASS` or `MFA_ALLOW_TRUSTED_HEADER_BYPASS` signs everyone out.

## Cookies
`WEBUI_SESSION_COOKIE_SAME_SITE` (`lax` default, `strict`, `none` needs HTTPS) and `WEBUI_SESSION_COOKIE_SECURE`; `WEBUI_AUTH_COOKIE_SAME_SITE` and `WEBUI_AUTH_COOKIE_SECURE` fall back to the session values when unset. Do not use `strict` with `ENABLE_OAUTH_SIGNUP`: the OAuth callback loses the cookie (also `OAuth callback state is invalid or expired` for MCP OAuth 2.1). `WEBUI_AUTH=False` works only on a fresh install with no users. `WEBUI_AUTH_SIGNOUT_REDIRECT_URL` sets the post-logout redirect.

## CORS
`CORS_ALLOW_ORIGIN` (default `*`) is a semicolon-separated list, for example `https://yourdomain.com;http://yourdomain.com;http://localhost:3000`. Log line `... is not an accepted origin` means an origin is missing. `CORS_ALLOW_CUSTOM_SCHEME` takes extra schemes without `://`, such as `app;electron`.

## Password rules
`ENABLE_PASSWORD_VALIDATION=true` applies `PASSWORD_VALIDATION_REGEX_PATTERN` (default needs 8+ chars with upper, lower, digit and special) to signup, changes, admin creation and resets; existing passwords are not forced to change. Always set `PASSWORD_VALIDATION_HINT` with a custom pattern, and test it: an invalid regex blocks registration.

## Security headers
Each is unset (header not sent) by default; a value outside the accepted format is replaced by a fallback, so the header is still sent. Fallbacks: `HSTS` (`max-age=31536000;includeSubDomains`), `XFRAME_OPTIONS` (`DENY`), `REFERRER_POLICY` (`no-referrer`), `XCONTENT_TYPE` (`nosniff`), `CROSS_ORIGIN_OPENER_POLICY` (`same-origin`), `CROSS_ORIGIN_EMBEDDER_POLICY` (`require-corp`), `CROSS_ORIGIN_RESOURCE_POLICY` (`same-origin`), plus `PERMISSIONS_POLICY`, `XDOWNLOAD_OPTIONS`, `XPERMITTED_CROSS_DOMAIN_POLICIES`, `CONTENT_SECURITY_POLICY`, `CONTENT_SECURITY_POLICY_REPORT_ONLY`, `REPORTING_ENDPOINTS` (last three unvalidated). Read once at startup.

## Checked
2026-11-07. Confirmed against the Open WebUI docs: reference/env-configuration (security header and cookie variables). Removed: an invented Verify section; clarified that an invalid header value is replaced by a fallback so the header is still sent.
Method: documentation only; no commands were run.
