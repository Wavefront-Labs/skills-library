---
id: computing-software.email-administration.mail-server-administration.queue-lifetime-tuning
name: queue-lifetime-tuning
category: computing-software
field: email-administration
product: mail-server-administration
tags: [queue-lifetime-tuning, maximal-queue-lifetime, bounce-queue-lifetime, queue-backoff]
level: advanced
status: draft
description: "Tune maximal_queue_lifetime, bounce_queue_lifetime, minimal and maximal backoff time and delay warnings."
sources:
  - https://www.postfix.org/documentation.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Queue lifetime tuning

**Goal:** balance retry persistence against queue bloat.
## Steps
1. Defaults: `postconf -d maximal_queue_lifetime minimal_backoff_time maximal_backoff_time` (maximal lifetime is 5d by default).
2. For an internal relay set shorter lifetimes (for example 1d) so users learn fast; keep default for MX.
3. `delay_warning_time = 4h` sends the sender a "delayed" notice (off by default).
4. `postfix reload` after changes.
## Failure modes
- Very short lifetimes bounce mail during a partner outage.
- Huge queues of spam to forged addresses: consider recipient verification at the edge.
## Verify
- `postconf maximal_queue_lifetime`; test with a deferring destination in staging and watch the bounce at expiry.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
