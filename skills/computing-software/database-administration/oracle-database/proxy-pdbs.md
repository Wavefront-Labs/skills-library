---
id: computing-software.database-administration.oracle-database.proxy-pdbs
name: proxy-pdbs
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, proxy-pdb, multitenant, location-transparency, database-link, pdb-relocation]
level: advanced
status: docs-checked
description: "Create Oracle proxy PDBs that forward SQL to a PDB in another CDB, for location transparency during relocation or to aggregate access, and know their limits."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/multi/creating-a-pdb-as-a-proxy-pdb.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/CREATE-PLUGGABLE-DATABASE.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxy PDBs

A proxy PDB lives in a local CDB but holds no user data: SQL issued in it is executed in the
**referenced PDB** in another (or the same) CDB. Clients connect locally; the data lives elsewhere.
Uses: keep connection strings stable after moving a PDB, expose a remote PDB inside an
application container, or reach a PDB across network zones through one CDB.

## Create
In the local CDB root, a database link to the remote CDB root or to the remote PDB (the link user
needs `CREATE PLUGGABLE DATABASE` and common-user rights there):
```sql
CREATE PUBLIC DATABASE LINK lnk_remote CONNECT TO c##proxyadm IDENTIFIED BY "<SECRET>" USING 'remotehost:1521/CDB2';
CREATE PLUGGABLE DATABASE sales_px AS PROXY FROM sales@lnk_remote;
ALTER PLUGGABLE DATABASE sales_px OPEN;
```

## Use
```sql
ALTER SESSION SET CONTAINER = sales_px;
SELECT COUNT(*) FROM sales_app.orders;   -- runs on the referenced PDB
```
`ALTER SESSION SET CONTAINER` into the proxy, or connecting to its service, is all a client needs.

## Gotchas
- Extra network round trip per call: latency-sensitive OLTP pays for it.
- Opening the proxy fails if the referenced PDB is closed or the listener unreachable.

## Verify
The proxy PDB opens, and a query run inside it returns data from the referenced PDB.

## Checked

2026-10-28. Confirmed against the cited Oracle documentation: CREATE PLUGGABLE DATABASE ... AS PROXY FROM, the term referenced PDB (Multitenant guide, administering PDBs and the CREATE PLUGGABLE DATABASE reference).

Removed or corrected: which tablespaces are copied, HOST/PORT clause on create, DML/DDL forwarding details, relocation pattern with AVAILABILITY MAX, IS_PROXY_PDB and V$PROXY_PDB_TARGETS, PDB-limit licensing remark (not found in the cited pages).

Method: documentation only; no commands were run.
