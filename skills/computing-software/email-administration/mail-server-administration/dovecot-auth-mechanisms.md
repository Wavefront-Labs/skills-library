---
id: computing-software.email-administration.mail-server-administration.dovecot-auth-mechanisms
name: dovecot-auth-mechanisms
category: computing-software
field: email-administration
product: mail-server-administration
tags: [dovecot-auth-mechanisms, auth-mechanisms, disable-plaintext-auth, ssl-required]
level: practitioner
status: docs-checked
description: "Set auth_mechanisms and ssl requirements in Dovecot so PLAIN and LOGIN are accepted only over TLS."
sources:
  - https://doc.dovecot.org/2.3/settings/core/
  - https://doc.dovecot.org/2.3/admin_manual/test_installation/
  - https://doc.dovecot.org/main/installation/upgrade/2.3-to-2.4/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dovecot auth mechanisms

**Goal:** safe credentials on the wire.
## Steps
1. `auth_mechanisms = plain login`
2. `ssl = required` (accepts yes, no, required; required covers imap, pop3, managesieve and submission and also blocks non-plaintext mechanisms without TLS) and `disable_plaintext_auth = yes` (the 2.3 default, which advertises LOGINDISABLED without TLS). Dovecot 2.4 replaces `disable_plaintext_auth` with `auth_allow_cleartext` and `ssl_cert`/`ssl_key` with `ssl_server_cert_file`/`ssl_server_key_file`.
3. Provide certs: `ssl_cert = </etc/ssl/mail/fullchain.pem`, `ssl_key = </etc/ssl/mail/privkey.pem`.
4. Apply changes with `doveadm reload`.
## Failure modes
- Clients that only do plaintext without TLS will fail; update them, do not weaken the server.
- Config syntax differs between 2.3 and 2.4; use `doveconf -n` to compare.
## Verify
- `openssl s_client -connect mail.example.com:993` then `a login ...` works; port 143 without STARTTLS refuses login.

## Notes
- Change one thing at a time in staging and keep a copy of the previous config.

## Checked

2026-11-03. Confirmed in the Dovecot 2.3 settings reference (auth_mechanisms default plain, disable_plaintext_auth default yes and LOGINDISABLED, ssl values), the 2.3 test-installation page (openssl s_client on port 993) and the 2.3 to 2.4 converted-settings table (auth_allow_cleartext, ssl_server_cert_file, ssl_server_key_file). Removed the claim that a reload is needed after each certificate renewal.

Method: documentation only; no commands were run.
