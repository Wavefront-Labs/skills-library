---
id: computing-software.cybersecurity-defensive.security-architecture.database-activity-monitoring
name: database-activity-monitoring
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [database-activity-monitoring, dam, database-auditing, pgaudit, sql-server-audit, oracle-unified-auditing, privileged-user-monitoring]
level: practitioner
status: draft
description: "Monitor database activity: native audit (pgAudit, SQL Server Audit, Oracle Unified Auditing) or DAM agents, what to capture, SIEM use cases and protecting the audit trail."
sources: ["https://github.com/pgaudit/pgaudit", "https://learn.microsoft.com/en-us/sql/relational-databases/security/auditing/sql-server-audit-database-engine", "https://docs.oracle.com/en/database/oracle/oracle-database/19/dbseg/introduction-to-auditing.html", "https://www.cisecurity.org/controls/v8"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Database activity monitoring

## What to capture (not everything - volume kills DAM)
- All privileged/DBA sessions and DDL, grants/role changes, audit configuration changes.
- Logins (success and failure), especially from new hosts or tools.
- SELECTs against sensitive tables (cardholder, PII) by humans; bulk reads by service accounts.

## Native options
**PostgreSQL (pgAudit):**
```
shared_preload_libraries = 'pgaudit'
pgaudit.log = 'ddl, role, write'
pgaudit.log_relation = on
# object-level auditing for sensitive tables:
pgaudit.role = 'auditor'      -- then: GRANT SELECT ON customers TO auditor;
```
**SQL Server:** server audit to file/Security log + server audit spec (`FAILED_LOGIN_GROUP`, `SERVER_ROLE_MEMBER_CHANGE_GROUP`, `DATABASE_PERMISSION_CHANGE_GROUP`) + database audit spec (`SELECT ON dbo.Cards BY public`).
**Oracle:** Unified Auditing policies (`CREATE AUDIT POLICY ... ACTIONS SELECT ON hr.employees`, `AUDIT POLICY ... EXCEPT svc_app`).
**Cloud:** RDS/Aurora database activity streams, Azure SQL auditing to Log Analytics, Cloud SQL pgAudit flags.

## SIEM use cases
- DBA account reading sensitive tables outside change windows.
- Service account used interactively (SSMS/DBeaver/psql client name) or from a non-app host.
- Row counts far above baseline in a single query/session.
- Audit disabled or audit policy altered.

## Gotchas
- DBAs can disable native auditing; ship logs off-host immediately and alert on audit config change, or use an agent/network DAM DBAs do not control.
- Connection pooling hides end users; pass application user context (e.g. `SET application_name`, `SESSION_CONTEXT`).
- Full statement logging may capture sensitive values in literals.

## Verify
- [ ] A test SELECT on a sensitive table appears in the SIEM within minutes with user and host.
- [ ] Disabling audit raises an alert.
