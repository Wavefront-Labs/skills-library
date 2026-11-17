---
id: computing-software.cloud-infrastructure-engineering.aws.dynamodb-gsi-projections-and-write-backpressure
name: dynamodb-gsi-projections-and-write-backpressure
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, dynamodb, gsi-projection, gsi-backpressure, write-amplification, global-secondary-index, index-design]
level: advanced
status: docs-checked
description: "Design DynamoDB GSIs that do not hurt writes: projection choices, write amplification, GSI throttling back-pressure on the base table, capacity settings and backfill behaviour."
sources: ["https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ServiceQuotas.html", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/metrics-dimensions.html", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/contributorinsights_HowItWorks.html", "https://github.com/boto/botocore/blob/develop/botocore/data/dynamodb/2012-08-10/service-2.json"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GSI projections and write back-pressure

## 1. Projection types
| Projection | Index stores | Trade-off |
|---|---|---|
| `KEYS_ONLY` | table keys + index keys | smallest, cheapest writes; queries need a follow-up read on the table for other attributes |
| `INCLUDE` | keys + listed non-key attributes (up to 100 attributes combined across all of a table's secondary indexes) | right-size for the query's needs |
| `ALL` | full item | simplest queries; storage cost can double; every attribute change rewrites the index item |
GSI queries cannot fetch attributes from the base table. `UpdateTable` can only create, update (capacity,
on-demand and warm throughput settings) or delete a GSI, so changing a projection means creating a new index,
migrating readers and deleting the old one. Each index item also carries 100 bytes of overhead.

## 2. Write amplification
Each base-table write that affects an index consumes write capacity from that index:
- Item added with index key attributes present: one index write.
- Index key attribute changed (A to B): two index writes (delete the old entry, put the new one).
- Index key attribute removed from an item that was in the index: one index write (delete).
- Only a projected non-key attribute changed: one index write. Only attributes that are neither index keys
  nor projected changed: no index write (a reason to avoid `ALL`).
- Item neither in the index before nor after: no index cost (sparse index).
- The 1 KB write-unit rounding applies to the index item, so larger index entries cost more units.
A table with many GSIs costs more per write than one with few.

## 3. Back-pressure: GSI capacity throttles the table
For a table write to succeed, the table and all its GSIs need enough write capacity; otherwise the table write
is throttled. In provisioned mode a GSI has its own read and write capacity settings, separate from the table.
Symptoms: `WriteThrottleEvents` on the GSI (dimension `GlobalSecondaryIndexName`) and `ThrottledRequests`
on the table operation. `ThrottledRequests` is incremented when any event in a request (table or index write)
is throttled.
Rules:
- Provisioned mode: set GSI write capacity equal to or greater than the table's for indexes that see every
  write; scale each GSI separately.
- Hot GSI keys: low-cardinality GSI partition keys (`status`, `type`, `date`) concentrate writes; shard them
  (`status#<0-9>`) and query all shards in parallel. Contributor Insights does not measure write throttling
  caused by insufficient GSI capacity; its "most accessed items" graph for the GSI shows skew.
- On-demand tables: GSIs inherit the capacity mode of the base table; per-item limits of 1,000 write units
  and 3,000 read units per second still apply.

## 4. Consistency and reads
GSI reads are eventually consistent only (strongly consistent reads are not supported on a GSI); a
just-written item may not appear yet. Design flows that need read-after-write on the base table key.

## 5. Adding a GSI to a big table
`update-table --global-secondary-index-updates Create=...` triggers a **backfill** that
reads the table and populates the index (`IndexStatus` `CREATING`, with `Backfilling` shown in
`DescribeTable`). Writes to the base table can be throttled during creation if GSI write capacity is too low.
Monitor `OnlineIndexPercentageProgress`; the documentation says `OnlineIndexConsumedWriteCapacity` and
`OnlineIndexThrottleEvents` now show 0 during index builds.

## Verify
- [ ] Every GSI's projection justified by a documented query; no `ALL` without reason.
- [ ] CloudWatch shows zero GSI `WriteThrottleEvents` at peak; table write throttles traced to GSIs if any.
- [ ] Low-cardinality GSI keys sharded or replaced.

## Checked
Checked 2026-10-24 against the DynamoDB guide pages for Global Secondary Indexes (including the provisioned
throughput and storage sections), Quotas, CloudWatch metrics and Contributor Insights, plus the botocore model.
Confirmed: the three projection types; the 100-attribute INCLUDE limit across all secondary indexes; GSI reads
eventually consistent and no `GetItem`/`BatchGetItem` on a GSI; the write-cost cases for adding, changing,
removing and not touching indexed attributes; GSI write capacity should be at least the base table's; the table
write is throttled when GSI capacity is short; metric names and the `GlobalSecondaryIndexName` dimension;
`OnlineIndexPercentageProgress` semantics; `UpdateGlobalSecondaryIndexAction` carries only capacity-related
members. Removed the "6x or more" multiplier, the old `ValidationException` claim for strongly consistent GSI
reads (the page says unsupported without naming the error) and the on-demand "1,000 WCU per partition"
wording, replaced by the documented per-item ceiling.
Method: documentation only; no commands were run.
