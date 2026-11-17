---
id: computing-software.database-administration.cloud-nosql-databases.firestore-distributed-counters-and-write-limits
name: firestore-distributed-counters-and-write-limits
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [firestore-distributed-counters-and-write-limits, firestore-transactions, firestore, google-firestore, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Handle high-frequency updates to a single document."
sources:
  - https://firebase.google.com/docs/firestore/solutions/counters
  - https://firebase.google.com/docs/firestore/best-practices
  - https://firebase.google.com/docs/firestore
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Counters and write rate limits

**Goal:** Handle high-frequency updates to a single document.

## Steps
- A single document cannot be updated at an unlimited rate; a counter document that is incremented often enough sees contention. A distributed counter is a counter document with a subcollection of shard documents; the value is the sum of the shards, and write throughput grows linearly with the shard count (10 shards handle 10x the writes). The documentation's sample assumes about one increment per second per shard.
- For low-rate counters, FieldValue.increment() updates a field without a read.
- An indexed field that increases or decreases sequentially between documents (such as a timestamp) limits the collection to 500 writes per second; exempt the field from indexing if you never query it.
- Ramp traffic to a new collection or to lexicographically close documents with the 500/50/5 rule: start at a maximum of 500 operations per second and increase by 50% every 5 minutes.

## Gotcha
Monotonically increasing document IDs or sequential indexed fields create hotspots; use automatic document IDs, which are scattered.

## Verify
- [ ] Load test confirms counters hold the rate with no contention errors.

## Checked

2026-11-03. Confirmed on the Distributed counters, Best practices and add-data pages (sharding, linear throughput, 500/50/5 rule, 500 writes per second with a sequential indexed field, scatter-based automatic IDs, increment()). Removed: the unsourced 1 write per second per document limit and the 10,000 writes per second figure.

Method: documentation only; no commands were run.
