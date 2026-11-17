---
id: computing-software.data-engineering.snowflake.open-catalog-and-horizon-iceberg-rest
name: open-catalog-and-horizon-iceberg-rest
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, snowflake-open-catalog, apache-polaris, iceberg-rest-catalog, interoperability]
level: sme
status: docs-checked
description: "Expose Snowflake-managed Iceberg tables to other engines: Horizon Iceberg REST (preferred) versus Open Catalog sync, auth options and credential vending."
sources:
  - https://docs.snowflake.com/en/user-guide/opencatalog/overview
  - https://docs.snowflake.com/en/user-guide/tables-iceberg-open-catalog-sync
  - https://docs.snowflake.com/en/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Open Catalog and Horizon Iceberg REST access

**Goal:** one Iceberg table readable (and writable) by Snowflake and other engines such as Spark, with governed access, without copying.

## Which one
- **Horizon Catalog (Horizon Iceberg REST API):** available in all existing Snowflake accounts. Snowflake recommends it for querying Snowflake-managed Iceberg tables from a third-party engine, with read and write on Iceberg v2 and v3 tables. No sync step is needed. New customers should use Horizon.
- **Snowflake Open Catalog:** a managed service for Apache Polaris, built on the open Iceberg REST protocol. Customers who never had an Open Catalog account cannot sign up for a first one; existing customers can continue and create more. Syncing Snowflake-managed tables to Open Catalog is no longer recommended.

## Horizon: connect Spark
Endpoint: `https://<account_identifier>.snowflakecomputing.com/polaris/api/catalog`. In the Spark REST catalog config:
```
spark.sql.catalog.<name> = org.apache.iceberg.spark.SparkCatalog
spark.sql.catalog.<name>.type = rest
spark.sql.catalog.<name>.uri = https://<account_identifier>.snowflakecomputing.com/polaris/api/catalog
spark.sql.catalog.<name>.warehouse = <DATABASE_NAME>
spark.sql.catalog.<name>.credential = <PAT or token per the auth option>
spark.sql.catalog.<name>.scope = session:role:<role>
spark.sql.catalog.<name>.header.X-Iceberg-Access-Delegation = vended-credentials
```
- The `warehouse` property takes your Snowflake **database** name, not a warehouse name.
- Vended credentials require the table's OWNERSHIP role to keep USAGE on the table's external volume, otherwise reads and writes that ask for vended credentials fail.
- Auth options documented: key-pair JWT, programmatic access token (PAT), and workload identity (OIDC). With a PAT you pass the PAT as `.credential` for the engine; the separate access token from the curl step is only for verifying permissions.
- Use a dedicated service-account user and role with just the privileges needed (read-only or write, per the page's privilege tables). Tables with row access and masking policies need an engine connection that enforces data policies; see the page's section on that.

## Open Catalog sync (existing customers)
Steps documented: set a `BASE_LOCATION_PREFIX`, create an external volume (omit the prefix from `STORAGE_BASE_URL`), create an external catalog and service connection in Open Catalog with a catalog role (TABLE_CREATE, TABLE_WRITE_PROPERTIES, TABLE_DROP, NAMESPACE_CREATE, NAMESPACE_DROP, or CATALOG_MANAGE_CONTENT), create a catalog integration, set `CATALOG_SYNC`, then create a Snowflake-managed Iceberg table.
```sql
CREATE OR REPLACE CATALOG INTEGRATION my_open_catalog_int
  CATALOG_SOURCE = POLARIS
  TABLE_FORMAT = ICEBERG
  REST_CONFIG = (
    CATALOG_URI = 'https://<orgname>-<open_catalog_account>.snowflakecomputing.com/polaris/api/catalog'
    CATALOG_NAME = '<external_catalog_name>')
  REST_AUTHENTICATION = (TYPE = OAUTH OAUTH_CLIENT_ID = '<id>' OAUTH_CLIENT_SECRET = '<secret>'
    OAUTH_ALLOWED_SCOPES = ('PRINCIPAL_ROLE:ALL'))
  ENABLED = TRUE;
ALTER DATABASE db1 SET CATALOG_SYNC = 'my_open_catalog_int';   -- also schema, table, account level
```
- Synced name is `<catalog>.<database>.<schema>.<table>`. If your engine only reads two namespace levels, create the database with `CATALOG_SYNC_NAMESPACE_MODE = FLATTEN` (cannot be altered later).
- Changes made in Snowflake sync automatically to the external catalog. `SHOW ICEBERG TABLES` shows `catalog_sync_name`.

## Open Catalog governance
Principal roles are granted to service principals; catalog roles hold privileges on catalog resources and are granted to principal roles. Credential vending is on by default for internal catalogs and optional for external ones; do not enable it for an external catalog whose tables have overlapping storage locations, because vended credentials for one table then reach the other.

## Verify
In Spark, list tables in the namespace and compare a row count with Snowflake.

## Checked
2026-11-09. Confirmed on the Open Catalog overview, "Sync a Snowflake-managed table with Snowflake Open Catalog" and "Query Iceberg tables with an external engine using Horizon" pages: recommendation order, sign-up restriction, endpoint, Spark properties, warehouse property meaning, vended credentials and owner USAGE requirement, auth options, PAT versus access token, sync steps and privileges, FLATTEN mode, CATALOG_SYNC levels, credential vending behaviour. Removed: the claim that Spark/Flink/Trino compatibility and maintenance (compaction, snapshot expiry) advice, network policy statements, TABLE_READ_DATA/TABLE_WRITE_DATA names and catalog-linked database writes, none of which were confirmed. The Horizon and Open Catalog pages were read through targeted searches plus the full sync page, not every line of the 42k-character Horizon page.
Method: documentation only; no commands were run.
