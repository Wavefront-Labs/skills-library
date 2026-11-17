---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.globally-distributed-database
name: globally-distributed-database
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, database-selection, globally-distributed-database, spanner, cosmos-db, dynamodb-global-tables, cockroachdb]
level: practitioner
status: draft
description: "Choose a globally distributed database: consistency guarantees (Spanner, Cosmos DB levels, DynamoDB global tables), latency, conflict handling, data residency and cost."
sources: ["https://cloud.google.com/spanner/docs/true-time-external-consistency", "https://learn.microsoft.com/azure/cosmos-db/consistency-levels", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GlobalTables.html", "https://www.cockroachlabs.com/docs/stable/multiregion-overview"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Globally distributed databases

## Steps
1. **Start from requirements**: where users write from, acceptable write latency, consistency
   needed for each operation (balances, inventory need strong; profiles can be eventual), RPO
   on region loss, residency.
2. **Know the options**:
   - Spanner (and multi-region configs): external consistency via TrueTime; writes pay
     cross-region quorum latency; read-only and stale reads are local.
   - Cosmos DB: five consistency levels (strong, bounded staleness, session, consistent
     prefix, eventual); multi-region writes with conflict resolution (LWW or custom); strong
     consistency restrictions with multi-write.
   - DynamoDB global tables: multi-active; eventual consistency with last-writer-wins by
     default; multi-Region strong consistency mode where available; check current docs.
   - CockroachDB / YugabyteDB: SQL with regional tables, global tables and row-level homing.
   - Aurora Global Database: single writer region, fast promotion; good when writes can be homed.
3. **Data homing**: pin rows to regions (Cockroach REGIONAL BY ROW, partitioning by tenant)
   to keep strong consistency local and meet residency.
4. **Model the cost**: replicated writes are billed per region; cross-region transfer.
5. **Test failover and latency** with realistic geography.

## Gotchas
- Choosing strong global consistency for everything makes every write slow.
- Last-writer-wins silently drops concurrent updates; design for it or avoid multi-writer.

## Verify
- [ ] Consistency level justified per operation.
- [ ] Region-failure test with measured RPO/RTO.
