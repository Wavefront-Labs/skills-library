---
id: computing-software.cloud-infrastructure-engineering.observability.audit-logs-vs-operational-logs
name: audit-logs-vs-operational-logs
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [audit-log-design, audit-vs-operational-logs, structured-logging, compliance, log-retention, security]
level: practitioner
status: draft
description: "Design audit logs separately from operational logs: who/what/when schema, append-only storage, retention and integrity, and separate pipelines."
sources: ["https://kubernetes.io/docs/tasks/debug/cluster/audit/", "https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html", "https://csrc.nist.gov/pubs/sp/800/92/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Audit logs vs operational logs

| | Operational logs | Audit logs |
|---|---|---|
| Purpose | debugging, observability | accountability, compliance, forensics |
| Loss tolerance | sampling and drops acceptable | never sampled, delivery guaranteed |
| Retention | days to weeks | months to years per regulation |
| Mutability | can be deleted/compacted | append-only, tamper-evident |
| Access | engineers | restricted, access itself audited |

## Audit event schema
`timestamp`, `actor` (user/service id, auth method), `action` (verb), `resource` (type + id), `outcome` (success/failure + reason), `source` (IP, user agent, request id/trace id), `tenant`, `changes` (before/after for config, never secrets).

## Pipeline
- Emit audit events through a dedicated logger/topic, not the app's general logger, so log level changes cannot disable them.
- Ship to separate storage: object storage with Object Lock (WORM) or a SIEM; keep a copy outside the production account.
- Integrity: hash chain or signed batches; S3 Object Lock compliance mode; restrict delete permissions.
- Kubernetes API audit: `--audit-policy-file` with levels `Metadata` for most, `RequestResponse` for RBAC changes; ship via webhook or file.

## Gotchas
- Putting audit events in Loki with 14-day retention fails compliance; route by stream to a separate tenant with long retention.
- Never log secrets, tokens or full request bodies in audit trails; log that a secret changed, not its value.
- Clock skew undermines ordering: sync time (chrony) and include monotonic sequence numbers.

## Verify
- [ ] Changing log level to ERROR does not stop audit events.
- [ ] A test delete of audit storage is denied; retention meets the written policy.
