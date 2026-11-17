---
id: computing-software.database-administration.oracle-database.database-resource-manager-plans
name: database-resource-manager-plans
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, resource-manager-plan, dbms-resource-manager, consumer-groups, cdb-resource-plan, cpu-management, runaway-queries]
level: advanced
status: docs-checked
description: "Allocate Oracle CPU and limit runaway work with Database Resource Manager: consumer groups, mapping rules, plan directives, CDB plans for PDB shares, and monitoring."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/admin/managing-resources-with-oracle-database-resource-manager.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/multi/using-oracle-resource-manager-for-pdbs-with-sql-plus.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Database Resource Manager plans

## Build a plan (inside a PDB or non-CDB)
```sql
BEGIN
  DBMS_RESOURCE_MANAGER.CREATE_PENDING_AREA;
  DBMS_RESOURCE_MANAGER.CREATE_CONSUMER_GROUP('OLTP',    'online users');
  DBMS_RESOURCE_MANAGER.CREATE_CONSUMER_GROUP('REPORTS', 'reporting');
  DBMS_RESOURCE_MANAGER.CREATE_PLAN('DAYTIME', 'business hours');
  DBMS_RESOURCE_MANAGER.CREATE_PLAN_DIRECTIVE('DAYTIME', 'OLTP',    mgmt_p1 => 70);
  DBMS_RESOURCE_MANAGER.CREATE_PLAN_DIRECTIVE('DAYTIME', 'REPORTS', mgmt_p1 => 20,
     parallel_degree_limit_p1 => 4,
     switch_group => 'CANCEL_SQL', switch_time => 1800, switch_estimate => TRUE);   -- cancel > 30 min (estimated)
  DBMS_RESOURCE_MANAGER.CREATE_PLAN_DIRECTIVE('DAYTIME', 'OTHER_GROUPS', mgmt_p1 => 10);
  -- mapping: who lands where
  DBMS_RESOURCE_MANAGER.SET_CONSUMER_GROUP_MAPPING(DBMS_RESOURCE_MANAGER.ORACLE_USER, 'APP_OLTP', 'OLTP');
  DBMS_RESOURCE_MANAGER.SET_CONSUMER_GROUP_MAPPING(DBMS_RESOURCE_MANAGER.SERVICE_NAME, 'REPORTING_SVC', 'REPORTS');
  DBMS_RESOURCE_MANAGER.VALIDATE_PENDING_AREA;
  DBMS_RESOURCE_MANAGER.SUBMIT_PENDING_AREA;
END;
/
EXEC DBMS_RESOURCE_MANAGER_PRIVS.GRANT_SWITCH_CONSUMER_GROUP('APP_OLTP', 'OLTP', FALSE);
EXEC DBMS_RESOURCE_MANAGER_PRIVS.GRANT_SWITCH_CONSUMER_GROUP('PUBLIC', 'REPORTS', FALSE);
ALTER SYSTEM SET resource_manager_plan = 'DAYTIME' SCOPE = BOTH;
```
Every plan must include `OTHER_GROUPS`. Users need switch privilege on a group for the mapping to apply.
Mapping by service is the cleanest: route reporting connections to a reporting service.
Other directive limits: `utilization_limit` (hard CPU cap), `active_sess_pool_p1` (queue sessions),
`max_idle_time`, `switch_io_megabytes`, `session_pga_limit` (megabytes per session; `ORA-10260` when exceeded).

## CDB plan: shares between PDBs
```sql
-- in CDB root
BEGIN
  DBMS_RESOURCE_MANAGER.CREATE_PENDING_AREA;
  DBMS_RESOURCE_MANAGER.CREATE_CDB_PLAN('CDB_PLAN', 'PDB shares');
  DBMS_RESOURCE_MANAGER.CREATE_CDB_PLAN_DIRECTIVE('CDB_PLAN', 'SALES', shares => 3, utilization_limit => 80, parallel_server_limit => 50);
  DBMS_RESOURCE_MANAGER.CREATE_CDB_PLAN_DIRECTIVE('CDB_PLAN', 'HR',    shares => 1, utilization_limit => 40);
  DBMS_RESOURCE_MANAGER.UPDATE_CDB_DEFAULT_DIRECTIVE('CDB_PLAN', new_shares => 1, new_utilization_limit => 50);
  DBMS_RESOURCE_MANAGER.VALIDATE_PENDING_AREA;
  DBMS_RESOURCE_MANAGER.SUBMIT_PENDING_AREA;
END;
/
ALTER SYSTEM SET resource_manager_plan = 'CDB_PLAN';
```
Simpler: set `cpu_count` / `cpu_min_count` per PDB (`ALTER SYSTEM SET cpu_count = 4` inside the PDB) with a CDB plan active.

## Monitor
```sql
SELECT name, active_sessions, execution_waiters, requests, consumed_cpu_time, cpu_waits, cpu_wait_time
FROM v$rsrc_consumer_group;
SELECT sid, resource_consumer_group FROM v$session WHERE username IS NOT NULL;
SELECT * FROM v$rsrc_plan_history ORDER BY start_time DESC;
```
`V$RSRC_CONSUMER_GROUP` shows `cpu_waits` and `cpu_wait_time`: time sessions were throttled by the plan (expected under load, a problem if OLTP shows it).

## Gotchas
- Scheduler maintenance windows can activate their own plan (`DEFAULT_MAINTENANCE_PLAN` is the supplied one), replacing yours while the window is open.
- CPU management acts only when CPU is saturated, except `utilization_limit`.
- Check `dba_scheduler_windows` to see which windows switch plans and when.

## Verify
Sessions map to the intended groups, and under contention OLTP's `cpu_wait_time` stays low while REPORTS absorbs waits.

## Checked
2026-10-31. Confirmed in the 19c Administrator's Guide (Managing Resources with Database Resource
Manager), Multitenant Administrator's Guide (Resource Manager for PDBs) and Database Reference
(`V$RSRC_CONSUMER_GROUP`, `V$RSRC_PLAN_HISTORY`): the `OTHER_GROUPS` requirement, directive names
(`switch_group`, `switch_time`, `switch_estimate`, `session_pga_limit`), CDB plan procedures and
`shares` / `utilization_limit`, `cpu_count` per PDB, `DEFAULT_MAINTENANCE_PLAN`, monitoring views.
Removed: "18c+" and "12.2+" version gates, the `resmgr:cpu quantum` wait event and the `FORCE:` plan
claim (not found in the fetched pages). Group, user and service names are examples.
Method: documentation only; no commands were run.
