---
id: computing-software.database-administration.sql.row-level-security-policies
name: row-level-security-policies
category: computing-software
field: database-administration
product: sql
tags: [sql, row-level-security-policies]
level: advanced
status: docs-checked
description: "Restrict rows per user with PostgreSQL row-level security."
sources: ["https://www.postgresql.org/docs/current/ddl-rowsecurity.html", "https://www.postgresql.org/docs/current/sql-createpolicy.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Row-level security policies

- `ALTER TABLE t ENABLE ROW LEVEL SECURITY; CREATE POLICY tenant_p ON t USING (tenant_id = current_setting('app.tenant')::int) WITH CHECK (tenant_id = current_setting('app.tenant')::int);`
- Superusers and roles with BYPASSRLS always bypass row security; table owners normally bypass it unless `ALTER TABLE ... FORCE ROW LEVEL SECURITY`.
- With row security enabled and no applicable policy, a default-deny policy applies: no rows are visible or modifiable.
- Self-check: connect as a non-owner role and compare visible rows.

## Checked

2026-11-02. Confirmed in the row security page and CREATE POLICY page: bypass rules, FORCE ROW LEVEL SECURITY, default deny. Removed: policy-column indexing and SET LOCAL advice (not stated in pages read).
Method: documentation only; no commands were run.
