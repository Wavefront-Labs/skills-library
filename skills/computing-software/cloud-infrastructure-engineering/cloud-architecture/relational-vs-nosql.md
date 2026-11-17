---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.relational-vs-nosql
name: relational-vs-nosql
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, database-selection, relational-vs-nosql, data-store-selection, access-patterns, document-database]
level: practitioner
status: docs-checked
description: "Choose relational or NoSQL data stores from access patterns, consistency, query flexibility and scale, using Azure's model heuristics and AWS's database family guide."
sources: ["https://learn.microsoft.com/azure/architecture/guide/technology-choices/data-store-overview", "https://docs.aws.amazon.com/whitepapers/latest/choosing-an-aws-nosql-database/choosing-an-aws-nosql-database.html", "https://cloud.google.com/architecture/framework/performance-optimization"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Relational vs NoSQL data store choice

## Decision factors (as the vendor guides state them)
- **Relational**: normalised tables, schema-on-write, ACID transactions, rich SQL and complex joins.
  Azure lists multi-row transactional consistency, strong constraints and mature reporting as strengths,
  and notes that horizontal scale generally requires sharding or partitioning. AWS recommends Aurora
  for modernising relational workloads or when query patterns are less predictable; Aurora PostgreSQL
  Limitless Database is for write throughput or storage beyond a single Aurora instance.
- **Key-value**: point lookup by key, atomicity at a single key. AWS describes DynamoDB as serverless
  NoSQL with single-digit millisecond performance at any scale, suited to session stores and carts.
- **Document**: aggregate-shaped, denormalised data with per-document schema flexibility. Azure's
  considerations: document size growth, limited transactional scope, careful data-shape design for
  high-scale queries. AWS positions DocumentDB for JSON-like documents with rich querying.
- **Wide-column**: AWS Keyspaces (Cassandra) for Cassandra migrations or single-digit millisecond
  latency at high throughput; Azure lists wide, sparse, write-heavy telemetry as column-family or time series.
- **Graph, time series, search, vector, object, analytics**: separate models for those query shapes.

## Azure heuristics
| Need | Prefer |
|---|---|
| Strict multi-entity transactions | Relational |
| Evolving aggregate shape, JSON-centric APIs | Document |
| Extreme low-latency key lookups or caching | Key-value |
| Deep relationship traversal | Graph |
| Full-text relevance and filtering | Search and indexing |

## Steps
1. List the access patterns with their latency, consistency and transaction needs before choosing a model.
2. Prefer one service while it still meets performance, scale and governance objectives (Azure: avoid
   premature fragmentation). Combine models only when access patterns diverge.
3. Check resiliency: AWS names backup and restore, replication, failover and point-in-time recovery.

## Gotchas
- Azure's re-evaluation signals: increasing ad hoc joins on a document store suggest adding a
  relational read model; large denormalised documents cause partial-update contention.
- Azure antipatterns: several microservices sharing one database, adding a model without operational
  maturity (monitoring, backups), and making a search index the primary store.

## Verify
- [ ] Access pattern list exists and each pattern maps to an index or key design.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed on the Azure data store overview and the AWS database guide: model strengths and
considerations, the heuristics table, antipatterns, DynamoDB, DocumentDB, Keyspaces, Aurora and Limitless
statements, and PITR as a resiliency factor. The Google Cloud performance page was fetched but gave no
claim used here. Removed as unconfirmed on those pages: Spanner, AlloyDB, Cloud SQL, Bigtable, Firestore
placement, "default relational", single-table design and hot-partition advice, and on-demand cost claims.
