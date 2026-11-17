---
id: computing-software.database-administration.oracle-database.virtual-private-database-dbms-rls
name: virtual-private-database-dbms-rls
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle-security, virtual-private-database, dbms-rls, row-level-security, application-context]
level: advanced
status: docs-checked
description: "Implement Oracle Virtual Private Database row filtering with DBMS_RLS policies, choose policy types, and know who is exempt."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/arpls/DBMS_RLS.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Virtual Private Database (DBMS_RLS)

A policy function returns a predicate that the server adds when a table, view or synonym is referenced in a
statement. The server treats the object as a view over a transient view `SELECT * FROM hr.employees WHERE P1`,
where `P1` is the predicate. The predicate is acquired at statement parse time, and the function may build it from
session environment variables, usually application contexts.

## Policy function
```sql
CREATE OR REPLACE FUNCTION sec.tenant_policy(p_schema VARCHAR2, p_object VARCHAR2)
RETURN VARCHAR2 AS
BEGIN
  RETURN 'tenant_id = SYS_CONTEXT(''app_ctx'', ''tenant_id'')';
END;
/
```
- Signature required: `FUNCTION f (object_schema IN VARCHAR2, object_name VARCHAR2) RETURN VARCHAR2`.
- It must have purity level WNDS (write no database state).
- A zero-length predicate means no restriction for that user, so do not return one by accident.
- If the predicate contains a subquery, the function owner is used to resolve objects and check security in it;
  users need no privileges on the function or underlying policy objects (the server calls it with definer's rights).
- Several policies on one object are ANDed. If a table alias is required, use the table or view name itself.

## Attach the policy
```sql
BEGIN
  DBMS_RLS.ADD_POLICY(
    object_schema   => 'APP', object_name => 'ORDERS',
    policy_name     => 'ORDERS_TENANT',
    function_schema => 'SEC', policy_function => 'TENANT_POLICY',
    statement_types => 'SELECT,INSERT,UPDATE,DELETE',
    update_check    => TRUE,
    policy_type     => DBMS_RLS.CONTEXT_SENSITIVE,
    namespace       => 'app_ctx', attribute => 'tenant_id');
END;
/
```
- `statement_types` defaults to all except `INSERT` and `INDEX`. If you use `INSERT` you must set
  `update_check => TRUE`, otherwise `ORA-28104` is raised. The check applies only to security-relevant columns in
  the policy definition.
- Policy types: `DYNAMIC` (default; re-executes the function on every parse and execution), `STATIC` (executed once,
  cached in the SGA), `SHARED_STATIC`, `CONTEXT_SENSITIVE` (re-evaluated at execution if the context changed; for
  session pooling the middle tier must reset context on client switches), `SHARED_CONTEXT_SENSITIVE`. Setting
  `policy_type` overrides `static_policy`.
- `long_predicate` allows predicates up to 32K bytes (default 4000).
- Column-level VPD: `sec_relevant_cols` enforces the policy only when those columns are referenced (tables and
  views, not synonyms). With `sec_relevant_cols_opt => DBMS_RLS.ALL_ROWS`, all rows are returned for `SELECT` but
  the sensitive columns appear as NULL.
- `DBMS_RLS.DROP_POLICY` and `ENABLE_POLICY` manage existing policies. DBMS_RLS procedures commit current DML
  first (except inside a DDL event trigger).

## Exemptions and checks
- `SYS` is free of security policies, and policies do not apply to users with the `EXEMPT ACCESS POLICY` system
  privilege.
- `V$VPD_POLICIES` shows current cursors and their predicates.

## Verify
After setting the context for a session, a query on the protected table returns only the matching rows, and
`V$VPD_POLICIES` shows the applied predicate for the cursor.

## Checked
2026-11-09. Read the 19c `DBMS_RLS` reference (overview, operational notes, `ADD_POLICY` parameters and policy-type
table, usage notes). The second source (`dbseg` Using Oracle VPD, a 1228-character landing page) gave no content and
was dropped. Removed because the cited page does not state them: the application-context creation package and
`DBMS_SESSION.SET_CONTEXT` setup, the logon trigger advice, fail-closed `1=0` pattern, cursor-sharing remark,
Enterprise Edition note, `ORA-28113`, Data Pump export filtering, indexing advice and multitenant tags. The policy
function body and names are illustrative.
Method: documentation only; no commands were run.
