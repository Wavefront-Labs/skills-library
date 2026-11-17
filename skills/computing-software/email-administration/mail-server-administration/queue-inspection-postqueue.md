---
id: computing-software.email-administration.mail-server-administration.queue-inspection-postqueue
name: queue-inspection-postqueue
category: computing-software
field: email-administration
product: mail-server-administration
tags: [queue-inspection-postqueue, postfix-queue, postqueue, mailq, postcat, deferred-queue]
level: practitioner
status: draft
description: "Inspect the Postfix queue with postqueue -p, mailq, postcat and the queue ID, and read deferral reasons."
sources:
  - https://www.postfix.org/documentation.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Queue inspection postqueue

**Goal:** find what is stuck and why.
## Steps
1. `postqueue -p` lists queue entries (`!` = on hold, `*` = active) with the deferral reason in parentheses.
2. `postcat -q <queue-id>` shows the envelope and message (headers and body).
3. `qshape deferred` summarises by recipient domain and age.
4. Trigger a retry: `postqueue -f` (flush all) or `postqueue -i <queue-id>` (one message).
## Failure modes
- Mass flush against a blocked destination makes you look worse; fix the cause first.
- Reading message bodies is sensitive: do it only as needed.
## Verify
- After the fix, `postqueue -p` count falls and log lines show `status=sent`.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
