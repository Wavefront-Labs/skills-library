---
id: computing-software.email-administration.mail-server-administration.opendkim-setup
name: opendkim-setup
category: computing-software
field: email-administration
product: mail-server-administration
tags: [opendkim-setup, dkim, opendkim, dkim-signing, keytable, signingtable]
level: practitioner
status: draft
description: "Set up OpenDKIM as a Postfix milter that signs outbound mail and verifies inbound, with SigningTable and KeyTable."
sources:
  - https://www.rfc-editor.org/rfc/rfc6376
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Opendkim setup

**Goal:** sign outbound mail with d=example.com (RFC 6376).
## Steps
1. Generate: `opendkim-genkey -b 2048 -d example.com -s mail2026 -D /etc/opendkim/keys/example.com`.
2. KeyTable: `mail2026._domainkey.example.com example.com:mail2026:/etc/opendkim/keys/example.com/mail2026.private`.
3. SigningTable: `*@example.com mail2026._domainkey.example.com`.
4. Postfix: `smtpd_milters = inet:127.0.0.1:8891`, `non_smtpd_milters = $smtpd_milters`.
5. Publish the DNS record (see dkim-key-publishing), restart both services.
## Failure modes
- Private key readable by others, or wrong owner: the milter refuses to start.
- Signing only on port 25 flow: set `non_smtpd_milters` for locally injected mail.
## Verify
- Send to a test mailbox: header shows `dkim=pass header.d=example.com`.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
