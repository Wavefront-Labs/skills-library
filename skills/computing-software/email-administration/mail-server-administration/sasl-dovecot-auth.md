---
id: computing-software.email-administration.mail-server-administration.sasl-dovecot-auth
name: sasl-dovecot-auth
category: computing-software
field: email-administration
product: mail-server-administration
tags: [sasl-dovecot-auth, postfix-sasl, smtpd-sasl-type, dovecot-sasl, smtpd-sasl-path]
level: practitioner
status: docs-checked
description: "Use Dovecot as the SASL authentication backend for Postfix submission via a private auth socket."
sources:
  - https://doc.dovecot.org/main/howto/sasl/postfix.html
  - https://www.postfix.org/postconf.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sasl dovecot auth

**Goal:** one user database for IMAP and SMTP.
## Steps
1. Postfix: `smtpd_sasl_type = dovecot`, `smtpd_sasl_path = private/auth`, `smtpd_sasl_auth_enable = yes`.
2. Dovecot `10-master.conf`:
```
service auth {
  unix_listener /var/spool/postfix/private/auth {
    mode = 0660
    user = postfix
    group = postfix
  }
}
```
3. Dovecot `auth_mechanisms = plain login` (Outlook and Windows Mail work only with LOGIN, per the Dovecot page); require TLS on the submission service.
## Failure modes
- Wrong socket owner or path: Postfix cannot reach the auth socket (`smtpd_sasl_path` is relative to `$queue_directory`).
- chroot'd smtpd needs the socket inside the Postfix queue directory.
## Verify
- An authenticated session over TLS (for example `AUTH PLAIN <base64>`) is accepted and can relay via `permit_sasl_authenticated`.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.

## Checked
Date: 2026-11-02. Documentation: Dovecot docs 'Postfix and Dovecot SASL' (howto/sasl/postfix, source repo), postconf(5) smtpd_sasl_type/smtpd_sasl_path.
Confirmed: `smtpd_sasl_type = dovecot`, `smtpd_sasl_path = private/auth` (relative to the queue directory), `smtpd_sasl_auth_enable = yes`, the `service auth` unix_listener at /var/spool/postfix/private/auth with mode 0660 user/group postfix, `auth_mechanisms = plain login`, `permit_sasl_authenticated`.
Corrected or removed: 'only offered over TLS' (not the documented reason for the setting), the warning and 235 reply text.
Method: documentation only; no commands were run.
