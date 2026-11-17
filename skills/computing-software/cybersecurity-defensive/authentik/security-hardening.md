---
id: computing-software.cybersecurity-defensive.authentik.security-hardening
name: security-hardening
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, hardening, mfa, session-binding, reputation, csp]
level: advanced
status: docs-checked
description: "Harden authentik: password and MFA settings, enumeration protection, reputation, session lifetime, impersonation, blocked endpoints, CIDRs, CSP."
sources:
  - https://docs.goauthentik.io/security/security-hardening/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: tighten a default install according to your threat model; each change costs convenience.

## Authentication
- Shipped password policy: 8 characters plus zxcvbn (fails score 2 or below), bound only to the default password change flow. Bind it to enrollment too; for NIST raise length to 15 and enable **Check haveibeenpwned.com** (needs outbound access, so air-gapped needs an Expression policy).
- Authenticator Validation stage: **Not configured action** defaults to Continue (password-only login). Set it to force configuration or deny. Limit **Device Classes**, set **WebAuthn User verification** to Required (default Preferred), keep throttling factors at 1 (0 disables back-off). Device type restrictions skip devices enrolled before 2024.4 or with an unknown AAGUID.
- Identification stage: keep **Pretend user exists** on, turn **Show matched user** off, limit **User Fields**. Unlinking enrollment, recovery or passwordless flows only hides them (still at `/if/flow/<slug>/`); bind a policy or delete them.
- Reputation policy: each failed login is -1, success +1; it passes at or below the threshold. Bind to a CAPTCHA stage, or to the flow with **Negate**; without Negate it locks out everyone but the attacker. Limits are in **System > Settings**.
- Notification rules on `login_failed` and `suspicious_request`.

## Sessions
User Login stage: **Session duration** `seconds=0` (ends at browser close), **Remember device** `days=30`, **Remember me offset** `seconds=0`, **Terminate other sessions** off by default. **Network binding** (ASN/network/IP) and **GeoIP binding** (continent/country/city) default to none; stricter binding causes spurious logouts. Each needs its database (`AUTHENTIK_EVENTS__CONTEXT_PROCESSORS__ASN` or `...__GEOIP`); a missing database terminates the session on the first IP change.

## Admin and deployment
- Prefer roles and permissions over superuser membership. Under **System > Settings** disable **Impersonation** if unused and keep **Require reason for impersonation**. Event retention defaults to `days=365`.
- Block endpoints at the reverse proxy to freeze expressions (`/api/v3/policies/expression*`, `/api/v3/propertymappings*`, `/api/v3/stages/prompt/prompts*`, `/api/v3/managed/blueprints*`) or CAPTCHA stages (`/api/v3/stages/captcha*`); objects are then editable only through file blueprints.
- Keep `AUTHENTIK_SECRET_KEY` out of version control; rotating it invalidates all sessions. Narrow `AUTHENTIK_LISTEN__TRUSTED_PROXY_CIDRS`; set `AUTHENTIK_POSTGRESQL__SSLMODE` to `verify-ca` or `verify-full` (default `disable`); set `AUTHENTIK_OUTPOSTS__DISABLE_EMBEDDED_OUTPOST` to `true` if unused; keep log level `info` (`trace` can log cookies).
- CSP is not set by authentik; add at the proxy only where none exists: `default-src 'self'; img-src https: data:; object-src 'none'; frame-ancestors 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline';`.

## Checked

2026-11-08: read in full against the documentation source(s) listed in sources; the claims, names, values and examples in this skill match the page text.

Method: documentation only; no commands were run.
