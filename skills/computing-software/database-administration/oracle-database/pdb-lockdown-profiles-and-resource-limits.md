---
id: computing-software.database-administration.oracle-database.pdb-lockdown-profiles-and-resource-limits
name: pdb-lockdown-profiles-and-resource-limits
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, multitenant, pluggable-database, pdb-lockdown, lockdown-profile, cdb-resource-plan, resource-manager, max-iops, cpu-count-pdb, sga-target-pdb, noisy-neighbour]
level: advanced
status: draft
description: "Isolate Oracle PDBs with lockdown profiles (blocked statements, options, features) and CDB resource plans plus per-PDB CPU, memory and I/O limits."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/multi/using-pdb-lockdown-profiles-to-restrict-operations-on-pdbs.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/multi/using-oracle-resource-manager-for-pdbs-with-sql-plus.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PDB lockdown profiles and resource limits

**Goal:** a PDB admin (or a tenant app) cannot escape its PDB, and one busy PDB
cannot starve the others.

## Lockdown profiles (security isolation)
```sql
-- in CDB$ROOT
CREATE LOCKDOWN PROFILE tenant_lock;
ALTER LOCKDOWN PROFILE tenant_lock DISABLE STATEMENT = ('ALTER SYSTEM')
  CLAUSE = ('SET') OPTION ALL EXCEPT = ('open_cursors','optimizer_mode','cursor_sharing');
ALTER LOCKDOWN PROFILE tenant_lock DISABLE FEATURE = ('NETWORK_ACCESS');   -- UTL_HTTP, UTL_SMTP, UTL_TCP...
ALTER LOCKDOWN PROFILE tenant_lock DISABLE FEATURE = ('OS_ACCESS');        -- UTL_FILE, external procs, Java OS
ALTER LOCKDOWN PROFILE tenant_lock DISABLE OPTION = ('PARTITIONING');      -- license control
ALTER LOCKDOWN PROFILE tenant_lock DISABLE STATEMENT = ('ALTER DATABASE') CLAUSE = ('ENABLE FORCE LOGGING');
-- apply to one PDB (connected to it) or as default for all PDBs (in root)
ALTER SESSION SET CONTAINER = sales;
ALTER SYSTEM SET pdb_lockdown = tenant_lock;
SELECT profile_name, rule_type, rule, clause, clause_option, status FROM cdb_lockdown_profiles;
```
Notes: lockdown applies to users inside the PDB including local `SYSDBA`-like admins;
common users connected in root are not affected. Built-in profiles
`PRIVATE_DBAAS`, `SAAS`, `PUBLIC_DBAAS` (18c+) are starting points. 19c+ supports
profiles in application roots and `CREATE LOCKDOWN PROFILE ... FROM <base>` (static copy)
or `INCLUDING <base>` (dynamic inheritance).

## Per-PDB parameters (19c)
```sql
ALTER SESSION SET CONTAINER = sales;
ALTER SYSTEM SET cpu_count = 4;               -- instance caging per PDB (needs a resource plan in root)
ALTER SYSTEM SET sga_target = 8G;             -- guaranteed-ish share; also sga_min_size
ALTER SYSTEM SET pga_aggregate_limit = 4G;
ALTER SYSTEM SET max_iops = 5000;             -- I/O caps (Exadata uses IORM instead)
ALTER SYSTEM SET max_mbps = 400;
ALTER SYSTEM SET sessions = 300;
ALTER PLUGGABLE DATABASE STORAGE (MAXSIZE 500G);   -- space cap for the PDB's datafiles
```

## CDB resource plan (shares + utilization limits)
```sql
BEGIN
  DBMS_RESOURCE_MANAGER.CREATE_PENDING_AREA;
  DBMS_RESOURCE_MANAGER.CREATE_CDB_PLAN(plan => 'cdb_plan', comment => 'tenants');
  DBMS_RESOURCE_MANAGER.CREATE_CDB_PLAN_DIRECTIVE(plan => 'cdb_plan', pluggable_database => 'sales',
     shares => 3, utilization_limit => 70, parallel_server_limit => 50);
  DBMS_RESOURCE_MANAGER.CREATE_CDB_PLAN_DIRECTIVE(plan => 'cdb_plan', pluggable_database => 'hr',
     shares => 1, utilization_limit => 30);
  DBMS_RESOURCE_MANAGER.UPDATE_CDB_DEFAULT_DIRECTIVE(plan => 'cdb_plan', new_shares => 1, new_utilization_limit => 50);
  DBMS_RESOURCE_MANAGER.VALIDATE_PENDING_AREA;
  DBMS_RESOURCE_MANAGER.SUBMIT_PENDING_AREA;
END;
/
ALTER SYSTEM SET resource_manager_plan = 'cdb_plan';   -- in root
```
Shares decide CPU split under contention; utilization_limit is a hard cap. 12.2+
performance profiles (`CREATE_CDB_PROFILE_DIRECTIVE` + `DB_PERFORMANCE_PROFILE` in the
PDB) let you define tiers (gold/silver) instead of per-PDB directives.

## Monitor
`V$RSRCPDBMETRIC` / `V$RSRCPDBMETRIC_HISTORY` (CPU, I/O, throttling per PDB);
wait event `resmgr:cpu quantum` = sessions being throttled by the plan.

## Verify
- [ ] From a PDB admin session, `ALTER SYSTEM SET` on a blocked parameter raises ORA-01031.
- [ ] `resource_manager_plan` set in root; each PDB's limits visible in `V$RSRCPDBMETRIC`.
