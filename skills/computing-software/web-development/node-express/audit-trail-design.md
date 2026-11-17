---
id: computing-software.web-development.node-express.audit-trail-design
name: audit-trail-design
category: computing-software
field: web-development
product: node-express
tags: [audit-trail, audit-log, tamper-evidence, append-only-log, compliance-logging, security-logging]
level: practitioner
status: docs-checked
description: "Designing an application audit trail: event schema (actor, action, target, changes, context), append-only storage, tamper evidence, retention, customer-facing audit logs."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
  - https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html
  - https://github.com/paper-trail-gem/paper_trail
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Audit trail design

Debug logs answer "what broke"; an audit trail answers "who did what to which record, when, from where" and must survive disputes and investigations.

## 1. Event schema
```json
{
  "id": "01JAB...", "occurred_at": "2026-10-18T09:12:44.123Z",
  "actor": { "type": "user", "id": "u_123", "impersonated_by": "staff_9" },
  "action": "invoice.refund.created",
  "target": { "type": "invoice", "id": "inv_456", "tenant_id": "t_1" },
  "changes": { "status": ["paid", "refunded"], "refund_amount": [null, 4900] },
  "context": { "ip": "203.0.113.7", "user_agent": "...", "request_id": "req_abc", "auth_method": "sso" },
  "outcome": "success"
}
```
- Past-tense, namespaced action names; one event per business action, not per SQL row.
- Record failures for sensitive actions (denied exports, failed admin logins).
- Store field diffs, not full snapshots of sensitive data; never log secrets, tokens, full card numbers.

## 2. Capture
- Explicit calls at the service layer (`audit.record(...)` in the same DB transaction as the change) give business meaning.
- Model-history libraries for your framework, or database triggers into an `audit_log` table.

## 3. Integrity
- Append-only: application role has INSERT only on the audit table (no UPDATE/DELETE); a trigger rejects modifications.
- Tamper evidence: hash chain (`hash = sha256(prev_hash || canonical_json(event))`) and periodically anchor the head hash elsewhere.
- Export to WORM storage (for example S3 Object Lock, which uses a write-once-read-many model) or a separate logging account the app cannot delete from.
- UTC timestamps from synchronised clocks.

## 4. Retention and access
- Retention per regulation/contract; partition by month for cheap pruning/archival.
- Access to audit logs is itself audited; restrict to security/compliance roles.

## Verify
- [ ] Every privileged action in the permission matrix emits an audit event (test asserts it); the app DB role cannot delete audit rows.

## Checked
2026-10-28 Confirmed: Amazon S3 Object Lock uses a write-once-read-many (WORM) model (S3 user guide); OWASP Logging Cheat Sheet covers integrity, tamper detection and protection of logs. Removed: named libraries and pgaudit, compliance-mode wording, retention-years figure, enterprise-expectation claim.
Method: documentation only; no commands were run.
