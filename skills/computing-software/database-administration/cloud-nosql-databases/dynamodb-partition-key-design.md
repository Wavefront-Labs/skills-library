---
id: computing-software.database-administration.cloud-nosql-databases.dynamodb-partition-key-design
name: dynamodb-partition-key-design
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [dynamodb-partition-key-design, dynamodb-keys, dynamodb, amazon-dynamodb, cloud-nosql-databases, database-administration]
level: practitioner
status: draft
description: "Choose a partition key with high cardinality and even access so no partition runs hot."
sources:
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Partition key design

**Goal:** Choose a partition key with high cardinality and even access so no partition runs hot.

## Steps
- Each partition serves up to 3000 RCU and 1000 WCU per second (confirm); adaptive capacity isolates hot items but cannot split a single hot key.
- Prefer identifiers such as customerId or deviceId over status or date alone.
- For a hot key use write sharding: append a random suffix 1..N (pk = "2026-11-02#7") and scatter-gather reads across N shards.
- Use CloudWatch Contributor Insights to find the most-accessed keys.

## Gotcha
Low-cardinality keys (country, status) concentrate traffic; table-level throughput looks fine while one partition throttles.

## Verify
- [ ] Contributor Insights shows no key above a few percent of traffic and ThrottledRequests stays at 0 under load testing.
