---
id: computing-software.database-administration.cockroachdb.role-based-sql-audit-logging
name: role-based-sql-audit-logging
category: computing-software
field: database-administration
product: cockroachdb
tags: [audit-logging, sql-log-user-audit, role-based-audit, security-logging, compliance]
level: practitioner
status: docs-checked
description: "Turn on per-role SQL audit logging in CockroachDB with the sql.log.user_audit cluster setting, matching order, filters, privileges and examples."
sources:
  - https://www.cockroachlabs.com/docs/stable/role-based-audit-logging
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: record SQL activity of specific users or roles for compliance.

Mechanism: the cluster setting `sql.log.user_audit` holds a table-like list; each row is `USER/ROLE  STATEMENT_FILTER`. The special role name `ALL` matches every user. `STATEMENT_FILTER` keywords are `ALL` (audit every statement) and `NONE` (audit none). The first row that matches a user, by name or role membership, applies and iteration stops, so put specific rows first. Changes apply immediately within existing user sessions.

Privileges needed: `admin` role or the `MODIFYCLUSTERSETTING` system privilege.

Examples from the page:
```sql
-- exclude one role, audit everyone else
SET CLUSTER SETTING sql.log.user_audit = '
    service_account_role NONE
    ALL ALL
';
-- audit only one role
SET CLUSTER SETTING sql.log.user_audit = '
    test_role       ALL
    another_role    NONE
    ALL             NONE
';
SHOW CLUSTER SETTING sql.log.user_audit;
```
`sql.log.user_audit.reduced_config.enabled` computes a reduced audit configuration once, at the user's first SQL event after the setting is enabled, instead of at each event; later changes to role memberships or the cluster setting are then not reflected within an existing session.

Output: events of type `role_based_audit_event`, JSON payload including application name, query text, user and more. The query text can contain PII, so protect and route the audit log file sink accordingly (see the logging configuration page).

By default audit log files are prefixed `cockroach-sql-audit`. The page notes the feature is subject to change.

## Checked

2026-11-03. Confirmed against the role-based audit logging page: `sql.log.user_audit` syntax, `ALL` and `NONE`, privileges, matching order, examples, reduced-config setting, payload contents, file prefix. Removed: the unsupported claim of further filter keywords, the overhead claim and the invented verification step.
Method: documentation only; no commands were run.
