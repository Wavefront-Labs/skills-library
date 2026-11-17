---
id: computing-software.database-administration.oracle-database.sql-loader-and-external-tables
name: sql-loader-and-external-tables
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, data-pump, sql-loader, sqlldr, external-tables, oracle-loader, control-file, direct-path-load, bad-file, express-mode, csv-load, oracle-datapump-driver]
level: practitioner
status: draft
description: "Load flat files into Oracle with SQL*Loader control files (conventional or direct path) or query them as external tables, with bad and discard file handling."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/sutil/oracle-sql-loader.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/sutil/oracle-external-tables-concepts.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SQL*Loader and external tables

## SQL*Loader control file
```
-- orders.ctl
OPTIONS (SKIP=1, ERRORS=100, DIRECT=TRUE, PARALLEL=FALSE)
LOAD DATA
CHARACTERSET AL32UTF8
INFILE '/data/in/orders_20261016.csv'
BADFILE '/data/bad/orders.bad'
DISCARDFILE '/data/bad/orders.dsc'
APPEND                                   -- INSERT (empty only) | APPEND | REPLACE | TRUNCATE
INTO TABLE app.orders
WHEN (status != 'TEST')                  -- rows not matching go to the discard file
FIELDS CSV WITH EMBEDDED                 -- 12c+: handles quotes and embedded newlines
TRAILING NULLCOLS
( order_id,
  customer_id,
  order_date   DATE "YYYY-MM-DD HH24:MI:SS",
  amount       "TO_NUMBER(:amount, '999999.99')",
  status,
  notes        CHAR(4000),               -- default CHAR(255): longer values are rejected
  load_ts      SYSDATE )
```
```bash
sqlldr app@pdb1 control=orders.ctl log=orders.log
```
- Exit codes: 0 success, 2 warning (some rows rejected/discarded), 1 failure, 3 fatal.
  Scripts must treat 2 as "check the bad file".
- **Direct path** (`DIRECT=TRUE`) formats blocks above the HWM: much faster, but locks
  the table, skips insert triggers, enforces only NOT NULL/PK/unique (FKs and checks are
  disabled then re-enabled), and leaves indexes UNUSABLE if it fails mid-way. Use
  conventional path for small loads into busy tables.
- Express mode: `sqlldr app@pdb1 TABLE=orders` loads `orders.dat` with defaults (CSV, all columns), and writes a control file you can edit.

## External tables
Query the file in place with SQL; transform and load with `INSERT /*+ APPEND */ ... SELECT`.
```sql
CREATE DIRECTORY ext_in AS '/data/in';
CREATE DIRECTORY ext_bad AS '/data/bad';
GRANT READ ON DIRECTORY ext_in TO app;  GRANT WRITE ON DIRECTORY ext_bad TO app;
CREATE TABLE app.orders_ext (
  order_id NUMBER, customer_id NUMBER, order_date VARCHAR2(19), amount NUMBER, status VARCHAR2(10))
ORGANIZATION EXTERNAL (
  TYPE ORACLE_LOADER DEFAULT DIRECTORY ext_in
  ACCESS PARAMETERS (
    RECORDS DELIMITED BY NEWLINE CHARACTERSET AL32UTF8 SKIP 1
    BADFILE ext_bad:'orders_%p.bad' LOGFILE ext_bad:'orders_%p.log'
    FIELDS CSV WITH EMBEDDED TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
    MISSING FIELD VALUES ARE NULL)
  LOCATION ('orders_20261016.csv'))
REJECT LIMIT 100 PARALLEL 4;

INSERT /*+ APPEND */ INTO app.orders (order_id, customer_id, order_date, amount, status)
SELECT order_id, customer_id, TO_DATE(order_date,'YYYY-MM-DD HH24:MI:SS'), amount, status
FROM app.orders_ext;
COMMIT;
```
- Switch files without DDL: `SELECT * FROM app.orders_ext EXTERNAL MODIFY (LOCATION ('orders_20261017.csv'));` (12.2+).
- `PREPROCESSOR exec_dir:'zcat'` reads compressed files.
- `ORACLE_DATAPUMP` driver unloads query results to a binary file that another database
  reads as an external table (`CREATE TABLE x ORGANIZATION EXTERNAL (TYPE ORACLE_DATAPUMP ...) AS SELECT ...`).
- 19c+ `ORACLE_BIGDATA` / `DBMS_CLOUD` read object storage (CSV/Parquet).

## Choosing
SQL*Loader: client-side file, run from any host with the client. External tables:
file on the database server (or object storage), full SQL transformation, parallel
query, no separate tool. In both, the OS user running `oracle` must be able to read
the file and write bad/log files.

## Verify
- [ ] Log shows rows loaded vs rejected; bad file empty or reviewed.
- [ ] Indexes VALID after any direct-path load (`dba_indexes.status`).
- [ ] Character set in the control/access parameters matches the file encoding.
