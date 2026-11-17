---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.consistency-models
name: consistency-models
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, distributed-systems-design, consistency-models, strong-consistency, eventual-consistency, read-your-writes, cap-theorem, pacelc, cosmos-db-consistency-levels, multi-region-writes, conflict-resolution]
level: advanced
status: draft
description: "Choose the consistency model per data flow: strong vs eventual vs session, PACELC trade-offs, what managed databases actually offer (incl. multi-region), and conflict handling."
sources: ["https://learn.microsoft.com/azure/cosmos-db/consistency-levels", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadConsistency.html", "https://cloud.google.com/spanner/docs/true-time-external-consistency", "https://jepsen.io/consistency"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Consistency model choice

## Decide per flow, not per system
- **Strong / linearizable**: balances, inventory decrements, uniqueness (usernames), locks.
- **Session / read-your-writes**: user sees their own changes (profile edits, cart).
- **Eventual**: feeds, counters, analytics, search indexes, caches.

## Trade-off (PACELC)
During a partition choose availability or consistency; **else** (normal operation) choose
latency or consistency. Cross-region strong consistency costs round-trip latency on every write.

## What managed stores give you
| Store | Options |
|---|---|
| DynamoDB | eventually consistent reads by default; `ConsistentRead=true` for strong (single region); global tables multi-region replication is eventual with last-writer-wins (newer multi-region strong consistency option exists — check availability) |
| Cosmos DB | five levels: strong, bounded staleness, session (default), consistent prefix, eventual; multi-region writes require non-strong levels + conflict resolution policy |
| Spanner | external consistency (strong) globally via TrueTime; latency cost for multi-region writes |
| Aurora / RDS | strong on the writer; replicas are async (replica lag) — reads from replicas are eventual |
| S3 | strong read-after-write consistency for objects (since Dec 2020) |

## Steps
1. List data flows and their correctness requirement; pick the weakest acceptable level (cheaper, faster).
2. Route strong-read needs to the primary/writer; eventual reads to replicas/caches.
3. Multi-region active-active writes: define conflict resolution (LWW, merge, CRDTs, or
   partition ownership by region/home-region per user).
4. Monitor replication lag and treat it as an SLI.

## Verify
- [ ] Each flow documents its consistency level and the store setting that implements it.
- [ ] Tests cover reading immediately after writing on replica-backed paths.
