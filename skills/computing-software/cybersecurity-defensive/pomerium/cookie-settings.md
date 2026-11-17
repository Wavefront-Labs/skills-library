---
id: computing-software.cybersecurity-defensive.pomerium.cookie-settings
name: cookie-settings
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [cookie-secret, cookie-expire, cookie-http-only, cookie-same-site, cookie-domain]
level: practitioner
status: docs-checked
description: "Configure Pomerium session cookie settings (name, secret, domain, HttpOnly, expiry, SameSite) and understand the security trade-offs."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/reference/cookies.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Core setting names (environment variable is the uppercase form):
- `cookie_name`: default `_pomerium`.
- `cookie_secret` / `cookie_secret_file`: encrypts and signs the session cookie; generated if omitted. Generate with `head -c32 /dev/urandom | base64`. The file form suits secret managers, e.g. `/run/secrets/POMERIUM_COOKIE_SECRET`.
- `cookie_domain`: scope of the cookie; default is the setting host; an explicit domain also covers subdomains.
- `cookie_http_only`: default `true`, hides the cookie from JavaScript. Disabling it is strongly discouraged: it raises XSS exposure and lets any script (including third-party) read the cookie. If you must, audit all JavaScript, use a Content Security Policy, and limit cookie scope and lifetime.
- `cookie_expire`: Go duration, default `14h`. Pomerium enforces its own timeout because it cannot tell whether the user closed the browser; otherwise IdP tokens for abandoned sessions would be refreshed forever.
- `cookie_same_site`: unset by default, so browsers use `Lax`. `Strict` sends only on same-site requests; `None` sends cross-site and requires HTTPS.

Kubernetes uses `cookie.name`, `cookie.domain`, `cookie.httpOnly`, `cookie.expire`, `cookie.sameSite`; the secret comes from bootstrap secrets. In Enterprise, most are set in the Console or Terraform (the secret file is bootstrap only).

## Checked

2026-11-04. Read the Cookies Settings reference: setting names, defaults, secret generation command, secret file example, domain scope, HttpOnly warning, expiry rationale, SameSite options, Kubernetes names and Enterprise notes all confirmed. Removed an unsourced pointer about sharing cookies across subdomains.

Method: documentation only; no commands were run.
