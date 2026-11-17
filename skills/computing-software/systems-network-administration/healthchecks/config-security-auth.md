---
id: computing-software.systems-network-administration.healthchecks.config-security-auth
name: config-security-auth
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, webauthn-rp-id, remote-user-header, registration-open, private-ip-integrations]
level: sme
status: docs-checked
description: "Self-hosted Healthchecks access and security settings: WebAuthn RP_ID, REMOTE_USER_HEADER proxy auth, REGISTRATION_OPEN, private IP integrations and SECRET_KEY handling."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/self_hosted_configuration.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
- `RP_ID` (default None): WebAuthn Relying Party identifier. Setting it enables WebAuthn two-factor authentication.
- `REMOTE_USER_HEADER` (default None): request header used for external authentication via a reverse proxy or the WSGI server. Users are logged in and accounts are created automatically, and the built-in login methods are disabled. The proxy must strip spoofed copies of the header.
- `REGISTRATION_OPEN` (default True): controls whether visitors can create new accounts.
- `INTEGRATIONS_ALLOW_PRIVATE_IPS` (default False): allows integrations to request private IP addresses; a security risk if enabled.
- `SECRET_KEY`: unique and unpredictable, or provide `SECRET_KEY_FILE`.
- `SECURE_PROXY_SSL_HEADER`: header name and value that mark a request as HTTPS behind a proxy.
- `DEBUG`: keep False in production, with `ALLOWED_HOSTS` set.
- `SHELL_ENABLED`: keep False unless users are fully trusted.

Also remember: the proxy must set `X-Forwarded-For` or login rate limiting can be bypassed (see docker-reverse-proxy). Secrets via `_FILE` variables avoid putting values in the environment.

## Checked

2026-11-04. Confirmed against the Healthchecks server configuration page and README: RP_ID and WebAuthn, REMOTE_USER_HEADER behaviour and the header-stripping warning, REGISTRATION_OPEN, INTEGRATIONS_ALLOW_PRIVATE_IPS, SECRET_KEY and SECRET_KEY_FILE, SECURE_PROXY_SSL_HEADER, DEBUG and ALLOWED_HOSTS production advice, SHELL_ENABLED, and the X-Forwarded-For warning about login rate limiting.

Method: documentation only; no commands were run.
