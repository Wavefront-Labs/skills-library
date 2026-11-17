---
id: computing-software.data-engineering.apache-flink.flink-sql-catalogs
name: flink-sql-catalogs
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink-sql, flink-catalogs, hive-catalog, jdbc-catalog, iceberg-catalog, table-api]
level: practitioner
status: docs-checked
description: "Register and use Flink catalogs (GenericInMemory, Hive, JDBC, Iceberg) so table definitions persist and SQL jobs can query existing lake and database tables."
sources:
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/sql/catalogs/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/sql/interfaces/sql-client/
  - https://github.com/apache/flink-connector-hive/blob/main/docs/content/docs/connectors/table/hive/hive_catalog.md
  - https://github.com/apache/flink-connector-jdbc/blob/main/docs/content/docs/connectors/table/jdbc.md
  - https://github.com/apache/iceberg/blob/main/docs/docs/flink-configuration.md
  - https://github.com/apache/iceberg/blob/main/docs/docs/flink-writes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flink catalogs

By default Flink SQL uses `default_catalog` (GenericInMemoryCatalog): every `CREATE TABLE` vanishes when the session ends. A persistent catalog stores definitions and lets jobs read tables other systems already manage.

## Catalog types
| Catalog | Stores | Typical use |
|---|---|---|
| `generic_in_memory` | session only | ad-hoc, tests |
| `hive` | Hive Metastore | persist Flink table DDL (Kafka tables too, as generic tables), read/write Hive tables |
| `jdbc` | Postgres, MySQL and other JDBC databases (see the JDBC connector page) | query DB tables without DDL |
| `iceberg` | Iceberg catalog (`catalog-type` hive, hadoop or rest, or a custom `catalog-impl`) | streaming writes to/reads from Iceberg |

## Examples (SQL client)
```sql
CREATE CATALOG hive WITH ('type'='hive', 'hive-conf-dir'='/opt/hive/conf', 'default-database'='analytics');
CREATE CATALOG pg WITH ('type'='jdbc', 'base-url'='jdbc:postgresql://pg:5432', 'default-database'='shop',
                        'username'='flink', 'password'='${PG_PASSWORD}');
CREATE CATALOG lake WITH ('type'='iceberg', 'catalog-type'='rest', 'uri'='https://iceberg-rest:8181',
                          'io-impl'='org.apache.iceberg.aws.s3.S3FileIO');
USE CATALOG lake; USE analytics;
SHOW TABLES;
INSERT INTO lake.analytics.orders_iceberg SELECT * FROM default_catalog.default_database.orders_kafka;
SELECT * FROM pg.shop.`public.customers` LIMIT 10;     -- JDBC catalog: schema.table quoting
```
- Each catalog needs its jars on the classpath (Hive connector, JDBC connector plus the database driver, the Iceberg Flink runtime jar).
- Fully qualified names: `catalog.database.table`. Set defaults with `USE CATALOG` / `USE`.
- `HiveCatalog` handles Hive-compatible tables and generic (Flink-only) tables; a table is generic by default unless `'connector'='hive'` is set (or the Hive dialect is used). Generic tables are persisted in the metastore but using them from Hive leads to undefined behaviour.
- SQL client init scripts (`sql-client.sh -i init.sql`) can register catalogs per session.
- Catalog stores (`table.catalog-store.kind: file` with `table.catalog-store.file.path`) persist catalog definitions themselves across sessions.
- Credentials: avoid plain passwords in DDL that ends up in logs/history; use environment substitution or secret-mounted conf.

## Checked

2026-10-25 against the Apache Flink 2.3.0 documentation (release-2.3 branch on GitHub). Confirmed from the Catalogs page (GenericInMemoryCatalog, `default_catalog`/`default_database`, JdbcCatalog, HiveCatalog, catalog store options), the SQL client page (`-i`), the Hive connector repository's hive_catalog page (`'type'='hive'`, `hive-conf-dir`, generic versus Hive-compatible tables), the JDBC connector page (`base-url`, `default-database`, `username`, `password`, `schema.table` quoting) and the Iceberg Flink configuration page (`type`, `catalog-type` hive/hadoop/rest, `catalog-impl`, REST `uri`; `io-impl` S3FileIO class from the Iceberg AWS page; the Iceberg writes page for commits after a successful checkpoint). Removed the Paimon row (its docs were not checked), Derby, glue/nessie `catalog-type` values, and the operator and version claims.

Method: documentation only; no commands were run.

## Verify
- [ ] New session: `SHOW CATALOGS` / `SHOW TABLES` lists the persisted tables.
- [ ] A streaming insert into an Iceberg table commits snapshots on each checkpoint.
