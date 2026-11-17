---
id: computing-software.email-administration.mail-server-administration.queue-length-alerting
name: queue-length-alerting
category: computing-software
field: email-administration
product: mail-server-administration
tags: [queue-length-alerting, queue-alerting, qshape, queue-size]
level: practitioner
status: draft
description: "Alert on Postfix queue growth and deferred age with qshape and a simple script or Prometheus exporter."
sources:
  - https://www.postfix.org/documentation.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Queue length alerting

**Goal:** catch stuck delivery early.
## Steps
1. Count: `postqueue -p | tail -1` (summary) or `find /var/spool/postfix/deferred -type f | wc -l`.
2. Shape: `qshape -s deferred` for senders and `qshape deferred` for recipient domains by age.
3. Alert on sustained growth, not momentary spikes (for example above your baseline for 15 minutes).
4. Export via a Postfix exporter if you use Prometheus (third-party; names vary).
## Failure modes
- A spam run floods the active queue; alert on both active and deferred.
## Verify
- Stop outbound in staging; the alert fires and clears after flush.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
