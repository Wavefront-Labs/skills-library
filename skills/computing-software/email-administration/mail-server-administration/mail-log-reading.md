---
id: computing-software.email-administration.mail-server-administration.mail-log-reading
name: mail-log-reading
category: computing-software
field: email-administration
product: mail-server-administration
tags: [mail-log-reading, mail-logging, mail-log, maillog, postfix-log]
level: intro
status: draft
description: "Read Postfix log lines: connect, queue id, from, to, relay, delay, dsn and status fields."
sources:
  - https://www.postfix.org/documentation.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mail log reading

**Goal:** understand one delivery from its log lines.
## Fields
`to=<..>, relay=host[ip]:25, delay=1.2, delays=0.1/0/0.4/0.7, dsn=2.0.0, status=sent (250 2.0.0 Ok)`; `delays` = before queue / queue wait / connection setup / transmission.
## Steps
1. `grep <queue-id> /var/log/mail.log` (path varies; journald: `journalctl -u postfix`).
2. Components are tagged `postfix/smtpd`, `postfix/cleanup`, `postfix/qmgr`, `postfix/smtp`, `postfix/lmtp`.
3. Status values: sent, deferred, bounced.
## Failure modes
- Log rotation hides older events; keep enough history.
- Log lines contain addresses: treat as personal data.
## Verify
- You can follow one message from `postfix/smtpd client=` through `postfix/qmgr from=` to `status=sent`.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
