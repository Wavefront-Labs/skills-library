---
id: computing-software.cybersecurity-defensive.application-security.security-logging-failures
name: security-logging-failures
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [security-logging-failures, owasp-a09, application-security-logging, security-event-logging, alerting, audit-trail, appsec]
level: practitioner
status: gated
description: "Close OWASP A09 security logging and monitoring failures in an app: which events to log, required fields, protecting logs, alerting on abuse, and testing detection."
sources: ["https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/", "https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html", "https://cheatsheetseries.owasp.org/cheatsheets/Logging_Vocabulary_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Security logging and monitoring failures (OWASP A09:2021) (gated: unconfirmed, source is paywalled or blocked)

The failure: attacks happen and nobody can see them, or can reconstruct them afterwards.

## Events the application must log
- Authentication: success, failure, lockout, MFA enrol/remove, password change/reset.
- Authorisation failures (denied access to objects, attempts to reach admin functions).
- Input validation failures that indicate attack (not every typo).
- Session events: creation, invalidation, token refresh anomalies.
- High-value transactions and admin actions: role changes, payout details, exports, config changes.
- Application errors and security control failures (WAF block, signature check failed).
The OWASP Logging Vocabulary gives standard event names (`authn_login_fail`, `authz_fail`, `privilege_permissions_changed`).

## Fields per event
Timestamp (ISO 8601 with UTC offset), event type, user/principal ID, tenant, source IP (from trusted proxy header only),
user agent, resource/object ID, outcome, request/correlation ID, service and version.

## Never log
Passwords, session tokens, API keys, full card numbers, secrets, excessive PII. Mask or hash where
correlation is needed.

## Protect and ship
Structured (JSON) logs to a central store the app cannot delete from; encode/neutralise user input to prevent
log injection; retention aligned to policy; clock sync.

## Monitoring
Alerts for: many login failures across accounts (credential stuffing), authz failures from one user across
many objects (IDOR probing), admin actions out of hours, impossible travel. Each alert needs an owner and a
runbook.

## Verify
In a test environment run a short attack script (failed logins, IDOR attempts, one admin action) and confirm
each produces the expected events in the SIEM with correct fields and that at least the stuffing and IDOR
patterns raise alerts.

## Checked

2026-10-28. Confirmed in the OWASP Logging Cheat Sheet: ISO 8601 with UTC offset, log-injection warning; OWASP Logging Vocabulary Cheat Sheet: `authn_login_fail`, `authz_fail`, `privilege_permissions_changed`. Removed: the unsourced dwell-time statement and the 403 status detail. The A09:2021 category name could not be confirmed because the OWASP Top 10 page returned a stub, so it is gated.
Method: documentation only; no commands were run.
