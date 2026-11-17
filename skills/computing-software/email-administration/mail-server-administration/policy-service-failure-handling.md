---
id: computing-software.email-administration.mail-server-administration.policy-service-failure-handling
name: policy-service-failure-handling
category: computing-software
field: email-administration
product: mail-server-administration
tags: [policy-service-failure-handling, policy-service-timeout, policy-fail-open]
level: advanced
status: draft
description: "Handle policy service outages: timeouts, default actions, and monitoring so a dead daemon does not drop or open mail."
sources:
  - https://www.postfix.org/documentation.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Policy service failure handling

**Goal:** know what happens when the policy service is down.
## Facts
- If the connection fails, Postfix defers the request (temporary 4xx) rather than skipping the check (verify on your version).
- Parameters: `smtpd_policy_service_max_idle`, `smtpd_policy_service_max_ttl`, `smtpd_policy_service_timeout`.
## Steps
1. Run the daemon under a supervisor with restart on failure.
2. Alert on `warning: premature end-of-input` or `connect to ...policy: ... failed` in the log.
3. For optional checks, wrap with `check_policy_service` after cheaper static rules only.
## Failure modes
- Single point of failure for all inbound mail.
- Slow lookups (DNS or SQL) inside the daemon multiply per-RCPT latency.
## Verify
- Kill the daemon in staging; observe 4xx for inbound and a log warning; restore and see queue drain.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
