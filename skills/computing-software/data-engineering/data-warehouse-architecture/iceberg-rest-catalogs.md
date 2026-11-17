---
id: computing-software.data-engineering.data-warehouse-architecture.iceberg-rest-catalogs
name: iceberg-rest-catalogs
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, apache-iceberg, iceberg-rest-catalog, polaris, nessie, glue-catalog, credential-vending, multi-engine]
level: advanced
status: gated
description: "Pick and configure an Iceberg REST catalog (Polaris/Open Catalog, Glue, Unity, Nessie, Lakekeeper) for multi-engine access: Spark/Trino/Flink config, credential vending and RBAC."
sources:
  - https://iceberg.apache.org/docs/latest/spark-configuration/
  - https://py.iceberg.apache.org/configuration/
  - https://trino.io/docs/current/object-storage/metastores.html
  - https://iceberg.apache.org/rest-catalog-spec/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Iceberg REST catalogs

**Goal:** many engines (Spark, Trino, Flink, Snowflake, DuckDB, PyIceberg) read and write the same Iceberg tables safely through one catalog with central access control.

## Why the catalog matters
The catalog stores the pointer to each table's current metadata file and performs the atomic swap on commit. Two engines using different catalogs for the same table = lost commits/corruption. The REST spec standardises the API so any engine can use any compliant catalog.

## Options
| Catalog | Notes |
|---|---|
| Apache Polaris / Snowflake Open Catalog | REST, RBAC with principal roles/catalog roles, credential vending (gated: unconfirmed, source is paywalled or blocked) |
| AWS Glue (Iceberg REST endpoint) + Lake Formation | AWS-native permissions; also S3 Tables managed Iceberg (gated: unconfirmed, source is paywalled or blocked) |
| Databricks Unity Catalog (Iceberg REST API) | read Delta-UniForm/managed Iceberg from external engines (gated: unconfirmed, source is paywalled or blocked) |
| Project Nessie | git-like branches/tags across tables |
| Lakekeeper, Gravitino | open-source REST implementations (both exist as GitHub projects: lakekeeper/lakekeeper, apache/gravitino) |
| JDBC / Hive metastore catalogs | legacy, not REST; avoid for new multi-engine setups |

## Engine configuration
Spark (`type=rest`, `uri` per the Iceberg Spark configuration docs; the access-delegation header is defined in the REST spec as `X-Iceberg-Access-Delegation`; the `credential` and `scope` Spark properties are Polaris-style (gated: unconfirmed, source is paywalled or blocked); not run here):
```properties
spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions
spark.sql.catalog.lake=org.apache.iceberg.spark.SparkCatalog
spark.sql.catalog.lake.type=rest
spark.sql.catalog.lake.uri=https://catalog.example.com/api/catalog
spark.sql.catalog.lake.warehouse=analytics
spark.sql.catalog.lake.credential=<client_id>:<client_secret>
spark.sql.catalog.lake.scope=PRINCIPAL_ROLE:ALL
spark.sql.catalog.lake.header.X-Iceberg-Access-Delegation=vended-credentials
```
Trino (`etc/catalog/lake.properties`; every property below was found in the Trino metastore docs: `iceberg.rest-catalog.uri`, `warehouse`, `security`, `oauth2.credential`, `vended-credentials-enabled`):
```properties
connector.name=iceberg
iceberg.catalog.type=rest
iceberg.rest-catalog.uri=https://catalog.example.com/api/catalog
iceberg.rest-catalog.warehouse=analytics
iceberg.rest-catalog.security=OAUTH2
iceberg.rest-catalog.oauth2.credential=<id>:<secret>
iceberg.rest-catalog.vended-credentials-enabled=true
```
PyIceberg (`type="rest"`, `uri`, `warehouse`, `credential="client_id:client_secret"` confirmed in the PyIceberg configuration docs; the identical `load_catalog` / `load_table` / `scan(row_filter=...).to_arrow()` calls were run against a SQL catalog):
```python
from pyiceberg.catalog import load_catalog
cat = load_catalog("lake", type="rest", uri="https://catalog.example.com/api/catalog",
                   credential="id:secret", warehouse="analytics")
tbl = cat.load_table("sales.orders"); df = tbl.scan(row_filter="order_date >= '2026-10-01'").to_arrow()
```

## Credential vending
With vended credentials, the catalog returns short-lived, table-scoped storage credentials on `loadTable`. Engines need no broad bucket access; revoking catalog privileges revokes data access. Without vending, every engine needs its own storage IAM, and catalog RBAC can be bypassed by reading files directly.

## Governance setup
- One catalog of record per table; other platforms federate/mirror read-only if needed.
- Map principals (service accounts per engine/job) to roles with least privilege (read vs write per namespace).
- Table maintenance (compaction, snapshot expiry, orphan cleanup) owned by one writer platform to avoid conflicting rewrites.

## Gotchas
- Spec versions and features (view support, multi-table transactions, server-side planning) vary by catalog; test the engines you need.
- Case sensitivity and namespace nesting differ between engines.
- Token endpoints/OAuth scopes differ per implementation.

## Verify
- [ ] Write from Spark, read from Trino and PyIceberg: same snapshot id.
- [ ] Revoking a role's catalog privilege blocks data reads (vending), confirmed by test.
