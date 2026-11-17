---
id: computing-software.cybersecurity-defensive.keycloak.brute-force-detection
name: brute-force-detection
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, brute-force, lockout, login-failures, wait-increment]
level: practitioner
status: docs-checked
description: "Enable and tune Keycloak brute-force detection: permanent, temporary or mixed lockout, wait strategy, failure reset time, quick-login checks."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/threat/brute-force.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# brute force detection
Brute force detection is disabled by default. Enable it in *Realm Settings* > *Security Defenses* > *Brute Force Detection* and choose a Brute Force Mode. It applies only to password, OTP and recovery codes. A locked user still sees the default `Invalid username or password` message so an attacker cannot tell the account is disabled.

Permanent lockout: the account is disabled until an administrator re-enables it; enabling resets the count. Parameters (defaults): Max Login Failures 30, Quick Login Check Milliseconds 1000 milliseconds, Minimum Quick Login Wait 1 minute.

Temporary lockout: the wait grows as the attack continues. Defaults: Max Login Failures 30, Strategy to increase wait time Multiple, Wait Increment 1 minute, Max Wait 15 minutes, Failure Reset Time 12 hours, Quick Login Check Milliseconds 1000, Minimum Quick Login Wait 1 minute. The failure count resets when a failure comes later than Failure Reset Time after the last failure, and on successful login.

Strategies for the wait:
- *Multiple* (default): wait is Wait Increment * (count / Max Login Failures), integer division rounded down. With Max Login Failures 5 and Wait Increment 30 s: 30 s at 5 to 9 failures, 60 s at 10.
- *Linear*: wait is Wait Increment * (1 + count - Max Login Failures). Same settings: 30 s at 5, 60 s at 6, 90 s at 7.

Mixed mode, *Lockout permanently after temporary lockout*: adds Maximum temporary Lockouts (default 1); when the temporary-lockout counter exceeds it, the user is locked permanently.

Secondary Authentication Failures Lockout applies to all modes; it is off at 0. A non-zero Maximum Secondary Authentication Failures permanently locks the user after that many failed second-factor attempts (currently only OTP); the page suggests 100.

Rules and gotchas:
- Keep Failure Reset Time greater than Max Wait, otherwise the effective wait never reaches Max Wait.
- The count does not increment when a temporarily disabled account fails to log in.
- Brute force detection makes the server open to denial of service: an attacker who knows account names can get them disabled. The docs suggest intrusion prevention software; Keycloak logs every login failure with the client IP, so an IPS can watch the server log and block addresses at the firewall.

## Checked
2026-11-03. Confirmed against server_admin/topics/threat/brute-force.adoc: defaults, both strategies and their formulas, mixed mode, secondary-authentication lockout, reset-time rule, DoS note. Removed: the "5-10 failures" tuning advice, "rate limits at the proxy" and the invented Verify step.
Method: documentation only; no commands were run.
