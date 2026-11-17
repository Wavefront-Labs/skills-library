---
id: computing-software.database-administration.oracle-database.common-and-local-users
name: common-and-local-users
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, multitenant, pluggable-database, common-users, local-users, common-user-prefix, container-all, container-data, common-roles, oracle-users]
level: practitioner
status: docs-checked
description: "Create and grant Oracle common and local users and roles correctly across CDB and PDBs, including C## prefix rules, CONTAINER clauses and CONTAINER_DATA."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/multi/managing-security-for-a-multitenant-environment.html
  - https://docs.oracle.com/en/error-help/db/ora-65096/
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/multi/overview-of-the-multitenant-architecture.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Common and local users

## Definitions
- **Common user**: exists with the same identity in root and every PDB (current and
  future). Created in `CDB$ROOT`; name must start with `COMMON_USER_PREFIX` (default
  `C##`). Existing Oracle-supplied names are exempt (the guide says so for roles such as DBA and RESOURCE; `DBA_USERS.COMMON`/`ORACLE_MAINTAINED` show which accounts are Oracle's).
- **Local user**: exists in one PDB only; created while connected to that PDB; name
  must **not** start with the common prefix. Application schemas are local users.
- Privileges are granted commonly (`CONTAINER=ALL`, in root) or locally (in one PDB).
  A common user has no access to a PDB until granted `CREATE SESSION` there or commonly.

## Create
```sql
-- root
CREATE USER c##dba_ops IDENTIFIED BY "<pw>" CONTAINER = ALL;
GRANT CREATE SESSION, SELECT ANY DICTIONARY TO c##dba_ops CONTAINER = ALL;
GRANT SYSDBA TO c##dba_ops CONTAINER = ALL;          -- if needed
CREATE ROLE c##monitoring CONTAINER = ALL;
GRANT SELECT_CATALOG_ROLE TO c##monitoring CONTAINER = ALL;

-- in one PDB
ALTER SESSION SET CONTAINER = sales;
CREATE USER app_owner IDENTIFIED BY "<pw>" DEFAULT TABLESPACE users QUOTA UNLIMITED ON users;
GRANT CREATE SESSION, CREATE TABLE, CREATE VIEW, CREATE PROCEDURE TO app_owner;
GRANT CREATE SESSION TO c##dba_ops;                  -- local grant of a privilege to a common user
```
Name the container explicitly. Creating a local user or role while connected to the root or an application root fails with `ORA-65049` ("Creation of local user or role is not allowed in this container"); create it in a PDB, or add `CONTAINER=ALL` for a common one. In the root, `ALTER USER` defaults to `CONTAINER=ALL`, but `SET CONTAINER_DATA` must use `CONTAINER = CURRENT`.

## Seeing other containers' data: CONTAINER_DATA
A common user connected to the root sees data from other containers in container-data objects (for example `V$SESSION`) only for containers listed in the user's `CONTAINER_DATA` attribute. Omitting `FOR <object>` applies the setting to all container-data objects the user can access:
```sql
ALTER USER c##hr_admin SET CONTAINER_DATA = (CDB$ROOT, SALES, HR) FOR V$SESSION CONTAINER = CURRENT;
SELECT username, default_attr, owner, object_name, all_containers, container_name FROM cdb_container_data;
```
Monitoring agents connected to the root need this to see other PDBs' rows. (The `CONTAINER_DATA` initialization parameter is a different setting.)

## Listing
```sql
SELECT username, common, con_id, oracle_maintained FROM cdb_users WHERE oracle_maintained = 'N' ORDER BY con_id;
SELECT grantee, privilege, common, con_id FROM cdb_sys_privs WHERE grantee LIKE 'C##%';
```

## Gotchas
- `ORA-65096`: a common user or role name must start with `COMMON_USER_PREFIX` (default `C##`). Connect to the PDB for local users.
- `ORA-65049`: a local user/role was created in the root; see Create above.
- Application containers add application common users, created in the application root.
- Do not create application objects in common users' schemas; they appear in every PDB.

## Verify
- [ ] No application schemas in `CDB$ROOT`; app users are local in their PDB.
- [ ] Monitoring common users have `CONTAINER_DATA` set and see all PDBs' sessions.
- [ ] Common users/roles are prefixed and documented.

## Checked
Date 2026-10-22. Oracle Database 19c Multitenant Administrator's Guide (Managing Security for a Multitenant Environment),
Database Reference (DBA_USERS, DBA_SYS_PRIVS, DBA_CONTAINER_DATA) and Oracle error help (ORA-65096, ORA-65049).
Confirmed: COMMON_USER_PREFIX default C## and the exemption for Oracle-supplied roles, local roles must not use the prefix,
`ALTER USER ... SET CONTAINER_DATA ... FOR V$SESSION CONTAINER=CURRENT` form, ALTER USER default CONTAINER=ALL,
COMMON column of DBA_USERS / DBA_SYS_PRIVS, CDB_CONTAINER_DATA columns. Corrected: ORA-65049 means a local user/role was
created in the root (the skill described a PDB-not-open case). Removed unconfirmed: `SET CONTAINER_DATA = ALL`, CREATE USER
default container in root, `_ORACLE_SCRIPT`, common profile naming, "12.2+" and the list of unprefixed Oracle accounts.
Method: documentation only; no commands were run.
