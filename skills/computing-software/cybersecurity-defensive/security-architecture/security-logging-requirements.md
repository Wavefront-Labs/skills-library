---
id: computing-software.cybersecurity-defensive.security-architecture.security-logging-requirements
name: security-logging-requirements
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [security-logging-requirements, logging-standard, audit-events, owasp-logging, log-retention, nist-sp-800-92, detection-requirements]
level: practitioner
status: draft
description: "Define security logging requirements for a system: which events, mandatory fields, time sync, integrity, retention, privacy redaction and SIEM onboarding acceptance tests."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html", "https://csrc.nist.gov/pubs/sp/800/92/final", "https://owasp.org/www-project-application-security-verification-standard/", "https://www.cisa.gov/resources-tools/resources/best-practices-event-logging-and-threat-detection"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Security logging requirements

Write these into the system's non-functional requirements so logging is designed, not retrofitted.

## Events (minimum)
- Authentication success/failure, MFA events, lockouts, password/MFA resets.
- Authorisation failures (access denied), privilege changes, role assignments.
- Admin actions and configuration changes, including security settings and log settings.
- Session creation/termination, token issuance/revocation.
- Data access to sensitive records (read for regulated data), bulk export.
- Input validation failures indicative of attack (deserialisation errors, WAF blocks).
- Application start/stop, errors in security controls.

## Mandatory fields
Timestamp (UTC, ISO 8601, ms), event type, outcome, actor (user ID, not just name), source IP and
user agent, target object, application/service and host, correlation/request ID, session ID (hashed).
Prefer a structured format (JSON) mapped to a schema (ECS, OCSF, CIM).

## Never log
Passwords, full tokens/session IDs, secrets, full PAN, encryption keys; mask PII per privacy rules.

## Integrity and retention
- Ship off-host in near real time; append-only/immutable store; access restricted and audited.
- Retention from regulation and detection needs (e.g. 12 months, 3 months hot).
- NTP-synchronised clocks.

## Acceptance tests
For each event type: trigger it in test, confirm it reaches the SIEM parsed with all mandatory
fields within the agreed latency, and a detection rule exists or is backlogged.

## Gotchas
- Logging only failures hides account takeover (successful logins after spray).
- Log injection: encode CR/LF and delimiters in user-controlled values.

## Verify
- [ ] Event catalogue signed off by the SOC.
- [ ] Acceptance tests passed before go-live.
