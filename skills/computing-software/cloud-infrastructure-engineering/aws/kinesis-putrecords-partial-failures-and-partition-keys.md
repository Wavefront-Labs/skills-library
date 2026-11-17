---
id: computing-software.cloud-infrastructure-engineering.aws.kinesis-putrecords-partial-failures-and-partition-keys
name: kinesis-putrecords-partial-failures-and-partition-keys
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, kinesis-data-streams, putrecords, partition-key-design, failedrecordcount, producer-retries, ordering]
level: advanced
status: docs-checked
description: "Write to Kinesis Data Streams reliably: PutRecords partial failures and retry loops, partition key design for spread vs ordering, per-shard limits, and producer metrics."
sources: ["https://docs.aws.amazon.com/streams/latest/dev/service-sizes-and-limits.html", "https://docs.aws.amazon.com/kinesis/latest/APIReference/API_PutRecords.html", "https://docs.aws.amazon.com/streams/latest/dev/monitoring-with-cloudwatch.html", "https://docs.aws.amazon.com/streams/latest/dev/monitoring-with-kpl.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kinesis PutRecords partial failures and partition keys

## 1. Limits per shard
Writes: 1,000 records/s and 1 MB/s per shard (provisioned mode); reads via `GetRecords`: 2 MB/s
per shard, shared by all shared-throughput consumers. The payload of one record (before base64) can
be up to 10 MiB; Kinesis handles intermittent records of 1-10 MiB with burst capacity.
`PutRecords`: up to 500 records per call, up to 10 MiB for the whole request including
partition keys.
New on-demand streams start at 4 MB/s write and 8 MB/s read and scale automatically.

## 2. PutRecords is not all-or-nothing
The call returns HTTP 200 with `FailedRecordCount` and per-record `ErrorCode`
(for example `ProvisionedThroughputExceededException` or `InternalFailure`).
Retry only the failed records, with backoff:
```python
import random, time
def put_all(kinesis, stream, records):          # records: [{"Data": b, "PartitionKey": k}]
    pending, attempt = records, 0
    while pending:
        resp = kinesis.put_records(StreamName=stream, Records=pending)
        if resp["FailedRecordCount"] == 0:
            return
        pending = [r for r, res in zip(pending, resp["Records"]) if "ErrorCode" in res]
        attempt += 1
        if attempt > 8:
            raise RuntimeError(f"{len(pending)} records failed after retries")
        time.sleep(min(5, 0.1 * 2 ** attempt) * random.random())
```
Order of results matches order of input. `PutRecords` does not guarantee record ordering, and
retried records lose relative ordering with records that succeeded in between; if strict
ordering per key matters, use `PutRecord` (with `SequenceNumberForOrdering`).

## 3. Partition key design
The MD5 hash of the partition key picks the shard.
- **Spread**: high-cardinality keys (request ID, user ID among many users) distribute evenly.
- **Ordering**: records with the same key go to the same shard in order; choose the entity
  that needs ordering (order ID, device ID), not something coarse (country, event type).
- Hot keys: one tenant producing most traffic overloads a shard. Add a suffix
  (`tenant#<0-N>`) when per-tenant global order is not needed, or give the hot tenant its
  own stream.
- Random keys (`uuid4()`) give perfect spread but no ordering.
- `ExplicitHashKey` pins a record to a hash range (advanced, for manual balancing).

## 4. Producer-side metrics
- Stream metrics: `PutRecords.FailedRecords`, `PutRecords.ThrottledRecords`,
  `WriteProvisionedThroughputExceeded`, `IncomingBytes`, `IncomingRecords`.
- Enable **enhanced shard-level metrics** (`enable-enhanced-monitoring --shard-level-metrics
  IncomingBytes WriteProvisionedThroughputExceeded`) to find the hot shard, then map
  partition keys to it.
- The Kinesis Producer Library publishes its own metrics (`UserRecordsPut`, `BufferingTime`, `RetriesPerRecord`).

## 5. Options to reduce throttling
More shards (or on-demand), better keys, KPL aggregation (many user records in one Kinesis
record, de-aggregated by KCL/Lambda), compression of payloads, batching up to the 500-record and 10 MiB
limits per call.

## Verify
- [ ] Producer code inspects `FailedRecordCount` and retries; load test shows zero dropped records.
- [ ] Shard-level metrics show balanced `IncomingBytes` across shards.
- [ ] Ordering requirements documented per partition key choice.

## Checked

2026-10-27, AWS documentation (current release as read on that date). Kinesis quotas page, PutRecords API reference, CloudWatch and KPL metrics pages, EnableEnhancedMonitoring reference. Fixed: PutRecords limit is 10 MiB per request (not 5 MB) and a record can be up to 10 MiB (not 1 MB). Confirmed: 500 records per call, 1 MB/s and 1,000 records/s per shard writes, 2 MB/s per shard reads, FailedRecordCount and per-record ErrorCode, MD5 partition key mapping, ExplicitHashKey, PutRecords.FailedRecords and PutRecords.ThrottledRecords, shard-level metric names, KPL metric names. Removed the unsourced enhanced fan-out figure and the on-demand hot-key claim.
Method: documentation only; no commands were run.
