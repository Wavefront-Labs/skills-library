---
id: computing-software.database-administration.cloudnative-pg.upgrade-1-30-security-changes
name: upgrade-1-30-security-changes
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [upgrade, security, cve, scram-sha-256, passwordpassthrough, search-path, lease, databaserole]
level: advanced
status: docs-checked
description: "What changes moving to CloudNativePG 1.30.0, 1.29.2 or 1.28.4: SCRAM encoding, pinned search_path, DatabaseRole, Lease-based primary election and status-port authentication."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/installation_upgrade.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Review these before upgrading to 1.30.0 (or 1.29.2 / 1.28.4 for the two CVE fixes).

**Password encoding (CVE-2026-55765).** The operator now SCRAM-SHA-256 encodes role passwords before `CREATE`/`ALTER ROLE`, for the superuser, application-user and managed-role Secrets, so cleartext never reaches `pg_stat_statements` or `pgaudit`. If a cluster overrides `password_encryption` (for example `md5`) and PostgreSQL should hash instead, set `cnpg.io/passwordPassthrough: "enabled"` on each **basic-auth Secret**, not on the `Cluster`; a cleartext value is then visible to those extensions.

**search_path (CVE-2026-55769).** Operator connections pin `pg_catalog, public, pg_temp`. Custom monitoring queries run in a transaction with that path, so schema-qualify objects in other schemas (`myschema.mytable`). `postInit*` and import post-SQL are unaffected.

**Safe primary election (1.30.0).** Promotion is coordinated through a per-cluster `Lease`. If you manage operator RBAC yourself, grant `create`, `delete`, `get`, `list`, `update`, `watch` on `leases` in `coordination.k8s.io` **before** upgrading, or primaries cannot promote.

**Operator-to-instance authentication (1.30.0).** Sensitive status-port endpoints (backup, `pg_controldata`, partial WAL archive, instance-manager upgrade) require a pinned client certificate; the port must be TLS, the default since 1.24. Earlier releases should keep a `NetworkPolicy` on TCP 8000.

Also new in 1.30.0: standalone `DatabaseRole` resources; and from releases older than 1.29.1/1.28.3 the metrics exporter runs as `cnpg_metrics_exporter` with `pg_monitor` only (CVE-2026-44477), so custom queries over user tables need explicit `GRANT`s.

## Checked

2026-11-04. Upgrade notes for 1.30.0, 1.29.2 and 1.28.4 (CVE-2026-55765, CVE-2026-55769, Lease RBAC, status-port authentication, CVE-2026-44477) confirmed on the Installation and upgrades page.

Method: documentation only; no commands were run.
