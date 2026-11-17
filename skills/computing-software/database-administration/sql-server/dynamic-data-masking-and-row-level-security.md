---
id: computing-software.database-administration.sql-server.dynamic-data-masking-and-row-level-security
name: dynamic-data-masking-and-row-level-security
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, azure-sql, sql-server-security, dynamic-data-masking, ddm, row-level-security, rls, security-policy, predicate-function, unmask, multi-tenant]
level: practitioner
status: docs-checked
description: "Apply SQL Server dynamic data masking and row-level security policies correctly, and know the inference attacks and performance traps of each."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/security/dynamic-data-masking
  - https://learn.microsoft.com/en-us/sql/relational-databases/security/row-level-security
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic data masking and row-level security

## Dynamic data masking (DDM)
Masks column values in query results for users without `UNMASK`. Data is stored
unchanged; it is a presentation control, **not** encryption.
```sql
ALTER TABLE dbo.customers ALTER COLUMN email ADD MASKED WITH (FUNCTION = 'email()');
ALTER TABLE dbo.customers ALTER COLUMN phone ADD MASKED WITH (FUNCTION = 'partial(0,"XXX-XXX-",4)');   -- prefix,padding,suffix
ALTER TABLE dbo.customers ALTER COLUMN credit_limit ADD MASKED WITH (FUNCTION = 'random(1,100)');
ALTER TABLE dbo.customers ALTER COLUMN birth_date ADD MASKED WITH (FUNCTION = 'default()');
GRANT UNMASK TO support_lead;                        -- database-wide; SQL Server 2022+ also allows UNMASK ON schema/table/column
SELECT OBJECT_NAME(object_id), name, masking_function FROM sys.masked_columns WHERE is_masked = 1;
```
Other mask: `datetime("Y")` style (SQL Server 2022+). Adding or changing a mask needs `ALTER ANY MASK` plus ALTER on the table.
A mask cannot be put on Always Encrypted, FILESTREAM, COLUMN_SET/sparse-in-column-set or computed columns,
PolyBase external table columns, or a column with dependencies (drop the dependent index first).
Limits to tell stakeholders:
- Users with ad hoc query access can infer values: `WHERE credit_limit > 5000`
  filters on the real value; brute-force predicates reveal it (Microsoft says to enable auditing if such access is granted).
- Masks do not stop `UPDATE`: users with write permission can still change the data.
- `sysadmin`, `db_owner` and anyone with `CONTROL` see everything (CONTROL includes UNMASK and ALTER ANY MASK).
  `SELECT INTO`/`INSERT INTO` and Import/Export by a masked user store masked values.
Use DDM to hide data from app screens and support staff using fixed queries; use
Always Encrypted or permissions where real secrecy is needed.

## Row-level security (RLS)
A schema-bound inline table-valued function is applied as a filter predicate (silently
hides rows) and/or block predicate (rejects writes) via a security policy.
```sql
CREATE SCHEMA sec;
GO
CREATE FUNCTION sec.fn_tenant_filter(@tenant_id int)
RETURNS TABLE WITH SCHEMABINDING
AS RETURN SELECT 1 AS ok
   WHERE @tenant_id = CAST(SESSION_CONTEXT(N'tenant_id') AS int)
      OR IS_MEMBER('db_owner') = 1;
GO
CREATE SECURITY POLICY sec.tenant_policy
  ADD FILTER PREDICATE sec.fn_tenant_filter(tenant_id) ON dbo.orders,
  ADD BLOCK PREDICATE  sec.fn_tenant_filter(tenant_id) ON dbo.orders AFTER INSERT
  WITH (STATE = ON);
-- app, after opening a connection:
EXEC sp_set_session_context @key = N'tenant_id', @value = 42, @read_only = 1;
```
Rules:
- Keep the predicate function trivial and sargable; it is inlined into every query.
  Index `tenant_id` (usually leading key) or every query scans.
- With connection pooling, set session context on every checkout (`@read_only = 1`
  stops the app resetting it mid-session).
- Side channels: error-based queries (e.g. `SELECT 1/(salary-100000)`) can leak filtered values
  to users with ad hoc access; RLS is for app-mediated access.
- Permissions: creating/altering/dropping a policy needs `ALTER ANY SECURITY POLICY` and, to create or drop, `ALTER` on the schema;
  each predicate also needs SELECT and REFERENCES on the function, REFERENCES on the target table and its argument columns.
- Policies apply to dbo and `db_owner` too, so the function must allow admins explicitly (as the example does).
- Block predicates: `AFTER INSERT`, `AFTER UPDATE`, `BEFORE UPDATE`, `BEFORE DELETE`. Indexed views cannot sit on a table with a policy;
  security predicates on a temporal table are not copied to its history table.

## Verify
- [ ] Masked user sees masked output; `UNMASK` grantees listed and justified.
- [ ] As each tenant (set session context), counts match that tenant's rows only.
- [ ] Execution plans for hot queries still seek on the tenant column.

## Checked
Date 2026-10-23. Documentation release: SQL Server 2025 pages for Dynamic Data Masking and Row-Level Security (2016+ features; 2022 gates noted).
Confirmed: mask function syntax and the 2022 datetime mask, UNMASK/CONTROL/ALTER ANY MASK semantics, 2022 granular UNMASK, `sys.masked_columns`, inference and SELECT INTO behaviour, RLS predicate types, SCHEMABINDING function, permissions, SESSION_CONTEXT with `@read_only`, side-channel notes, indexed-view and temporal restrictions.
Method: documentation only; no commands were run.
