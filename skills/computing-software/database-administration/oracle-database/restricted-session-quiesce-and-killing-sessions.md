---
id: computing-software.database-administration.oracle-database.restricted-session-quiesce-and-killing-sessions
name: restricted-session-quiesce-and-killing-sessions
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, kill-session, restricted-session, quiesce, disconnect-session, blocking-sessions, maintenance]
level: practitioner
status: docs-checked
description: "Control Oracle access for maintenance: restricted session, quiesce, and killing or disconnecting sessions safely (including RAC and stuck KILLED sessions)."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/admin/managing-processes.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/admin/starting-up-and-shutting-down.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Restricted session, quiesce, and killing sessions

## Restricted session
Only users with `RESTRICTED SESSION` (DBAs) can connect; existing sessions stay.
```sql
ALTER SYSTEM ENABLE RESTRICTED SESSION;     -- or STARTUP RESTRICT
-- maintenance
ALTER SYSTEM DISABLE RESTRICTED SESSION;
SELECT logins FROM v$instance;              -- RESTRICTED / ALLOWED
```
Per PDB: `ALTER PLUGGABLE DATABASE pdb1 OPEN RESTRICTED FORCE;`.

## Quiesce
Lets active non-DBA transactions finish, then holds new non-DBA work (sessions wait, not error).
```sql
ALTER SYSTEM QUIESCE RESTRICTED;
SELECT active_state FROM v$instance;   -- QUIESCING -> QUIESCED
ALTER SYSTEM UNQUIESCE;
```
Use for short DBA actions that need no concurrent application activity.

## Find the session
```sql
SELECT s.inst_id, s.sid, s.serial#, s.username, s.status, s.program, s.machine, s.sql_id,
       s.event, s.blocking_session, s.last_call_et, p.spid
FROM gv$session s JOIN gv$process p ON p.addr = s.paddr AND p.inst_id = s.inst_id
WHERE s.username = 'APPUSER' ORDER BY s.last_call_et DESC;
```
Blocking tree: sessions with `blocking_session` set; kill the root blocker, not the waiters.

## Kill or disconnect
```sql
ALTER SYSTEM KILL SESSION '123,45678' IMMEDIATE;          -- local instance
ALTER SYSTEM KILL SESSION '123,45678,@2' IMMEDIATE;       -- RAC instance 2
ALTER SYSTEM CANCEL SQL '123,45678';                      -- cancel the statement, keep the session
```
Killing rolls back the transaction: a large update can take as long to roll back as it ran.

Session stuck in `KILLED` status with its process alive: find `spid` and kill the OS process
using the operating system; the database then cleans up. Never kill
background processes.

## Gotchas
- Connection pools reconnect immediately; disable the app/service first (`srvctl stop service` or `DBMS_SERVICE.STOP_SERVICE`) for real maintenance windows.
- Granting `ALTER SYSTEM` to let developers kill sessions gives far more power; wrap kills in a definer-rights procedure that checks the target username.

## Verify
After maintenance `logins` is ALLOWED, `active_state` NORMAL, and application services are running.

## Checked

2026-10-28. Confirmed against the cited Oracle documentation: ENABLE/DISABLE RESTRICTED SESSION, ALTER SYSTEM QUIESCE RESTRICTED and the V$INSTANCE ACTIVE_STATE values, ALTER SYSTEM KILL SESSION, ALTER SYSTEM CANCEL SQL, DBMS_SERVICE.STOP_SERVICE (Administrator Guide, Managing Processes and Starting Up and Shutting Down).

Removed or corrected: ORA-12526 listener claim, the Resource Manager prerequisite, DISCONNECT SESSION POST_TRANSACTION, rollback-progress query and SMON remark, orakill/kill -9 specifics (not found in the cited pages).

Method: documentation only; no commands were run.
