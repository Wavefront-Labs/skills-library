---
id: computing-software.collaboration-platform-administration.bookstack.bookstack-security-hardening
name: bookstack-security-hardening
category: computing-software
field: collaboration-platform-administration
product: bookstack
tags: [bookstack, security, app-key, content-filtering, csp, iframe, trusted-proxies, mfa, session-secure-cookie, uploads]
level: advanced
status: docs-checked
description: "Harden BookStack: initial checklist, MFA, image storage exposure, APP_CONTENT_FILTERING flags, iframe and CSP variables, APP_PROXIES, failed-login logging and APP_KEY handling."
sources: ["https://www.bookstackapp.com/docs/admin/security/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# BookStack security settings

Initial setup: change the default admin account, expose only the `public` folder, give the database user rights only on BookStack's database, set `APP_URL` so generated URLs cannot be manipulated, and review registration, public access and roles.

- MFA: users can enable TOTP apps and 16 single-use backup codes (stored encrypted); roles can enforce it via "Requires Multi-Factor Authentication".
- Uploads: images are public by default; the "higher security image uploads" setting adds a random 16-character string to filenames; disable directory indexes for `/uploads` (nginx `autoindex off`, Apache `Options -Indexes`). Attachments sit in `storage/uploads` behind app authentication.
- `APP_CONTENT_FILTERING` flags: `j` JavaScript, `h` dangerous HTML, `f` form elements, `a` allowlist. Unset is strictest; an empty value is dangerous. `ALLOW_CONTENT_SCRIPTS` is deprecated.
- Embedding: `ALLOWED_IFRAME_HOSTS` (frame-ancestors; setting it makes cookies `SameSite=None`), `ALLOWED_IFRAME_SOURCES` (frame-src; default draw.io, YouTube, Vimeo; `*` is risky). Also `ALLOWED_STYLE_SOURCES`, `ALLOWED_IMAGE_SOURCES`.
- `SESSION_SECURE_COOKIE=true`, implied by an HTTPS `APP_URL`.
- `APP_PROXIES`: comma-separated trusted proxy IPs or `*`, so `X-Forwarded-For` feeds the audit log and rate limiting.
- `LOG_FAILED_LOGIN_MESSAGE` (with `%u` for the username) feeds Fail2Ban; social and SAML2 logins are not logged.
- `ALLOW_UNTRUSTED_SERVER_FETCHING` enables server fetches from user content (only in trusted environments); `ALLOWED_SSR_HOSTS` restricts webhooks and similar.
- `MYSQL_ATTR_SSL_CA` encrypts and verifies the database connection.
- `APP_KEY` encrypts MFA, cookies and sessions: generate with `php artisan key:generate --show`, keep secret, retain on restore.

## Checked

2026-11-03. Confirmed against the BookStack docs page(s) admin/security/ (under https://www.bookstackapp.com/docs/), including the prose, not only identifiers.
Removed or reworded: nothing.
Method: documentation only; no commands were run.
