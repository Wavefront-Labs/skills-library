---
id: computing-software.cloud-infrastructure-engineering.aws.dynamodb-batch-operations-and-unprocessed-items
name: dynamodb-batch-operations-and-unprocessed-items
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, dynamodb, batch-write-item, batchgetitem, unprocessed-items, exponential-backoff, bulk-load]
level: practitioner
status: docs-checked
description: "Use DynamoDB BatchGetItem and BatchWriteItem correctly: size limits, retrying UnprocessedItems/Keys with backoff, SDK helpers, and when to use import from S3 instead."
sources: ["https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_BatchWriteItem.html", "https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_BatchGetItem.html", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transaction-apis.html", "https://github.com/boto/botocore/blob/develop/botocore/data/dynamodb/2012-08-10/service-2.json", "https://github.com/boto/boto3/blob/develop/boto3/dynamodb/table.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DynamoDB batch operations

## 1. Limits
| | BatchWriteItem | BatchGetItem |
|---|---|---|
| Items per call | 25 put/delete requests | 100 keys |
| Payload | 16 MB total request, 400 KB per item | up to 16 MB returned |
| Tables | many in one call | many in one call |
| Update expressions/conditions | **not supported**: puts replace whole items, no conditions, deleted items are not returned | n/a |
| Atomicity | each put/delete is atomic, the batch as a whole is not | n/a |
| Consistency | n/a | eventually consistent by default; `ConsistentRead` can be set per table |
The same item (identical key) cannot appear twice in one BatchWriteItem call (the whole batch is rejected),
and BatchGetItem returns a `ValidationException` if the same key is specified more than once.

## 2. Unprocessed items are normal
When throttled or after an internal failure, DynamoDB returns success with
`UnprocessedItems` (writes) or `UnprocessedKeys` (gets). Code that ignores them silently
loses data. Retry only those, with exponential backoff and jitter:
```python
import random, time
def batch_write(client, table, items):
    reqs = [{"PutRequest": {"Item": it}} for it in items]
    for i in range(0, len(reqs), 25):
        pending = {table: reqs[i:i + 25]}
        attempt = 0
        while pending:
            resp = client.batch_write_item(RequestItems=pending)
            pending = resp.get("UnprocessedItems") or {}
            if pending:
                attempt += 1
                if attempt > 10:
                    raise RuntimeError(f"giving up, {sum(map(len, pending.values()))} items left")
                time.sleep(min(20, (2 ** attempt) * 0.05) * random.random())
```
boto3's resource-level `table.batch_writer()` buffers writes and accepts `overwrite_by_pkeys` to
de-duplicate keys within a buffer.

## 3. Capacity and throughput
- Each put or delete consumes the same write capacity whether or not it is batched (the API reference says
  parallel processing reduces latency, not capacity); a delete of a nonexistent item still consumes one WCU.
- If every item in a BatchWriteItem is throttled the call returns `ProvisionedThroughputExceededException`
  or `ThrottlingException`; check `ThrottlingReason` for the cause. Spread work across distinct partition keys.
- Warm throughput can be set when a table is created (`CreateTable` accepts `WarmThroughput`) for a known load.

## 4. Alternatives
- **Import from S3** (`ImportTable`; CSV, DynamoDB JSON or Ion) creates a **new** table from S3 data.
- **TransactWriteItems** when items must succeed or fail together (up to 100 actions, 4 MB aggregate,
  supports conditions, two underlying writes per item).
- **PartiQL `BatchExecuteStatement`** for batches of PartiQL statements (up to 25 per batch).
- Deleting many items: there is no bulk delete by condition; read keys then batch delete, or use TTL.

## Gotchas
- `BatchGetItem` returns items in no particular order; include the key attributes in the projection and map by key.
- A request with a missing or mismatched key attribute, an item over 400 KB, more than 25 requests or more than
  16 MB is rejected as a whole rather than partially processed.
- `BatchGetItem` can return partial results via `UnprocessedKeys` when the 16 MB limit is hit (the API
  reference example: 300 KB items return 52 of 100), when throughput is exceeded, or when more than 1 MB per
  partition is requested.

## Verify
- [ ] Bulk loader logs zero unprocessed items left; item count matches source.
- [ ] Load test shows throttling handled by retries without data loss.
- [ ] Initial bulk loads into a new table considered for import from S3.

## Checked
Checked 2026-10-24 against the DynamoDB API Reference for BatchWriteItem and BatchGetItem, the Transactions page,
the botocore DynamoDB model and boto3 `table.py`. Confirmed: 25 requests / 16 MB / 400 KB per item for writes;
100 items / 16 MB for gets; unprocessed items and the recommendation for exponential backoff; duplicate-key
rejection; no conditions or updates in BatchWriteItem; `ConsistentRead` per table; partial results and the
1 MB-per-partition cause; TransactWriteItems 100 actions and 4 MB; `BatchExecuteStatement` batch size 25;
`ImportTable` input formats CSV, DYNAMODB_JSON, ION; `batch_writer(overwrite_by_pkeys=...)` exists.
Removed unchecked statements: Java SDK helper behaviour, the 2x previous-peak throttling rule, the "no WCU
consumed" claim for S3 import, the 2x cost multiplier wording, and the empty-string-key gotcha.
Method: documentation only; no commands were run.
