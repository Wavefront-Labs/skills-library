---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.database-modernisation
name: database-modernisation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, modernisation, database-modernisation, managed-database, heterogeneous-migration, babelfish]
level: advanced
status: draft
description: "Modernise databases to managed or open-source engines: target choice, compatibility assessment, schema and code conversion, migration and tuning."
sources: ["https://docs.aws.amazon.com/SchemaConversionTool/latest/userguide/CHAP_Welcome.html", "https://learn.microsoft.com/azure/azure-sql/migration-guides/", "https://cloud.google.com/database-migration/docs/oracle-to-postgresql"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Database modernisation to managed engines

## Paths
- **Homogeneous** (SQL Server to Azure SQL Managed Instance / RDS for SQL Server; MySQL to
  Aurora MySQL): low code change, removes OS and patching burden.
- **Heterogeneous** (Oracle or SQL Server to PostgreSQL): removes licence cost, needs
  schema and code conversion. Babelfish for Aurora PostgreSQL accepts T-SQL to reduce app change.
- **Purpose-built** (move key-value or document access patterns to DynamoDB, Cosmos DB,
  Firestore): only with an access-pattern redesign.

## Steps
1. **Assess compatibility**: AWS SCT / DMS Schema Conversion assessment report, Azure
   Migrate / Data Migration Assistant, ora2pg reports. Look at % auto-converted and the
   complexity of stored procedures, packages, proprietary features (Oracle RAC, partitioning
   options, SQL Agent jobs, linked servers, CLR).
2. **Choose target** by feature needs, licence cost, team skills, HA options.
3. **Convert schema and code**; rewrite what tools cannot; move business logic out of the
   database where reasonable.
4. **Test**: functional regression, performance with production-like data and query mix;
   check query plans, collation and case sensitivity, NULL and empty-string semantics
   (Oracle treats empty string as NULL), date and numeric types.
5. **Migrate data** with full load + CDC; rehearse cutover.
6. **Tune** after go-live: parameters, indexes, connection pooling (PgBouncer / RDS Proxy).

## Gotchas
- Stored-procedure-heavy systems can take far longer to convert than tools estimate.
- Managed services restrict superuser access, OS access and some extensions.

## Verify
- [ ] Assessment report and conversion effort estimate approved.
- [ ] Performance tests show parity or better on top queries.
