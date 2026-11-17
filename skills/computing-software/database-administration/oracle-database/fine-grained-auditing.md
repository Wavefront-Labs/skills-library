---
id: computing-software.database-administration.oracle-database.fine-grained-auditing
name: fine-grained-auditing
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle-security, fine-grained-auditing, dbms-fga, unified-auditing, sensitive-data, compliance]
level: practitioner
status: docs-checked
description: "Audit access to sensitive Oracle columns and rows with DBMS_FGA policies (condition, columns, statement types) and read the results from unified audit."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/arpls/DBMS_FGA.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fine-grained auditing (DBMS_FGA)

Standard/unified audit policies record that a statement ran against a table. FGA records it
only when the statement **touches specific columns and/or rows matching a condition**, and
can capture the SQL text and binds. Example: log any query that reads `salary` for executives.

## Create a policy
```sql
BEGIN
  DBMS_FGA.ADD_POLICY(
    object_schema   => 'HR',
    object_name     => 'EMPLOYEES',
    policy_name     => 'AUD_EXEC_SALARY',
    audit_condition => 'JOB_ID IN (''AD_PRES'',''AD_VP'')',   -- NULL = TRUE: audits even if no rows are processed; no AND/OR combinations
    audit_column    => 'SALARY,COMMISSION_PCT',
    audit_column_opts => DBMS_FGA.ANY_COLUMNS,                 -- or ALL_COLUMNS
    statement_types => 'SELECT,UPDATE',
    audit_trail     => DBMS_FGA.DB + DBMS_FGA.EXTENDED,        -- omit once migrated to unified auditing
    handler_schema  => 'SEC', handler_module => 'ALERT_PKG.NOTIFY',   -- optional callback
    enable          => TRUE);
END;
/
```
- `audit_column` defaults to NULL (any column). At most one audit record is generated per policy per
  statement, however many rows satisfy the condition.
- `audit_condition` is evaluated with the privileges of the user who creates the policy.
- The handler procedure can send alerts (keep it fast and non-failing).

## Read the results
After migration to unified auditing, FGA records are written to the unified audit trail
automatically (query `UNIFIED_AUDIT_TRAIL`; see the Database Reference for its columns). Before migration,
`audit_trail` chooses the destination: `DBMS_FGA.DB` writes to `SYS.FGA_LOG$`, `XML` to OS files under
`AUDIT_FILE_DEST`; `EXTENDED` adds SQL text and bind values.

## Manage
```sql
EXEC DBMS_FGA.DISABLE_POLICY('HR', 'EMPLOYEES', 'AUD_EXEC_SALARY');
EXEC DBMS_FGA.DROP_POLICY('HR', 'EMPLOYEES', 'AUD_EXEC_SALARY');
```
Plan retention and purging of audit records, or the trail grows without bound.

## Gotchas
- Test with your privileged accounts (DBA, ETL) to confirm their access is recorded the way the auditors expect.
- Heavy conditions on hot tables add overhead per execution; keep conditions simple.
- On read-only databases, records go to XML files regardless of `audit_trail`.

## Checked
2026-11-01. Confirmed on the 19c DBMS_FGA reference: ADD_POLICY parameters and defaults, NULL audit_condition, one record per policy per statement, audit_trail DB/XML/EXTENDED behaviour, unified auditing omission, read-only database XML fallback. Removed: unified trail column names, dba_audit_policies query, DBMS_AUDIT_MGMT, Enterprise Edition claim, SYS auditing and EXEMPT ACCESS POLICY remarks, flashback remark, unreadable audit-guide sources.
Method: documentation only; no commands were run.

## Verify
As a test user, `SELECT salary FROM hr.employees WHERE job_id = 'AD_PRES';` creates a record in the audit trail; a query on non-audited columns does not.
