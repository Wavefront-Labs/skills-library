---
id: computing-software.database-administration.duckdb.duckdb-iceberg-rest-catalogs
name: duckdb-iceberg-rest-catalogs
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, iceberg, rest-catalog, oauth2, polaris, lakekeeper, r2, time-travel, ducklake]
level: practitioner
status: docs-checked
description: "Attach Iceberg REST catalogs in DuckDB: iceberg secrets, ATTACH options, read/write support and limits, time travel, table properties, catalog examples."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/core_extensions/iceberg/iceberg_rest_catalogs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: read and write Iceberg tables through a REST catalog. (AWS S3 Tables and SageMaker Lakehouse have their own pages; the `ENDPOINT_TYPE` option is used for attaching S3Tables or Glue catalogs.)

Authenticate with an `iceberg` secret, then attach:

```sql
CREATE SECRET iceberg_secret (TYPE iceberg, CLIENT_ID '<id>', CLIENT_SECRET '<secret>',
    OAUTH2_SERVER_URI 'http://catalog.example/v1/oauth/tokens');
-- or with an existing bearer token:
CREATE SECRET iceberg_secret (TYPE iceberg, TOKEN '<bearer_token>');

LOAD httpfs;
ATTACH '<warehouse>' AS iceberg_catalog (TYPE iceberg, SECRET iceberg_secret, ENDPOINT 'https://rest_endpoint.example');
SHOW ALL TABLES;
```
Name the secret in `ATTACH` to avoid ambiguity.

ATTACH options: `ENDPOINT_TYPE` (`GLUE`, `S3_TABLES`; not with `ENDPOINT`), `ENDPOINT`, `SECRET`, `CLIENT_ID`, `CLIENT_SECRET`, `DEFAULT_REGION`, `OAUTH2_SERVER_URI`, `AUTHORIZATION_TYPE` (default `OAUTH2`; `SigV4`, or `none`), `ACCESS_DELEGATION_MODE` (default `vended_credentials`; or `none`), `SUPPORT_NESTED_NAMESPACES` (default true), `SUPPORT_STAGE_CREATE` (default false; for catalogs lacking stage create), `PURGE_REQUESTED` (default true; sent on DROP TABLE). Secret-only options (need OAUTH2): `OAUTH2_GRANT_TYPE`, `OAUTH2_SCOPE`.

Supported: `CREATE/DROP SCHEMA`, `CREATE/DROP TABLE`, `INSERT INTO`, `UPDATE`, `DELETE`, `SELECT`, and so `COPY FROM DATABASE duckdb_db TO iceberg_datalake` (deep copy either way). Not supported: `MERGE INTO`, `ALTER TABLE`. Reading from catalogs whose storage is not S3 or S3 Tables is not yet supported.

UPDATE/DELETE limits: only on tables that are not partitioned and not sorted (otherwise error); writes positional deletes only (copy-on-write is not yet supported); merge-on-read only, so the operation fails if a table has `write.update.mode` or `write.delete.mode` set to anything else. Table properties can be viewed, set and removed with:

```sql
SELECT * FROM iceberg_table_properties(iceberg_catalog.default.my_table);
CALL set_iceberg_table_properties(iceberg_catalog.default.my_table,
    {'write.update.mode': 'merge-on-read', 'write.delete.mode': 'merge-on-read'});
CALL remove_iceberg_table_properties(iceberg_catalog.default.my_table, ['some.property']);
```

Metadata and time travel (fully qualified names):

```sql
SELECT * FROM iceberg_snapshots(my_datalake.default.t);
SELECT * FROM my_datalake.default.t AT (VERSION => <snapshot_id>);
SELECT * FROM my_datalake.default.t AT (TIMESTAMP => TIMESTAMP '2025-09-22 12:32:43.217');
```
DuckLake interop (metadata-only copy): `ATTACH 'ducklake:my_ducklake.ducklake' AS my_ducklake; CALL iceberg_to_ducklake('iceberg_datalake', 'my_ducklake', skip_tables := ['t']);`

Catalog examples: Cloudflare R2 (`CREATE SECRET ... TYPE iceberg, TOKEN`; ATTACH warehouse with `ENDPOINT` catalog-uri from R2 settings); Polaris (client id/secret secret; `ATTACH 'quickstart_catalog'` with `ENDPOINT`); Lakekeeper (secret with `OAUTH2_SCOPE` and `OAUTH2_SERVER_URI`, ATTACH with `SECRET`).

## Checked

2026-11-07. Read the Iceberg REST Catalogs page in full and confirmed the secret forms, ATTACH with LOAD httpfs, both option tables (defaults, ENDPOINT versus ENDPOINT_TYPE, OAuth2-only secret options), the supported and unsupported operations, COPY FROM DATABASE, the UPDATE and DELETE limits, table property functions, metadata functions and time travel, iceberg_to_ducklake with skip_tables, the R2, Polaris and Lakekeeper examples and the non-S3 storage limitation. The page examples use placeholder hosts, so the fetch tool did not flag them as live. Reworded the ENDPOINT_TYPE hint and the table-property sentence (the page does not say setting properties fixes the failure) and removed the Verify step.

Method: documentation only; no commands were run.
