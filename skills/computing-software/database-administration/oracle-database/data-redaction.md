---
id: computing-software.database-administration.oracle-database.data-redaction
name: data-redaction
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, data-redaction, dbms-redact, oracle-security, masking, advanced-security, exempt-redaction-policy]
level: advanced
status: docs-checked
description: "Mask sensitive Oracle column values at query time with DBMS_REDACT policies (full, partial, regexp, random), conditional expressions, and exemptions."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/asoag/configuring-oracle-data-redaction-policies.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/arpls/DBMS_REDACT.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Oracle Data Redaction

Redaction rewrites column values in query **results** for users the policy applies to; stored data
is unchanged. Part of the Advanced Security option (the 19c Licensing Information lists Data Redaction under Advanced Security; check it for your edition). Treat it as a display-layer control, not as a defence against users who can run ad hoc SQL.

## Full redaction
```sql
BEGIN
  DBMS_REDACT.ADD_POLICY(
    object_schema => 'HR', object_name => 'EMPLOYEES', policy_name => 'REDACT_SALARY',
    column_name => 'SALARY', function_type => DBMS_REDACT.FULL,
    expression => q'[SYS_CONTEXT('USERENV','SESSION_USER') != 'HR_PAYROLL']');
END;
/
```
Full redaction returns 0 for NUMBER columns and a single space for character columns; `DBMS_REDACT.UPDATE_FULL_REDACTION_VALUES` changes these database-wide (needs CREATE ANY TABLE and EXECUTE on DBMS_REDACT; takes effect after a restart, or after closing and reopening a PDB; current values are in `REDACTION_VALUES_FOR_TYPE_FULL`).
`expression => '1=1'` applies to everyone except SYS and users with EXEMPT REDACTION POLICY. Redaction applies only when the expression is TRUE; comparisons with NULL tend to be FALSE, so check nulls explicitly. Allowed operators: AND, OR, IN, NOT IN, =, !=, <>, <, >, >=, <=; user-created functions are not permitted; check roles with `SYS_CONTEXT('SYS_SESSION_ROLES', 'ROLE')`.

## Partial and regexp
```sql
BEGIN
  DBMS_REDACT.ALTER_POLICY(
    object_schema => 'HR', object_name => 'EMPLOYEES', policy_name => 'REDACT_SALARY',
    action => DBMS_REDACT.ADD_COLUMN, column_name => 'CARD_NO',
    function_type => DBMS_REDACT.PARTIAL,
    function_parameters => 'VVVVFVVVVFVVVVFVVVV,VVVV-VVVV-VVVV-VVVV,*,1,12');  -- show last 4
  DBMS_REDACT.ALTER_POLICY(
    object_schema => 'HR', object_name => 'EMPLOYEES', policy_name => 'REDACT_SALARY',
    action => DBMS_REDACT.ADD_COLUMN, column_name => 'EMAIL',
    function_type => DBMS_REDACT.REGEXP,
    regexp_pattern => '<pattern>',
    regexp_replace_string => '<replacement>');
END;
/
```
For `REGEXP`, supply `regexp_pattern`, `regexp_replace_string` and optionally `regexp_position`, `regexp_occurrence`, `regexp_match_parameter`; the Advanced Security guide lists predefined pattern constants. `function_type` values: NONE, FULL, PARTIAL, RANDOM, REGEXP, NULLIFY, REGEXP_WIDTH.
Partial format is five comma-separated fields: input format, output format, mask character, mask-from, mask-to (the reference's example masks the first 5 digits of an SSN: `VVVFVVFVVVV,VVV-VV-VVVV,X,1,5`).
Only one policy can be defined on a table or view (a second one can go on a new view); add columns with `ALTER_POLICY` (actions ADD_COLUMN, DROP_COLUMN, MODIFY_EXPRESSION, MODIFY_COLUMN, SET_POLICY_DESCRIPTION, SET_COLUMN_DESCRIPTION). Named policy expressions (`CREATE_POLICY_EXPRESSION` then `APPLY_POLICY_EXPR_TO_COL`) take precedence over the inline expression; creating them needs CREATE ANY TABLE from 19c RU 19.32.

## Exemptions
```sql
GRANT EXEMPT REDACTION POLICY TO etl_user;   -- sees real data
```
SYS and users with `EXEMPT REDACTION POLICY` bypass all policies, so their results are not redacted.

## Inspect
```sql
SELECT * FROM redaction_policies;
SELECT * FROM redaction_columns;
SELECT * FROM redaction_expressions;   -- named policy expressions
```

## Gotchas
- Expressions may use `SYS_CONTEXT('USERENV', ...)` and `SYS_CONTEXT('SYS_SESSION_ROLES', ...)`; user-created functions are not allowed.
- Pair with VPD for row restriction and auditing for access records.

## Verify
Query the table as the application user (redacted values) and as an exempt user (real values).

## Checked
Date 2026-10-22. Oracle Database 19c PL/SQL Packages Reference (DBMS_REDACT), Advanced Security Guide (configuring
redaction policies, first 100,000 characters) and Licensing Information. Confirmed: ADD_POLICY signature, function_type
values, ALTER_POLICY actions, partial-redaction parameter format, UPDATE_FULL_REDACTION_VALUES, named policy expressions,
SYS and EXEMPT REDACTION POLICY bypass, one policy per table or view, expression rules, default full-redaction values for
NUMBER and character, views REDACTION_POLICIES / REDACTION_EXPRESSIONS / REDACTION_VALUES_FOR_TYPE_FULL. Removed (not in
the pages read): the 01-JAN-01 date default, predefined constants (RE_PATTERN_EMAIL_ADDRESS, REDACT_US_SSN_F5 etc.),
all ORA-28081 and Data Pump/CTAS behaviour, the 12.2 gate, and column lists for REDACTION_POLICIES / REDACTION_COLUMNS.
The credit-card partial format in the example follows the documented five-field pattern but is not itself an
Oracle example.
Method: documentation only; no commands were run.
