---
id: computing-software.email-administration.mail-server-administration.trace-message-in-logs
name: trace-message-in-logs
category: computing-software
field: email-administration
product: mail-server-administration
tags: [trace-message-in-logs, pflogsumm, message-tracing, queue-id]
level: practitioner
status: draft
description: "Trace a message through Postfix, milters and Dovecot logs using Message-ID and queue ID, and use pflogsumm for summaries."
sources:
  - https://www.postfix.org/documentation.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Trace message in logs

**Goal:** answer a user asking where their message went.
## Steps
1. Find the queue id: `grep 'message-id=<abc@example.net>' /var/log/mail.log`.
2. Grep that queue id for the delivery attempts; note `status=` and relay.
3. For Dovecot delivery, the `dovecot: lmtp(...)` line contains `msgid=<...>` and the saved folder.
4. Daily overview: `pflogsumm -d yesterday /var/log/mail.log`.
## Failure modes
- Message accepted by Postfix but filtered into Junk by Sieve: the Dovecot log shows `fileinto`.
## Verify
- Trace ends in `saved mail to INBOX`, a bounce, or a clear remote reject.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
