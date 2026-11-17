---
id: computing-software.database-administration.cloud-nosql-databases.firestore-hotspot-avoidance
name: firestore-hotspot-avoidance
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [firestore-hotspot-avoidance, firestore-limits-hotspots, firestore, google-firestore, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Prevent write and index hotspots."
sources:
  - https://firebase.google.com/docs/firestore/best-practices
  - https://firebase.google.com/docs/firestore/understand-reads-writes-scale
  - https://firebase.google.com/docs/firestore/ttl
  - https://firebase.google.com/docs/firestore
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hotspot avoidance

**Goal:** Prevent write and index hotspots.

## Steps
- Avoid monotonically increasing document IDs and monotonically increasing indexed fields (such as timestamps) at high write rates; use automatic document IDs, which use a scatter algorithm. If you never query a sequential field, exempt it from indexing.
- A hotspot is a high read, write or delete rate to a narrow range of lexicographically close documents; avoid it, including when migrating traffic to a new collection.
- Shard counters across multiple documents, and ramp traffic to new collections with the 500/50/5 rule (500 operations per second, then +50% every 5 minutes).
- Use Key Visualizer to analyze usage patterns and troubleshoot hotspotting.

## Gotcha
A hotspot shows as increased latency and contention errors on a particular key range, and sustained high volume on a single document can hotspot it, so split or replicate that data across documents.

## Verify
- [ ] Load testing at the target rate shows flat latency and no contention errors.

## Checked

2026-11-03. Confirmed on the Best practices, Understand reads and writes at scale and TTL pages (monotonic IDs and fields, scatter IDs, narrow-range definition of a hotspot, 500/50/5, Key Visualizer, single-document hotspots). Removed: the queue-sharding and range-iteration claims.

Method: documentation only; no commands were run.
