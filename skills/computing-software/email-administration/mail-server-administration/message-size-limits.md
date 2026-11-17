---
id: computing-software.email-administration.mail-server-administration.message-size-limits
name: message-size-limits
category: computing-software
field: email-administration
product: mail-server-administration
tags: [message-size-limits, message-limits, message-size-limit, mailbox-size-limit]
level: intro
status: docs-checked
description: "Set message_size_limit, mailbox_size_limit and virtual_mailbox_limit consistently with the filters behind Postfix."
sources:
  - https://www.postfix.org/postconf.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Message size limits

**Goal:** one coherent maximum.
## Steps
1. `postconf -e 'message_size_limit = 26214400'` (25 MiB; the default is 10240000 and the value includes envelope information).
2. Align any content filter and Dovecot-side limits with it.
3. `mailbox_size_limit` (default 51200000) only limits local(8) delivery and must not be smaller than the message size limit; zero means no limit.
## Failure modes
- `mailbox_size_limit` below `message_size_limit`: large messages cannot be delivered locally.
- Excessively small `message_size_limit` loses non-delivery notifications whose size exceeds it.
## Verify
- Send a message just over the limit; expect a rejection.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.

## Checked
Date: 2026-11-02. Documentation: Postfix source docs (vdukhovni/postfix html/ tree, same text as postfix.org): postconf(5) message_size_limit, mailbox_size_limit.
Confirmed: `message_size_limit` default 10240000, `mailbox_size_limit` default 51200000 and 0 = no limit.
Corrected or removed: the backwards statement that a limit below mailbox_size_limit breaks delivery (the mailbox limit must not be smaller), the 552 5.3.4 text, base64 and ClamAV/Rspamd claims.
Method: documentation only; no commands were run.
