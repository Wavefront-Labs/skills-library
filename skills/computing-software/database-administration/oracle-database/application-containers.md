---
id: computing-software.database-administration.oracle-database.application-containers
name: application-containers
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, application-container, application-root, application-pdb, multitenant, saas, application-upgrade, sharing-metadata]
level: sme
status: docs-checked
description: "Use Oracle application containers for SaaS-style multitenancy: application root, application PDBs, shared objects, and install/upgrade/sync of application versions."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/multi/overview-of-applications-in-an-application-container.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/multi/administering-application-containers-with-sql-plus.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Application containers

An application root is a PDB that acts as a mini-CDB root for one application: its application
PDBs share the application's common objects (metadata-linked tables, code) defined once in the root.
Typical use: one application installed for many tenants, upgraded in one place.

## Create
```sql
-- in CDB root
CREATE PLUGGABLE DATABASE saas_root AS APPLICATION CONTAINER ADMIN USER appadm IDENTIFIED BY "<SECRET>";
ALTER PLUGGABLE DATABASE saas_root OPEN;
-- in the application root
ALTER SESSION SET CONTAINER = saas_root;
CREATE PLUGGABLE DATABASE tenant1 ADMIN USER t1adm IDENTIFIED BY "<SECRET>";
ALTER PLUGGABLE DATABASE tenant1 OPEN;
```
Database files must be Oracle Managed Files for `AS APPLICATION CONTAINER`. An application seed speeds new-tenant creation (see the guide for its syntax).
Without the Multitenant option a CDB may have up to 3 user-created PDBs (Licensing Information, all offerings); with it up to 252 on Enterprise Edition.

## Install an application version
```sql
ALTER SESSION SET CONTAINER = saas_root;
ALTER PLUGGABLE DATABASE APPLICATION sales BEGIN INSTALL '1.0';
CREATE USER sales_app IDENTIFIED BY "<SECRET>";      -- application common user
CREATE TABLE sales_app.products SHARING = DATA (id NUMBER PRIMARY KEY, name VARCHAR2(100));      -- rows shared by all
CREATE TABLE sales_app.orders SHARING = METADATA (id NUMBER PRIMARY KEY, product_id NUMBER);     -- structure shared, rows per tenant
CREATE TABLE sales_app.config SHARING = EXTENDED DATA (k VARCHAR2(30), v VARCHAR2(100));          -- shared rows + tenant rows
ALTER PLUGGABLE DATABASE APPLICATION sales END INSTALL '1.0';
-- in each application PDB (or all at once)
ALTER SESSION SET CONTAINER = tenant1;
ALTER PLUGGABLE DATABASE APPLICATION sales SYNC;
```

## Upgrade
```sql
ALTER PLUGGABLE DATABASE APPLICATION sales BEGIN UPGRADE '1.0' TO '1.1';
ALTER TABLE sales_app.orders ADD (qty NUMBER);
ALTER PLUGGABLE DATABASE APPLICATION sales END UPGRADE TO '1.1';
```
Oracle clones the root to keep the old version for PDBs not yet synced; tenants sync on their own schedule.
Patches do not clone the root: `ALTER PLUGGABLE DATABASE APPLICATION sales BEGIN PATCH 101 MINIMUM VERSION '1.0';` ... `END PATCH 101;`.
`SYNC TO '<version>'` or `SYNC TO PATCH n` syncs to a specific point; `APPLICATION ALL SYNC` does not accept `SYNC TO`.

## Cross-tenant queries
`CONTAINERS()` from the application root queries a metadata-linked table across all application PDBs:
```sql
SELECT con_id, COUNT(*) FROM CONTAINERS(sales_app.orders) GROUP BY con_id;
```
Container maps route queries by a partitioning key: create a table partitioned BY LIST/HASH/RANGE whose partition names equal the application PDB names, run `ALTER PLUGGABLE DATABASE SET CONTAINER_MAP='schema.map_table';` in the application root (one map per application container), then inside an install block `ALTER TABLE t ENABLE CONTAINER_MAP;`. The map is not updated when PDBs are renamed or dropped.

## Inspect
```sql
SELECT app_name, app_version, app_status FROM dba_applications;
SELECT con_uid, app_name, app_version, app_status FROM dba_app_pdb_status;
SELECT statement_id, app_name, app_status, app_statement FROM dba_app_statements ORDER BY statement_id;   -- captured statements
```

## Gotchas
- Only statements run between BEGIN/END are captured and replayed on sync; DDL outside them is local to the root.

## Verify
`dba_app_pdb_status` shows every tenant at the expected version.

## Checked
Date 2026-10-22. Oracle Database 19c Multitenant Administrator's Guide (Administering Application Containers) and
Database Reference; Licensing Information User Manual 19c. Confirmed: BEGIN/END INSTALL, UPGRADE, PATCH and SYNC syntax,
that an upgrade clones the application root and a patch does not, SHARING values (METADATA default, DATA, EXTENDED DATA,
NONE), CONTAINER_MAP setup, CONTAINERS() clause, columns of DBA_APPLICATIONS, DBA_APP_PDB_STATUS and
DBA_APP_STATEMENTS, the 3-PDB licence limit. Removed unconfirmed gotchas on common users and unplugging. Sources
updated: the old creating-and-removing page returns 404.
Method: documentation only; no commands were run.
