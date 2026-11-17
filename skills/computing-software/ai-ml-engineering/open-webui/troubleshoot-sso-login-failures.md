---
id: computing-software.ai-ml-engineering.open-webui.troubleshoot-sso-login-failures
name: troubleshoot-sso-login-failures
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [troubleshooting, sso-oidc, oauth, csrf, cookies, reverse-proxy, open-webui]
level: practitioner
status: docs-checked
description: "Diagnose Open WebUI OAuth and OIDC login loops, mismatching_state, redirect URI and persistent-config problems from logs, cookies and proxy settings."
sources:
  - https://docs.openwebui.com/troubleshooting/sso
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: find why SSO login fails, checking causes in order of likelihood.

## Checklist
1. **Env var names** (most common cause). Wrong -> right: `OIDC_CONFIG` -> `OPENID_PROVIDER_URL`; `WEBUI_OIDC_CLIENT_ID`/`OPENID_CLIENT_ID` -> `OAUTH_CLIENT_ID`; `OPENID_CLIENT_SECRET` -> `OAUTH_CLIENT_SECRET`. `WEBUI_ENABLE_SSO` and `WEBUI_AUTH_TYPE` do not exist (OAuth is on via `ENABLE_OAUTH`; `ENABLE_OAUTH_SIGNUP=true` only lets SSO create accounts). In Kubernetes YAML a name quoted with a trailing space (`'OAUTH_CLIENT_ID '`) silently breaks. Restart after changes.
2. **`OPENID_PROVIDER_URL`** is mandatory for generic OIDC (not required for the Microsoft provider). Entra: `https://login.microsoftonline.com/<TENANT>/v2.0/.well-known/openid-configuration`; Google: `https://accounts.google.com/.well-known/openid-configuration`.
3. **Redirect URI** must match exactly: `/oauth/oidc/callback`, `/oauth/microsoft/callback`, `/oauth/google/callback` (not `/oauth/callback/oidc`). Check the WebUI URL in Settings > Admin > General.
4. **Persistent config**: `ENABLE_PERSISTENT_CONFIG` (default true) plus `ENABLE_OAUTH_PERSISTENT_CONFIG` (default false). With the default, env wins and the Admin Panel OAuth section is read-only; DB-saved values load only if the latter is true.
5. **Extra authorize params**: `OAUTH_AUTHORIZE_PARAMS={"prompt":"consent","login_hint":"user@example.com"}` (Google: `GOOGLE_OAUTH_AUTHORIZE_PARAMS`).

## Proxy and cookies
- Exclude `/api`, `/oauth`, `/callback`, `/login`, `/ws`, `/websocket` from proxy caching (nginx: `proxy_no_cache 1; proxy_cache_bypass 1;`, plus WebSocket upgrade headers).
- Redirect loops or "No token found in localStorage": set `WEBUI_SESSION_COOKIE_SAME_SITE=lax`, `WEBUI_AUTH_COOKIE_SAME_SITE=lax`, `WEBUI_SESSION_COOKIE_SECURE=true`, `WEBUI_AUTH_COOKIE_SECURE=true` (false on plain HTTP). Avoid `proxy_cookie_path / "/; Secure; HttpOnly; SameSite=None"`; prefer `proxy_cookie_flags ~ secure samesite=lax;`.

## Timeouts, CSRF, clusters
- `httpcore.ReadTimeout` or `CSRF Warning! State not equal in request and response` / `mismatching_state`: raise `OAUTH_TIMEOUT=60` (AIOHTTP_CLIENT_TIMEOUT does not affect the httpx-based OAuth client); make sure `WEBUI_URL` matches exactly and `WEBUI_SECRET_KEY` / `OAUTH_SESSION_TOKEN_ENCRYPTION_KEY` are set.
- Multi-instance: `REDIS_URL`, `WEBSOCKET_REDIS_URL`, same secrets everywhere, `ENABLE_WEBSOCKET_SUPPORT=true`, `WEBSOCKET_MANAGER=redis`.

## Log signatures
- `Sign-in with your identity provider failed...`: generic callback failure; read backend log (denied access, no email, domain not allowed).
- `Unsupported {'app_id'} in header`: update Open WebUI.
- `1 validation error for UserModel ... oauth`: upgraded from before v0.6.41; update, a repair migration fixes it at startup. `OAUTH_MERGE_ACCOUNTS_BY_EMAIL` does not help.
- 404 on callback: redirect URI mistake.
Set `GLOBAL_LOG_LEVEL=DEBUG` and trace GET `/oauth/{provider}/login` (302) then `/oauth/{provider}/callback?code=...`. Look for cookie `oauth_session_id` (new) vs `oauth_id_token` (legacy). Test with the proxy bypassed to isolate it.

## Security note
Without Redis, sign-out does not revoke JWTs (default 4 weeks). Use Sign out all devices, Redis, or shorter `JWT_EXPIRES_IN`.

## Checked
2026-11-07. Confirmed against the Open WebUI docs: troubleshooting/sso (read in full). Narrowed the OPENID_PROVIDER_URL note to what the page says: not required for Microsoft.
Method: documentation only; no commands were run.
