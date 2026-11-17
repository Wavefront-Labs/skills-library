---
id: computing-software.cloud-infrastructure-engineering.azure.cosmos-db-api-choice-and-mongodb-vcore
name: cosmos-db-api-choice-and-mongodb-vcore
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, cosmos-db, cosmos-api-choice, mongodb-vcore, mongodb-ru, postgresql-citus]
level: advanced
status: docs-checked
description: "Choose the right Azure Cosmos DB API (NoSQL, MongoDB, Cassandra, Gremlin, Table, PostgreSQL) for a workload and migrate MongoDB apps."
sources: ["https://learn.microsoft.com/azure/cosmos-db/", "https://learn.microsoft.com/azure/cosmos-db/concepts-limits", "https://learn.microsoft.com/azure/cosmos-db/mongodb/feature-support-42"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cosmos DB API choice and MongoDB options

**Goal:** pick the API and model once; switching later means a migration.

## APIs offered
The Azure Cosmos DB documentation hub lists these APIs: **NoSQL** (native SQL queries, automatic indexing, schema flexibility), **MongoDB** (wire protocol compatibility for existing MongoDB apps), **Apache Cassandra** (CQL), **Apache Gremlin** (graph), **Table** (modernise Azure Table Storage apps) and **PostgreSQL** (distributed relational, PostgreSQL wire protocol).

## Decision guide
| Need | Start from |
|---|---|
| New cloud-native app with document data | NoSQL API |
| Existing MongoDB application | MongoDB offering (check the supported features and syntax for your server version) |
| Existing Cassandra workload | Cassandra API |
| Graph traversals with Gremlin | Gremlin API |
| Azure Table Storage upgrade | Table API |
| Distributed relational workload on PostgreSQL | PostgreSQL API |

For the MongoDB offerings (request-unit based versus vCore cluster based, and the Azure DocumentDB naming), compare the current MongoDB documentation before deciding; differences in pricing model, scaling and query compatibility are not restated here.

## MongoDB facts worth checking before migrating
- Supported commands and protocol versions are listed in "Supported MongoDB features and syntax".
- Documents up to 16 MB are supported for the MongoDB API (large document sizes require feature enablement in the portal); the NoSQL API limit is 2 MB per item.
- Maximum execution time for MongoDB operations is 60 seconds for server versions 3.6 and 4.0.
- Set the driver idle connection timeout to 2-3 minutes: the service closes idle connections after 30 minutes and the default Azure Load Balancer timeout is 4 minutes.
- Azure Database Migration Service is a documented migration route for the MongoDB API.

## Verify
- [ ] Decision record lists API, reasons and rejected options.
- [ ] Compatibility check against the documented feature support has no blocking gaps.

## Checked

2026-10-24, against the Azure Cosmos DB documentation hub (updated 2026-06-18) and the service quotas article (updated 2026-08-25): list of APIs, MongoDB limits (16 MB documents, 60 s execution time, 30-minute idle timeout and 2-3 minute driver advice), 2 MB NoSQL item limit, Azure Database Migration Service as a migration route. Removed the unconfirmed RU-versus-vCore comparison table, SLA figure, Cosmos DB for PostgreSQL product name, Azure Data Studio extension and the retrywrites statement.

Method: documentation only; no commands were run.
