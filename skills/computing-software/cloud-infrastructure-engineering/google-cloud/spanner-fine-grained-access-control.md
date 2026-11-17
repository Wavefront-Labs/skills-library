---
id: computing-software.cloud-infrastructure-engineering.google-cloud.spanner-fine-grained-access-control
name: spanner-fine-grained-access-control
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, spanner, spanner-fine-grained-access, spanner-iam-roles, database-roles, least-privilege]
level: advanced
status: docs-checked
description: "Restrict Spanner access below the database level: IAM roles vs database roles, GRANT on tables/columns/views, mapping principals with databaseRoleUser and conditions."
sources: ["https://docs.cloud.google.com/spanner/docs/fgac-about", "https://docs.cloud.google.com/spanner/docs/configure-fgac", "https://docs.cloud.google.com/spanner/docs/access-with-fgac", "https://docs.cloud.google.com/spanner/docs/data-definition-language"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spanner fine-grained access control

IAM alone is database-wide (`roles/spanner.databaseReader`, `databaseUser`, `databaseAdmin`). FGAC adds
SQL **database roles** with table/column/view/change-stream privileges.

## 1. Pick the IAM layer
| Role | Use |
|---|---|
| `roles/spanner.databaseReader` / `databaseUser` | database-level IAM access; a session that names no database role is checked against database-level IAM |
| `roles/spanner.fineGrainedAccessUser` | may connect, but only sees what its database roles grant |
| `roles/spanner.databaseRoleUser` (with condition) | which database roles a principal may assume |
| `roles/spanner.databaseAdmin` | DDL incl. creating roles; keep for CI/migrations |

FGAC co-exists with database-level IAM. If a session specifies no database role, Spanner checks database-level IAM permissions; if you do specify a role and the FGAC check fails, the operation fails with no fallback to IAM. Do not give FGAC-only principals broad database-level roles.

## 2. Create roles and grants (DDL)
```sql
CREATE ROLE analyst;
GRANT SELECT ON TABLE Orders TO ROLE analyst;
GRANT SELECT(OrderId, Total, CreatedAt) ON TABLE Customers TO ROLE analyst;  -- column-level
GRANT SELECT ON VIEW OrdersSummary TO ROLE analyst;  -- a definer's-rights view needs SELECT only on the view; an invoker's-rights view also needs SELECT on its underlying objects
CREATE ROLE writer; GRANT INSERT, UPDATE ON TABLE Orders TO ROLE writer;
GRANT ROLE analyst TO ROLE writer;  -- writer inherits analyst's privileges
```

## 3. Map principals to database roles
```bash
gcloud spanner databases add-iam-policy-binding <DB> --instance=<I> \
  --member=serviceAccount:reporting@<P>.iam.gserviceaccount.com \
  --role=roles/spanner.fineGrainedAccessUser
gcloud spanner databases add-iam-policy-binding <DB> --instance=<I> \
  --member=serviceAccount:reporting@<P>.iam.gserviceaccount.com \
  --role=roles/spanner.databaseRoleUser \
  --condition='expression=resource.type == "spanner.googleapis.com/DatabaseRole" && resource.name.endsWith("/analyst"),title=analyst-only'
```
Clients pass the role when creating the session (for example `databaseRole` in Node.js, `database_role` in Python, `setDatabaseRole` in Java, `--database-role=analyst` in `gcloud spanner databases execute-sql`). Without a condition on `databaseRoleUser`, the principal may use all database roles.

## Gotchas
- Enabling FGAC for a principal automatically grants the `public` database role, which has no privileges by default; keep grants off it. The system role `spanner_info_reader` is needed to see unfiltered `INFORMATION_SCHEMA` results.
- A role cannot be dropped until all its privileges are revoked (`REVOKE ROLE parent FROM ROLE child`, then `DROP ROLE child`).

## Verify
- [ ] `gcloud spanner databases execute-sql <DB> --instance=<I> --database-role=analyst --sql="SELECT Email FROM Customers"` fails, while the granted columns succeed.
- [ ] `SELECT * FROM INFORMATION_SCHEMA.TABLE_PRIVILEGES WHERE grantee = 'analyst'` shows only intended grants.

## Checked
Checked 2026-10-24 against the Spanner FGAC overview, configure-FGAC, access-with-FGAC, DDL reference and the gcloud `spanner databases execute-sql` reference (docs.cloud.google.com). Confirmed `CREATE ROLE`, table and column-level `GRANT`, `GRANT ROLE ... TO ROLE`, the two IAM roles and the condition expression, `--database-role`, the `public` and `spanner_info_reader` roles, view privilege rules and role dropping. Removed the claim that databaseReader or databaseUser bypass FGAC, and the dropped-table grant claim, which the pages do not state.
Method: documentation only; no commands were run.
