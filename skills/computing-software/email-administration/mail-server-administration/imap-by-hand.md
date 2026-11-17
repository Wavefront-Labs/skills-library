---
id: computing-software.email-administration.mail-server-administration.imap-by-hand
name: imap-by-hand
category: computing-software
field: email-administration
product: mail-server-administration
tags: [imap-by-hand, dovecot-imap, imap, imap-capability, imap-test]
level: practitioner
status: docs-checked
description: "Test IMAP by hand with openssl s_client: LOGIN, LIST, SELECT, FETCH, LOGOUT, and read capability output."
sources:
  - https://www.rfc-editor.org/rfc/rfc3501
  - https://doc.dovecot.org/2.3/admin_manual/test_installation/
  - https://docs.openssl.org/3.0/man1/openssl-s_client/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Imap by hand

**Goal:** reproduce client-side IMAP problems (RFC 3501).
## Steps
1. `openssl s_client -connect mail.example.com:993 -crlf -quiet`.
2. `a1 CAPABILITY`, `a2 LOGIN alice@example.com password`, `a3 LIST "" "*"`, `a4 SELECT INBOX`, `a5 FETCH 1 (FLAGS)`, `a6 LOGOUT`. Each command needs a tag.
3. Read the `[CAPABILITY ...]` response: it shows `STARTTLS` and `AUTH=PLAIN` on a cleartext port, and `LOGINDISABLED` while plaintext logins are blocked.
## Failure modes
- Typing the password into shell history: use a test account.
- Using `LOGIN` over port 143 without TLS is blocked by `disable_plaintext_auth`.
## Verify
- You get `a2 OK Logged in` and `a4 OK [READ-WRITE] Select completed`.

## Notes
- Change one thing at a time in staging and keep a copy of the previous config.

## Checked

2026-11-03. Confirmed in the Dovecot 2.3 Test Installation page (openssl s_client on ports 993 and 143 with `-starttls imap`, `OK Logged in`, `OK [READ-WRITE] Select completed`, CAPABILITY example), the openssl s_client manual (`-crlf`, `-quiet`), the settings reference (LOGINDISABLED) and RFC 3501 (tagged commands, LOGOUT). Removed the IDLE, UIDPLUS and QUOTA capability names (not in the pages read) and the RFC 9051 source.

Method: documentation only; no commands were run.
