---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.partition-key-design
name: partition-key-design
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, data-patterns, partition-key-design, hot-partitions, write-sharding, cosmos-db-partitioning, dynamodb-partition-key, synthetic-keys]
level: advanced
status: docs-checked
description: "Choose partition keys that spread load and keep queries single-partition: cardinality, access patterns, hot key detection, synthetic and hierarchical keys."
sources: ["https://learn.microsoft.com/azure/cosmos-db/partitioning-overview", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Partition key design

## Goals
1. **Even distribution** of storage and request load: DynamoDB says to design for uniform activity across all
   partition keys in the table and its secondary indexes. Cosmos DB divides provisioned throughput evenly among
   physical partitions, so uneven keys create "hot" partitions, inefficient throughput use, rate limiting and higher
   cost.
2. **Query locality**: choose a key that matches common query predicates; a high-cardinality key helps only if it also
   aligns with them. For several independent query patterns, Cosmos DB suggests synthetic keys, hierarchical partition
   keys or global secondary indexes.

## Techniques
- **High cardinality**: a property with a wide range of possible values. Low-cardinality fields such as status, type or
  country give few logical partitions and tend to uneven distribution; use them only when data volume and traffic per
  value stay well below the limits.
- **Hierarchical partition keys** (Cosmos DB): up to three levels, for data that could exceed a logical partition's
  20 GB.
- **Synthetic keys** combining properties, where no single property fits.
- **Write sharding** is a named DynamoDB technique (see the "Using write sharding to distribute workloads evenly"
  topic) for spreading hot-key writes.

## Limits (as stated on the pages)
- DynamoDB: each partition is designed for a maximum of 3,000 read units and 1,000 write units per second. One read
  unit is one strongly consistent read per second (or two eventually consistent) for up to 4 KB; one write unit is a
  write of up to 1 KB per second. Item size counts: with 20 KB items one consistent read costs 5 read units, so a
  single item supports 600 reads per second.
- Cosmos DB: a logical partition holds up to 20 GB; a physical partition provides up to 10,000 RU/s, so logical
  partitions are also limited to 10,000 RU/s. Use Azure Monitor alerts to watch a logical partition approaching
  20 GB.

## Steps
1. Enumerate access patterns with expected rates.
2. Score candidate keys by cardinality, skew and how many queries become cross-partition.
3. Load test with realistic key distribution.
4. Monitor partition size and per-partition load.

## Gotchas
- Cosmos DB partition key values are immutable: an item cannot be moved by replacement; create a new item and delete
  the old one (not atomic across logical partitions). You cannot change the container's key in place: move data to a
  new container (container copy jobs help) or use global secondary indexes for alternate keys. Partition key values
  should be strings or converted to strings when numbers may exceed IEEE 754 binary64 precision.

## Verify
- [ ] Load test shows no single partition approaching its limits.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Cosmos DB partitioning overview and the DynamoDB partition key best practices page. Removed: the
Azure data-partitioning source (URL now lands on a generic Well-Architected page), the 70 percent threshold, time-series
and whale-tenant advice, transactional batch claims, specific monitoring metric names, and the key-suffix example.
