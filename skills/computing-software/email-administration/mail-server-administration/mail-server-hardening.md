---
id: computing-software.email-administration.mail-server-administration.mail-server-hardening
name: mail-server-hardening
category: computing-software
field: email-administration
product: mail-server-administration
tags: [mail-server-hardening, mail-hardening, hardening, disable-vrfy, smtpd-banner]
level: advanced
status: draft
description: "Harden a mail server: minimal exposed ports, VRFY off, banner hygiene, TLS only, patched packages and least-privilege services."
sources:
  - https://www.postfix.org/documentation.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mail server hardening

**Goal:** reduce attack surface.
## Steps
1. `disable_vrfy_command = yes`; `smtpd_banner = $myhostname ESMTP`.
2. Firewall: expose 25, 587/465, 993 (and 143 if needed); keep management ports private.
3. Run daemons as their dedicated users; Dovecot `first_valid_uid` set.
4. Keep Postfix and Dovecot patched; subscribe to project security announcements.
5. Limit message size and recipient counts.
## Failure modes
- Exposing the Rspamd controller or ManageSieve to the internet.
## Verify
- Port scan from outside shows only intended ports; `VRFY` returns 502.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
