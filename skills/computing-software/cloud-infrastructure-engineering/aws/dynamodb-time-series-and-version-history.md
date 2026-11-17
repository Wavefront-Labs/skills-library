---
id: computing-software.cloud-infrastructure-engineering.aws.dynamodb-time-series-and-version-history
name: dynamodb-time-series-and-version-history
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, dynamodb, time-series-pattern, version-history-pattern, table-per-period, write-sharding, ttl, sort-key-versioning, transact-write-items, optimistic-locking, audit-trail, single-table-design]
level: advanced
status: docs-checked
description: "Model time-series and versioned items in DynamoDB: table-per-period and sharded partition keys for telemetry, v0 latest-plus-history sort keys for versioning, with TTL and costs."
sources: ["https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transaction-apis.html", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ServiceQuotas.html", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/contributorinsights_HowItWorks.html", "https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_BatchWriteItem.html", "https://github.com/boto/botocore/blob/develop/botocore/data/dynamodb/2012-08-10/service-2.json"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DynamoDB time-series and version-history patterns

**Goal:** high-rate timestamped data lands without hot partitions and ages out cheaply, and
entities keep a queryable history of every version with the current one readable in a
single `GetItem`.

## 1. Time series
### Partition key choice
- `PK = deviceId`, `SK = ts` (ISO-8601 or epoch zero-padded) when there are many devices:
  writes spread naturally, `Query PK=device AND SK BETWEEN t1 AND t2` is the read.
- If the natural key is low-cardinality (`PK = date` or a single metric), **write-shard**:
  `PK = "2026-10-16#" + (hash(id) % N)`; reads fan out N queries in parallel and merge.
  Size N so the expected peak write rate per key stays well under the documented per-item ceiling of
  1,000 write units per second; Contributor Insights shows the hottest keys.
### Table per period
- One table per day/week/month, for example `metrics_2026_10`: the current table gets high capacity (or
  on-demand), older tables can be switched to lower capacity or to the `STANDARD_INFREQUENT_ACCESS` table class,
  and tables past retention can be deleted whole instead of deleting items one by one.
- Create the next period's table ahead of time (scheduled job), and route writes by timestamp in the writer.
- Reads across periods query multiple tables; keep a small table or index of period to table name.
### TTL alternative
Single table + `expiresAt` epoch attribute with TTL enabled (a Number in Unix epoch seconds). Simpler, but
expired items are deleted by the system at any time, typically within a few days after expiry, so filter them out of
Query and Scan results with a filter expression. TTL deletes do not consume write throughput, appear in
DynamoDB Streams as service deletions, and are removed from local and global secondary indexes like other
deletes.

## 2. Version history
Sort-key versioning: `v0` is always the latest; `v1..vN` are immutable history.
| PK | SK | attrs |
|---|---|---|
| `DOC#42` | `v0` | `latest=3`, full current state |
| `DOC#42` | `v1` | state at version 1 |
| `DOC#42` | `v2` | ... |
| `DOC#42` | `v3` | state at version 3 |
Update = one transaction: insert the new history item and update `v0` conditionally.
```python
ddb.transact_write_items(TransactItems=[
  {"Put": {"TableName": T, "Item": {"PK": {"S": "DOC#42"}, "SK": {"S": "v4"}, **new_state},
           "ConditionExpression": "attribute_not_exists(SK)"}},
  {"Put": {"TableName": T, "Item": {"PK": {"S": "DOC#42"}, "SK": {"S": "v0"}, "latest": {"N": "4"}, **new_state},
           "ConditionExpression": "latest = :prev", "ExpressionAttributeValues": {":prev": {"N": "3"}}}}])
```
- Current: `GetItem SK=v0`. History: `Query PK=DOC#42 AND begins_with(SK,'v')` with
  `ScanIndexForward=False` (the result also contains `v0`; skip it). Zero-pad version
  numbers in real tables (`v000004`; the example above is unpadded for brevity) or
  ordering breaks past `v9`.
- The condition on `latest` is optimistic locking: a failed condition cancels the transaction
  (`TransactionCanceledException` with a `ConditionalCheckFailed` cancellation reason) and the editor must re-read.
- Large histories: store only diffs in history items, or archive old versions to S3 via
  Streams.

## Gotchas
- An item collection (all items with one PK) has a 10 GB limit when the table has a local secondary index;
  long histories + LSI can raise `ItemCollectionSizeLimitExceededException`.
- A transaction performs two underlying writes for every item (prepare and commit), so a two-item version
  write costs roughly four times a single plain write of the same size.
- Transactions cannot target the same item twice and cannot use indexes.
- Table-per-period multiplies alarms, backups and IAM resources; template them.
- ISO timestamps must share timezone and precision or lexical order lies.

## Verify
- [ ] Load test at 2x peak shows no `ThrottledRequests` and even `ConsumedWriteCapacityUnits` across shards (Contributor Insights top keys).
- [ ] Period rollover job created next month's table before midnight in a dry run.
- [ ] Two concurrent updates to the same document: exactly one succeeds, the other gets a condition failure.
- [ ] History query returns versions in order, latest first, past v10.

## Checked
Checked 2026-10-24 against the DynamoDB guide pages for TTL, Transactions, Quotas and Contributor Insights, and
the BatchWriteItem API page. Confirmed: expired items are deleted typically within a few days and may be deleted at any time; TTL attribute must be a Number in epoch seconds; TTL deletes consume no
write throughput, appear as service deletions in Streams and leave indexes like normal deletes;
`TransactionCanceledException`, the `ConditionalCheckFailed` reason, two underlying writes per transaction item,
no duplicate item targets, no index use; 10 GB item-collection limit with LSIs; the `STANDARD_INFREQUENT_ACCESS`
table class value; per-item 1,000 write unit ceiling. Removed the unchecked "AWS-recommended" label for
table-per-period, the "free, instant" deletion claim, and the 1,000 WCU per-partition sizing rule.
Method: documentation only; no commands were run.
