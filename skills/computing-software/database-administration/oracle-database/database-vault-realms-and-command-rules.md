---
id: computing-software.database-administration.oracle-database.database-vault-realms-and-command-rules
name: database-vault-realms-and-command-rules
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, database-vault, realms, command-rules, separation-of-duty, dvsys, oracle-security, simulation-mode]
level: sme
status: docs-checked
description: "Protect Oracle application data from privileged users with Database Vault: roles, realms and mandatory realms, command rules, and simulation mode."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/dvadm/introduction-to-oracle-database-vault.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/dvadm/configuring-realms.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/dvadm/configuring-command-rules.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Database Vault realms and command rules

Database Vault enforces separation of duty and protects application data from privileged users.

## Roles and enabling
- `DV_OWNER` and `DV_ADMIN` create and manage Database Vault policies; `DV_ACCTMGR` manages user accounts. At
  configuration, `DV_OWNER` goes to a user who must already exist, and `DV_ACCTMGR` to a second, optional existing
  user. Create and maintain backup accounts for both (the guide strongly recommends it). Grant the roles to others
  only if trusted.
- Database Vault objects live in the `DVSYS` and `DVF` schemas. In a multitenant database `DVSYS` is a common user
  schema stored in the CDB root.
- Enable in the CDB with `EXEC DBMS_MACADM.ENABLE_DV;` (regular mode, same as `strict_mode => 'n'`) or
  `strict_mode => 'y'`, where PDBs without Database Vault run in restricted mode until it is configured and enabled
  there or strict mode is disabled. You must configure and enable Database Vault on each PDB that is to use it.
- Operations control, enabled from the CDB, can keep container users out of non-Oracle-maintained schema data in
  all PDBs without enabling Database Vault in them.

## Realms
A realm protects objects (a schema, tables, indexes or roles) from system-privilege-based access. A regular realm
still allows the object owner and object-privilege holders; a **mandatory realm** blocks both system- and
object-privilege access, so even the owner needs realm authorization. With several mandatory realms on one object
you must be authorized in all of them.
```sql
-- protect all current and future tables of a schema in a realm
BEGIN
  DBMS_MACADM.ADD_OBJECT_TO_REALM('realm_name', 'schema_name', '%', 'TABLE');
END;
/
```
- Realm protection is not restored if a protected table, index or role is dropped and recreated; the `%` form above
  covers future tables in the schema.
- A realm does not protect a table if access is granted to `PUBLIC` (unless it is mandatory); revoke unneeded
  `PUBLIC` privileges.
- A role created for the first time by SYS or SYSTEM is implicitly granted to the creator, which can make a realm
  authorization of that role accidentally broad.
- To relax a realm for an admin task, add the named account to the realm's authorized accounts and enable auditing
  on the authorization rule set, rather than disabling the realm; remove it afterwards.
- Realm status can be Enabled, Disabled or **Simulation**. Simulation enables the realm without enforcing it and
  writes violations to a log; `DV_OWNER` or `DV_ADMIN` can query `DBA_DV_SIMULATION_LOG`.
- A common realm protects only objects in the application root, not local PDB objects.

## Command rules
A command rule ties a SQL command (for example `ALTER TABLE`, or `CONNECT` events) to a rule set that must evaluate
true; the guide's examples include allowing DDL in a schema only after business hours. Rules, rule sets and command
rules are created with `DBMS_MACADM`. The guide's example for `ALTER SYSTEM SET ... SECURITY RESTRICTED SESSION`:
```sql
EXEC DBMS_MACADM.CREATE_RULE('RESTRICTED SESSION TRUE', 'UPPER(PARAMETER_VALUE) = ''TRUE''');
BEGIN
  DBMS_MACADM.CREATE_RULE_SET(rule_set_name => 'Check RESTRICTED SESSION for TRUE',
    description => 'Checks if restricted session is true', enabled => DBMS_MACUTL.G_YES,
    eval_options => DBMS_MACUTL.G_RULESET_EVAL_ALL,
    audit_options => DBMS_MACUTL.G_RULESET_AUDIT_FAIL + DBMS_MACUTL.G_RULESET_AUDIT_SUCCESS,
    fail_options => DBMS_MACUTL.G_RULESET_FAIL_SILENT, fail_message => 'RESTRICTED SESSION is not TRUE',
    fail_code => 20461, handler_options => DBMS_MACUTL.G_RULESET_HANDLER_FAIL, handler => '', is_static => false);
END;
/
EXEC DBMS_MACADM.ADD_RULE_TO_RULE_SET('Check RESTRICTED SESSION for TRUE', 'RESTRICTED SESSION TRUE');
BEGIN
  DBMS_MACADM.CREATE_COMMAND_RULE(command => 'ALTER SYSTEM', rule_set_name => 'Check RESTRICTED SESSION for TRUE',
    object_owner => '%', object_name => '%', enabled => DBMS_MACUTL.G_YES,
    clause_name => 'SECURITY', parameter_name => 'RESTRICTED SESSION', scope => DBMS_MACUTL.G_SCOPE_LOCAL);
END;
/
```
- For `ALTER SESSION`/`ALTER SYSTEM` command rules `object_owner` and `object_name` must be `%`. In a multitenant
  database create the rule set and rule in the same place as the command rule (application root or the PDB).
- `enabled` can also select simulation mode, which logs violations (user, SQL statement) to a log table. To
  temporarily relax an enabled command rule, switch it to simulation mode: it logs only activity that would have
  violated the rule.
- `SELECT`, `INSERT`, `UPDATE`, `DELETE` and `EXECUTE` command rules are not allowed for all (`%`) or the `SYS`
  and `DVSYS` schemas.

## Verify
Test new realms and command rules in simulation mode first, review `DBA_DV_SIMULATION_LOG`, then enable.

## Checked
2026-11-09. Read the 19c Database Vault Administrator's Guide pages for the introduction (roles, `DVSYS`,
multitenant and `ENABLE_DV` modes), configuring realms (mandatory realms, authorization, simulation, tips) and
configuring command rules (`CREATE_COMMAND_RULE` example and parameters, simulation). Searched by claim rather than
reading every line. Removed because the pages do not state them: the `CONFIGURE_DV` account creation steps, the
"SYS can no longer create users" claim, the licensing note, the `CREATE_REALM`/`ADD_AUTH_TO_REALM` call listing, the
host-based deploy rule example, the Data Pump, scheduler and patch authorization procedures, the `dba_dv_status`
check and the ORA-01031 verification.
Method: documentation only; no commands were run.
