---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.index-table
name: index-table
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, data-patterns, index-table, secondary-index, nosql-query-patterns, global-secondary-index, lookup-table]
level: practitioner
status: docs-checked
description: "Apply the index table pattern in key-value and NoSQL stores: denormalised, normalised and partial index tables, composite keys, async consistency, and cost."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/index-table", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Index table

## Problem
Many stores organise data by primary key (and partition key). A query on another attribute, such as customers by town, may have to fetch and examine every record. Relational systems offer secondary indexes; some data stores have none, or indexes that do not meet the workload's query, partitioning or performance needs. Then you choose between full scans and managing an index yourself.

## Structuring strategies (Azure Architecture Center)
1. **Complete denormalisation**: each index table duplicates full records, keyed by a secondary key. Suits read-heavy data that changes rarely; update overhead and storage grow with the update rate and data size.
2. **Normalised index**: the index stores only the primary key (the "fact table" holds the data). Saves space and update effort but costs two lookups: index, then fact table.
3. **Partial denormalisation**: the index copies frequently retrieved fields and references the fact table for the rest. Common queries need one lookup, with less space and maintenance than full copies.
4. **Composite keys**: for queries on a combination (town and last name), build the key from several attributes. Use an encoding that preserves component boundaries so different combinations cannot produce the same key, and keep the required sort order under the store's collation rules.
5. **Over sharded data**: especially with a hashed shard key, index by the non-hashed values and store the hashed shard key to route each hit to the right shard; this supports range and ordered lookups.

## Native alternative: DynamoDB global secondary indexes
- A GSI projects the base table's keys plus attributes you choose: `KEYS_ONLY`, include-list or `ALL`. Trade smaller index (lower storage and write cost) against fewer queryable attributes; GSI queries cannot fetch attributes from the base table.
- GSIs are updated asynchronously and support eventually consistent reads only.
- A write to the table is throttled if the table or any GSI lacks write capacity; the DynamoDB guide advises provisioning GSI write capacity at least equal to the base table's.
- A table update that changes only attributes neither in the index key nor projected causes no index write.

## Design steps
1. List access patterns first; create an index only for queries used regularly, and review existing ones to drop unused indexes.
2. Pick complete, normalised or partial denormalisation.
3. Decide consistency. If source and index cannot update in one transaction, design for eventual consistency and capture each change durably before acknowledging the write: consume a change feed, use the Transactional Outbox, or enqueue a command first. Do not update the source and then separately publish an index-update message; a failure between them leaves the index stale.
4. Make the consumer idempotent, carry a source version or sequence number and apply only newer updates, and keep a versioned tombstone for deletes so a late older update cannot recreate an entry.
5. Expect stale references and missing recent records between the write and the index update.

## When not to
- Volatile data whose write rate outpaces asynchronous index refresh.
- Non-discriminating keys (such as a Boolean) or heavily skewed values (for example 90 percent identical), unless queries target the rare values.

## Verify
- [ ] Each access pattern is served by a key or index without scans.
- [ ] Index refresh is idempotent and handles out-of-order updates and deletes.
- [ ] Cost of extra writes (throughput units) is counted per index.

## Checked
2026-11-08, documentation only.
Confirmed against: Azure Architecture Center, Index Table pattern (last updated 2026-09-25); Amazon DynamoDB Developer Guide, Using Global Secondary Indexes.
Removed as unconfirmed by those pages: local secondary index behaviour, `TransactWriteItems`, Cosmos DB indexes-everything default, Bigtable row-key claim and the "status=PENDING" hot-partition example.
Method: documentation only; no commands were run.
