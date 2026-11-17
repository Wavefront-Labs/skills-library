---
id: computing-software.cloud-infrastructure-engineering.aws.multi-region-active-active-write-conflicts
name: multi-region-active-active-write-conflicts
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, multi-region, write-conflicts, multi-region-writes, dynamodb-global-tables, last-writer-wins, active-active]
level: practitioner
status: draft
description: "Multi-region active-active writes: last-writer-wins in DynamoDB global tables, strong consistency options, home-region partitioning and conflict-safe data models."
sources: ["Amazon DynamoDB Developer Guide - Global tables consistency modes (MREC and MRSC)", "Amazon Aurora User Guide - Write forwarding for Aurora Global Database", "AWS Whitepaper - Disaster Recovery of Workloads on AWS (multi-site active/active)", "Amazon Aurora DSQL User Guide - Multi-Region clusters"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multi-region active-active write conflicts

**Goal:** accept writes in more than one region without silently losing updates.

## What each data store does
| Store | Multi-region writes | Conflict behaviour |
|---|---|---|
| DynamoDB global tables, eventual (MREC) | every replica writable | **last writer wins** by timestamp per item; concurrent updates to the same item in two regions lose one silently |
| DynamoDB global tables, strong (MRSC) | writable, strongly consistent across 3 regions | conflicting concurrent writes fail with a replication conflict error rather than overwrite; higher write latency |
| Aurora Global Database | single writer region; write forwarding from secondaries | no conflicts (one writer); forwarded writes pay cross-region latency |
| Aurora DSQL multi-region | active-active, strong consistency | optimistic concurrency; conflicting transactions abort and retry |
| S3 bidirectional replication | both buckets writable | last writer wins per key; no merge |
| ElastiCache Global Datastore | one primary region | no conflicts |

## Design patterns
1. **Home region per entity:** route each user/tenant's writes to one region (cookie, account
   attribute, Route 53 geolocation); other regions read locally and forward writes. Conflicts disappear; failover reassigns home.
2. **Partitioned ownership:** different regions own different item types or key ranges.
3. **Conditional writes with versions:** `ConditionExpression: version = :expected` still only
   protects within a region on MREC; on MRSC it is safe globally.
4. **Commutative updates:** counters via `ADD`, append-only event logs (each region writes distinct items keyed by region + id), then aggregate.
5. **Idempotent operations** so retried cross-region writes do not double-apply.

## Detecting problems
- DynamoDB: `ReplicationLatency` metric per replica region; alarm on spikes (conflict window widens).
- Add `updated_region` and `updated_at` attributes so overwritten updates can be investigated.
- Test with chaos: concurrent writes to the same key in two regions, verify which survives and whether the business can accept it.

## Gotchas
- Last-writer-wins uses the service timestamp, not your application clock.
- Read-modify-write (read balance, write new balance) across regions is the classic lost-update bug; use atomic updates or single-region ownership for money.
- Strong multi-region consistency raises latency of every write to cross-region round trips.

## Verify
- [ ] Data classification lists which tables accept multi-region writes and their conflict policy.
- [ ] Concurrent-write test results documented and accepted by the business owner.
