---
id: computing-software.web-development.node-express.logging-auth-and-access-events
name: logging-auth-and-access-events
category: computing-software
field: web-development
product: node-express
tags: [security-logging, auth-event-logging, audit-logging, owasp, monitoring]
level: practitioner
status: docs-checked
description: "Logging authentication and authorization events for detection and forensics: which events, structured fields, correlation IDs, retention, and tamper resistance."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
  - https://owasp.org/Top10/2025/A09_2025-Security_Logging_and_Alerting_Failures/
  - https://cheatsheetseries.owasp.org/cheatsheets/Logging_Vocabulary_Cheat_Sheet.html
  - https://expressjs.com/en/guide/behind-proxies.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Logging auth and access-control events

## 1. Events to log (OWASP Top 10 A09 / ASVS 5.0 V16)
- Login success, failure (with reason category, not the password), lockout, logout.
- MFA enrol/remove, challenge failures, recovery-code use.
- Password change/reset request/complete, email change.
- Session creation/revocation, token refresh failures, API key create/revoke.
- Authorization failures (403s), especially repeated ones and IDOR-shaped patterns.
- Privilege changes: role grants, admin actions, impersonation start/stop.
- Input validation failures at volume, CSRF failures, rate-limit trips.

## 2. Structured format
```js
logger.info({
  event: "authn_login_fail",            // OWASP logging vocabulary style
  outcome: "failure", reason: "bad_password",
  user_id: user?.id ?? null, username_hash: sha256(email),   // avoid raw identifiers if policy requires
  ip: req.ip, user_agent: req.get("user-agent"),
  request_id: req.id, session_id_hash: hash(req.sessionID),
  ts: new Date().toISOString(),
}, "login failed");
```
Use JSON logs (pino, winston, structlog, lograge). Include who, what, when (UTC), where (IP, service, endpoint), outcome, and a correlation ID propagated across services (`traceparent`).
Behind proxies, configure `app.set("trust proxy", ...)` correctly or `req.ip` is your load balancer (or attacker-spoofed `X-Forwarded-For`).

## 3. Storage
- Ship off-host immediately (CloudWatch, Loki, Elastic, Datadog, SIEM) so an attacker on the box cannot erase them.
- Append-only/immutable storage for audit events. Retention per policy/regulation.
- Restrict who can read logs - they contain personal data.

## 4. Audit trail vs debug logs
Business audit events (who changed the payout account) belong in a durable audit table/stream with integrity guarantees, not just app logs that are sampled or dropped.

## Verify
Trigger each event in staging and find it in the central log store with all fields; confirm logs survive instance termination.

## Checked

2026-10-25 against OWASP Cheat Sheet Series (OWASP/CheatSheetSeries, commit of 2026-10-24), the OWASP ASVS 5.0 repository, OWASP Top 10 2025 and the Express 5 docs. Confirmed: event names such as authn_login_fail, authz_fail, authz_admin and authn_token_revoked exist in the OWASP logging vocabulary; ASVS 5.0 chapter V16 is Security Logging and Error Handling (V7 is Session Management); OWASP Top 10 2025 A09 is Security Logging and Alerting Failures; session identifiers should be hashed or removed from logs; Express trust proxy controls how req.ip is derived from X-Forwarded-For.

Method: documentation only; no commands were run.
