---
id: computing-software.systems-network-administration.apache-guacamole.totp-mfa
name: totp-mfa
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, totp, mfa, multi-factor-authentication, totp-issuer, totp-digits, totp-period, totp-mode, enrollment, authenticator-app]
level: practitioner
status: docs-checked
description: "Enable TOTP two-factor login in Guacamole: issuer, digits, period and mode defaults, QR enrollment, resetting a lost device, per-user disable and the database requirement."
sources:
  - https://guacamole.apache.org/doc/gug/totp-auth.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TOTP multi-factor authentication

Install: copy `guacamole-auth-totp-1.6.0.jar` to `GUACAMOLE_HOME/extensions/`, restart Tomcat. Docker: `TOTP_ENABLED=true`.

Properties (default; Docker uppercase):
- `totp-issuer`: "Apache Guacamole"
- `totp-digits`: 6 (6, 7 or 8)
- `totp-period`: 30 s
- `totp-mode`: sha1 (sha1, sha256, sha512)
- `totp-bypass-hosts`, `totp-enforce-hosts`: IPs or CIDR; enforce wins

Defaults match Google Authenticator, which silently ignores non-default values; confirm your app supports changes.

Enrollment: after the first factor, Guacamole shows a QR code (or "Show" under Details for manual entry). The user enrolls by submitting a valid code. If they do not finish, the next login issues a new key and the old QR stops working.

Admin actions in the user's settings:
- **Clear TOTP secret**: new key, forces re-enrollment (lost phone).
- Uncheck **TOTP key confirmed**: shows the same QR again.
- **Disable TOTP** (from 1.6.0) on a user or a group; group membership exempts members. Before 1.6.0 it applied to everyone.

Requirements:
- Layered on another auth method; needs a storage-capable extension, currently only the database extensions, so set up the database first (apache-guacamole.database-auth-overview).
- Real client IPs needed for host rules.

Verify: log in with a fresh user, enroll, log out, and log in with a current code.

## Checked

2026-11-04. Confirmed against the Guacamole manual page totp-auth: the storage prerequisite (only the database extensions currently), jar name and location, TOTP_ENABLED, totp-issuer, digits, period and mode defaults and legal values, the Google Authenticator warning, bypass and enforce host lists with enforce taking priority, the reverse proxy IP warning, the QR and Show enrollment flow and incomplete-enrollment regeneration, Clear TOTP secret and TOTP key confirmed, the 1.6.0 Disable TOTP option for users and groups, and the Tomcat restart. No changes needed.

Method: documentation only; no commands were run.
