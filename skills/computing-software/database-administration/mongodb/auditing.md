---
id: computing-software.database-administration.mongodb.auditing
name: auditing
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, mongodb-security, mongodb-auditing, audit-log, audit-filter, auditauthorizationsuccess, enterprise-audit, compliance]
level: practitioner
status: docs-checked
description: "Enable MongoDB Enterprise/Atlas auditing: audit log destinations and format, filters for auth, DDL and user changes, runtime filter changes and log volume."
sources:
  - https://www.mongodb.com/docs/manual/core/auditing/
  - https://www.mongodb.com/docs/manual/tutorial/configure-audit-filters/
  - https://www.mongodb.com/docs/manual/reference/audit-message/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Auditing

**Goal:** a tamper-evident record of who authenticated, changed users/roles, and altered schemas, for compliance, without drowning in volume.

## Enable (MongoDB Enterprise; Atlas has its own database auditing settings)
```yaml
auditLog:
  destination: file              # file | syslog | console
  format: JSON                   # or BSON
  path: /var/log/mongodb/audit.json
  filter: '{ atype: { $in: [ "authenticate", "createUser", "dropUser", "updateUser", "grantRolesToUser", "revokeRolesFromUser", "createRole", "dropDatabase", "dropCollection", "createIndex", "dropIndex", "shutdown" ] } }'
setParameter:
  auditAuthorizationSuccess: false   # true also audits CRUD operations (authCheck success): large volume
```

## Filters
Filters match audit message fields (`atype`, `param`, `users`, `roles`, `result`):
```javascript
// failed authentications only
{ atype: "authenticate", "param.mechanism": "SCRAM-SHA-256", result: 18 }
// CRUD on one collection (needs auditAuthorizationSuccess: true)
{ atype: "authCheck", "param.ns": "hr.salaries", "param.command": { $in: ["find","update","delete"] } }
```
5.0+: set `auditLog.runtimeConfiguration: true` in the config file (restart once; the server refuses to start if `auditLog.filter` or `auditAuthorizationSuccess` is also set there), then change the filter and `auditAuthorizationSuccess` at runtime with the `auditConfig` cluster parameter (7.1+, via `setClusterParameter`) or the deprecated `setAuditConfig` command (5.0+). With runtime configuration on, drop `filter` and `auditAuthorizationSuccess` from the YAML above.

## Message
```json
{ "atype": "createUser", "ts": { "$date": "2026-10-16T03:12:44Z" }, "local": {...}, "remote": { "ip": "10.0.4.7" },
  "users": [ { "user": "admin", "db": "admin" } ], "param": { "user": "etl", "db": "admin", "roles": [...] }, "result": 0 }
```
`result` 0 = success; for `authCheck` 13 = unauthorized; for `authenticate` 18 = authentication failed.

## Operations
- Ship to SIEM (syslog destination, or filebeat on the JSON file). Rotate with `db.adminCommand({ logRotate: "audit" })`.
- 8.0+: `auditLog.schema` selects `mongo` (default) or `OCSF` message format.
- Audit logs can contain query predicates (PII); restrict file permissions.

## Gotchas
- `auditAuthorizationSuccess: true` without a narrow filter produces very large logs; pair it with a filter.
- Events go to an in-memory buffer and are flushed periodically, so events can be lost if the server terminates; if the server cannot write to the audit destination it terminates.
- Since 5.0 secondaries do not log DDL audit events for replicated changes.

## Verify
Create and drop a test user; both events appear in the audit log with the acting user and remote IP.

## Checked

2026-10-25, against the MongoDB manual source (mongodb/docs repository, content/manual/manual, latest commit 2026-10-23). Confirmed: destinations (console, syslog, JSON, BSON), auditAuthorizationSuccess for CRUD, 5.0 runtimeConfiguration rules and startup failure, auditConfig cluster parameter (7.1), setAuditConfig deprecated, result codes for authCheck (13) and authenticate (18), auditLog.schema OCSF (8.0), logRotate with "audit", server terminates if audit destination unwritable. Removed unconfirmed Percona, BSON-speed and throughput claims.

Method: documentation only; no commands were run.
