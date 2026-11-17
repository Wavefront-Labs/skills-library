---
id: computing-software.email-administration.mail-server-administration.smtp-session-by-hand
name: smtp-session-by-hand
category: computing-software
field: email-administration
product: mail-server-administration
tags: [smtp-session-by-hand, smtp-protocol, smtp, telnet, openssl-s-client, ehlo]
level: practitioner
status: draft
description: "Drive an SMTP session manually with openssl s_client or nc to see greeting, EHLO, STARTTLS, MAIL FROM and DATA."
sources:
  - https://www.rfc-editor.org/rfc/rfc5321
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Smtp session by hand

**Goal:** reproduce delivery problems by speaking SMTP yourself (RFC 5321).
## Steps
1. `openssl s_client -starttls smtp -connect mail.example.com:25 -crlf` (use `nc` for plaintext).
2. Type `EHLO client.example.net`; read the advertised extensions (STARTTLS, SIZE, AUTH, 8BITMIME, SMTPUTF8, PIPELINING).
3. `MAIL FROM:<sender@example.net>`, `RCPT TO:<user@example.com>`, `DATA`, headers, blank line, body, a lone `.` line, then `QUIT`.
4. Note which command gets the first 4xx/5xx and its exact text.
## Failure modes
- Typing too slowly: server idle timeouts close the session.
- Outbound port 25 blocked by your provider, so the connection hangs.
- Testing against production with real recipient addresses: use a test mailbox.
## Verify
- You see `250 2.0.0 Ok: queued as <id>` and the id appears in the server log.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
