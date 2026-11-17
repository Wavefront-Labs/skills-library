---
id: computing-software.systems-network-administration.paperless-ngx.remote-user-sso
name: remote-user-sso
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, remote-user, sso, http-remote-user, paperless-enable-http-remote-user, logout-redirect]
level: advanced
status: docs-checked
description: "Authenticate Paperless-ngx users through a trusted proxy header with the HTTP remote user settings, and the risks if headers can be forged."
sources:
  - "https://docs.paperless-ngx.com/configuration/"
  - "https://docs.paperless-ngx.com/advanced_usage/"
  - "https://docs.paperless-ngx.com/api/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Remote user (header) authentication

Some SSO applications provide remote user authentication, which Paperless can use.

## Settings
- `PAPERLESS_ENABLE_HTTP_REMOTE_USER=true` allows authentication via `HTTP_REMOTE_USER`. Default false.
- `PAPERLESS_ENABLE_HTTP_REMOTE_USER_API=true` allows it directly against the REST API. It is separate from the setting above to avoid introducing a security vulnerability to existing reverse proxy setups. Default false.
- `PAPERLESS_HTTP_REMOTE_USER_HEADER_NAME`: customises the header the username is read from when either setting above is enabled. Default `HTTP_REMOTE_USER`. Values are in terms of Django's `HttpRequest.META`, so the value must start with `HTTP` followed by the normalised header name.
- `PAPERLESS_LOGOUT_REDIRECT_URL`: URL to send users to after logout; with remote user auth and SSO it can redirect back to the SSO application's logout page to complete logout. Default none.

## The danger
Authentication then works by simply adding a `Remote-User: <username>` header to a request. You must ensure that any such header is not passed from external requests through your reverse proxy to Paperless, or all authentication is bypassed. If Paperless is exposed to the internet directly (no reverse proxy), do not use this.

## Making SSO the only door
Once external auth is set up:
- `PAPERLESS_DISABLE_REGULAR_LOGIN` disables the regular frontend username and password login. It does not disable the Django admin login or logging in with local credentials via the API; consider blocking `/admin/` in your web server or reverse proxy.
- `PAPERLESS_REDIRECT_LOGIN_TO_SSO` automatically redirects users (using JavaScript) to the first SSO provider login.

## Checked
Date: 2026-11-07
Pages read in full: configuration, advanced_usage, api (docs/*.md; the API page's authentication section confirms the Remote User option against the API).
Removed as unconfirmed: "set only after real authentication", "for the web UI", and the advice to keep a superuser reachable another way (replaced by the documented fact that the admin and API local logins stay available).
Method: documentation only; no commands were run.
