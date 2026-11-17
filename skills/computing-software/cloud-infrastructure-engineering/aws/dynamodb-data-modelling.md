---
id: computing-software.cloud-infrastructure-engineering.aws.dynamodb-data-modelling
name: dynamodb-data-modelling
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, dynamodb, single-table-design, partition-key, sort-key, gsi, lsi, global-secondary-index, local-secondary-index, access-patterns, composite-keys, key-overloading, sparse-index, inverted-index, hot-partition, write-sharding, item-collection, query-vs-scan, begins-with, adjacency-list, nosql-workbench, item-size-limit, transactions, condition-expression, optimistic-locking, partiql]
level: advanced
status: docs-checked
description: "Model DynamoDB from access patterns: partition/sort keys, overloaded keys for single-table design, sparse and inverted GSIs, hot-partition avoidance, and the 400 KB / 10 GB limits."
sources: ["https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ServiceQuotas.html", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transaction-apis.html", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadConsistency.html", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/contributorinsights_HowItWorks.html", "https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_BatchWriteItem.html", "https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_BatchGetItem.html", "https://github.com/boto/botocore/blob/develop/botocore/data/dynamodb/2012-08-10/service-2.json"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DynamoDB data modelling: keys, indexes, single-table design

**Goal:** a table (usually one) whose keys and indexes answer every known access
pattern with a `Query` (never a `Scan`), spread load evenly across partitions, and stay
inside the hard limits, designed *before* the first item is written, because keys
cannot be changed afterwards.

## 1. Start from access patterns, not entities
Write the list first: "get user by id", "list orders for a user newest first", "find
order by order id", "list orders by status in the last 24 h", "all items in order".
Each row becomes a key design or an index. DynamoDB has no joins and no ad-hoc query
planner: an access pattern you did not design for costs a `Scan` of the whole table.

## 2. Key mechanics
- **Partition key (PK)**: hashed to a physical partition; every `GetItem`/`Query` needs
  it exactly. Choose something with many distinct values and even traffic.
- **Sort key (SK)**: orders items inside a partition; `Query` supports comparison operators, `between` and
  `begins_with` on it, ascending/descending (`ScanIndexForward`), and `Limit` with `LastEvaluatedKey` pagination:
  this is where "list newest N" and hierarchical lookups live.
- An **item collection** = all items with the same PK; it is the unit of locality.
- Hard limits and defaults: item up to **400 KB** (as stored); an item collection in a table with an LSI is
  limited to **10 GB**; per-item throughput ceiling of **1,000 write units / 3,000 read units per second**
  (Contributor Insights page); default **20 GSIs** and **5 LSIs** per table. A table's primary key cannot be
  altered by `UpdateTable`, so a key change means a new table and a migration.
## 3. Single-table design with overloaded keys
Generic attribute names `PK`/`SK` (and `GSI1PK`/`GSI1SK`) hold typed, prefixed values:
| Entity | PK | SK | GSI1PK | GSI1SK |
|---|---|---|---|---|
| User | `USER#u1` | `PROFILE` | `EMAIL#a@b.c` | `USER#u1` |
| Order | `USER#u1` | `ORDER#2026-10-15T09:00#o77` | `ORDER#o77` | `ORDER#o77` |
| Order item | `ORDER#o77` | `ITEM#sku9` | n/a | n/a |
| Order by status | (same item) | | `STATUS#SHIPPED` | `2026-10-15T09:00#o77` |
- "Orders for user newest first": `Query PK=USER#u1, SK begins_with ORDER#, ScanIndexForward=false`.
- "Order by id": `Query GSI1 GSI1PK=ORDER#o77`.
- "User by email": `Query GSI1 GSI1PK=EMAIL#...`. DynamoDB has no unique constraint, so write a separate
  uniqueness item (`PK=EMAIL#a@b.c`) in a transaction with the profile.
- Store a `type` attribute on every item for filtering/ETL; use ISO-8601 or zero-padded
  numbers in sort keys so lexical order = chronological order.
- Put a parent and its children in one collection (adjacency list) so one `Query`
  fetches the aggregate; keep collections well under 10 GB if any LSI exists.

## 4. Indexes
| | GSI | LSI |
|---|---|---|
| Keys | Any PK/SK | Same PK, different SK |
| Created | Any time (`UpdateTable` GSI create) | Only at table creation (no LSI update in `UpdateTable`) |
| Consistency | Eventual only | Strong available |
| Capacity (provisioned) | Own read/write capacity; short GSI write capacity throttles table writes | n/a here |
| Size | no stated limit | Item collection <= 10 GB |
- **Sparse index**: only items that have the GSI key attribute appear: put
  `GSI2PK=PENDING` only on pending orders and the "list pending" query touches just them;
  delete the attribute when state changes.
- **Inverted index**: GSI with the table's SK as its partition key and PK as its sort key turns a many-to-many
  (user<->group) into queries from either side.
- **Projection**: `KEYS_ONLY` / `INCLUDE` specific attributes (100 combined across a table's secondary indexes) /
  `ALL`. Projected attributes are stored again and a change to one is an index write; project only what the
  query reads and fetch the rest from the table when rare (`BatchGetItem` takes up to 100 keys).
- GSI write cost: one item write that touches 3 GSIs costs the table write plus up to 3 index writes, and a
  changed index key attribute costs two writes in that index (delete + put).

## 5. Avoid hot partitions
- Time-series with `PK=date` is the classic hot key: every write today hits one
  key. Shard: `PK=date#<n>` with `n = hash(id) % 10` and query all 10 shards in
  parallel; or `PK = deviceId`, `SK = timestamp`.
- Popular items (a celebrity's feed, a global counter): write-shard the same way, or
  cache reads with DAX. Counters: `UpdateItem ADD` on a few shards, sum on read.
- CloudWatch Contributor Insights on the table shows the most accessed and most throttled keys.

## 6. Writes that need guarantees
- `ConditionExpression: attribute_not_exists(PK)` for create-if-absent;
  `version = :expected` for optimistic locking (bump `version` in the same update).
- **Transactions** (`TransactWriteItems`: up to 100 actions on distinct items, 4 MB aggregate, two underlying
  writes per item) for multi-item invariants: profile + email-uniqueness item, debit + credit. Transactions cannot
  use indexes. Not a substitute for modelling the data so one item holds the invariant.
- `BatchWriteItem` (25 requests) has no conditions and can partially fail (`UnprocessedItems`): retry with backoff.
- Large attributes: compress (gzip + binary type) or put blobs in S3 and store the key.

## 7. Reading efficiently
`Query` with `KeyConditionExpression` and `Limit`/pagination (`LastEvaluatedKey`); `FilterExpression` is applied
after the query reads the items and before results are returned, so filtering does not reduce what is read:
a filter that discards most items means the key design is wrong. Eventually consistent reads cost half of strongly
consistent ones; use `ConsistentRead=true` only where read-after-write matters (tables and LSIs, never GSIs).
PartiQL without a key condition is a `Scan`.

## Gotchas
- Changing the primary key = new table + migration (`Scan` and write, or DynamoDB export/import to S3).
  Design the keys like a public API.
- An LSI caps every item collection at 10 GB for the life of the table (LSIs cannot be
  added or removed later); avoid LSIs unless you need strong consistency on a second sort order.
- Attribute names that are DynamoDB reserved words (the API docs use `Percentile` as an example) must go
  through `ExpressionAttributeNames` (`#p`).
- `Scan` with `Segment`/`TotalSegments` is available for parallel scans (ETL); keep scans off request paths.
- Items returned by `BatchGetItem` come in no particular order.

## Verify
- [ ] Every access pattern in the list maps to a `GetItem`/`Query` (document the table facet per pattern); zero `Scan` in application code.
- [ ] Load test: `ThrottledRequests`/`WriteThrottleEvents` on table and each GSI stay 0 at target throughput; Contributor Insights shows no key dominating traffic.
- [ ] `ConsumedReadCapacityUnits` per query is close to returned-item size (filters discard little).
- [ ] Largest item is well under 400 KB; largest item collection (if LSI) projected well under 10 GB at 3-year growth.
- [ ] A uniqueness violation (duplicate email) is rejected by the transaction, not detected after the fact.

## Checked
Checked 2026-10-24 against the DynamoDB guide pages for Quotas, Global Secondary Indexes, Transactions,
read consistency and Contributor Insights, the BatchWriteItem and BatchGetItem API pages and the botocore
model. Confirmed: 400 KB item size, 10 GB item collection limit with LSIs, default 20 GSIs and 5 LSIs,
GSI-only `UpdateTable` index changes (so LSIs at creation and no primary key change), GSI eventual consistency
and independent capacity, 100-attribute INCLUDE limit, sparse-index behaviour, transaction limits and cost, no
indexes in transactions, batch limits, per-item 1,000/3,000 ceiling, `ScanIndexForward`, `LastEvaluatedKey`,
`Segment`/`TotalSegments`, and that filter expressions apply after the read. The old "Unconfirmed" notes on the
transaction item limit and GSI count are now resolved (100 and 20 defaults). Removed unchecked statements:
the per-partition-key 3,000/1,000 wording, LSI "shares table capacity", the ProjectionExpression/RCU note, the
38-digit number note, the empty-string note, KSUID/ULID remarks, the NoSQL Workbench mention and the claim that
specific attribute names such as `name` or `status` are reserved.
Method: documentation only; no commands were run.
