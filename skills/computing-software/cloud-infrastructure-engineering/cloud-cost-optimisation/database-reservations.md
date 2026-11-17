---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.database-reservations
name: database-reservations
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, rate-optimization, database-reservations, reserved-instances, rds, elasticache, opensearch, dynamodb, commitment-discounts]
level: practitioner
status: draft
description: "Buy non-compute commitments: RDS, Aurora, ElastiCache, OpenSearch, Redshift, DynamoDB and cloud SQL reservations; size flexibility, engine rules and break-even."
sources: ["https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithReservedDBInstances.html", "https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/CacheNodes.Reserved.html", "https://learn.microsoft.com/azure/cost-management-billing/reservations/save-compute-costs-reservations", "https://cloud.google.com/sql/docs/committed-use-discounts"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Non-compute commitments (database, cache, search, warehouse)

Managed data services are steady, long-lived and often 20-40% of a bill, yet frequently left on
on-demand because compute savings plans do not cover them.

## AWS
- **RDS / Aurora reserved DB instances**: per engine, instance class, region, deployment (Single-AZ
  vs Multi-AZ). **Size flexibility** within an instance family applies to MySQL, MariaDB, PostgreSQL,
  Aurora and Oracle BYOL; not to licence-included SQL Server / Oracle.
- **ElastiCache / MemoryDB reserved nodes**: per node type and engine; check size flexibility rules
  in current docs.
- **OpenSearch reserved instances**, **Redshift reserved nodes** (RA3 provisioned).
- **DynamoDB reserved capacity**: only for provisioned capacity mode (read/write capacity units),
  standard table class; on-demand tables cannot use it.
- Check whether newer database savings plan offerings fit your engines before buying RIs.

## Azure
Reservations for SQL Database / Managed Instance (vCore), Cosmos DB (RU/s), Azure Database for
PostgreSQL/MySQL, Cache for Redis, Synapse/Databricks pre-purchase; scopes and exchange rules as for
VM reservations.

## Google Cloud
Spend-based CUDs for Cloud SQL, AlloyDB, Memorystore, Spanner, Bigtable and others (1 or 3 years);
BigQuery editions slot commitments.

## Steps
1. Inventory steady databases running > 6 months with no planned engine or class change.
2. Normalise: for size-flexible families, convert to normalised units to find the floor.
3. Break-even: `months = upfront_equivalent / (on-demand monthly - reserved monthly)`; typically
   7-9 months for 1-year, 12-18 for 3-year.
4. Prefer 1-year for databases planned for engine migration (e.g. to Aurora / serverless) or
   major version changes; 3-year for stable core systems.
5. Buy, then track utilisation like compute commitments.

## Gotchas
- Moving Single-AZ to Multi-AZ, changing engine or region stops the reservation applying.
- Serverless database tiers usually cannot use reservations.
- Graviton (r7g, m7g) classes need their own reservations; plan migrations first.

## Verify
- [ ] Database coverage and utilisation reported separately from compute.
- [ ] Planned migrations checked before every purchase.
