---
id: computing-software.cloud-infrastructure-engineering.aws.dynamodb-capacity-streams-ttl-dax
name: dynamodb-capacity-streams-ttl-dax
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, dynamodb, dynamodb-streams, dax, on-demand-capacity, provisioned-capacity, ttl, time-to-live, auto-scaling, rcu, wcu, throttling, kinesis-data-streams, change-data-capture, cdc, lambda-trigger, global-tables, point-in-time-recovery, pitr, export-to-s3, import-from-s3, table-class, standard-ia, dynamodb-backup, warm-throughput, streams-lambda, kinesis-for-dynamodb, dax-cluster, dax-consistency]
level: practitioner
status: docs-checked
description: "Operate DynamoDB: on-demand vs provisioned with auto scaling, throttle metrics, Streams and Kinesis CDC to Lambda, TTL semantics, DAX caching, global tables, PITR and S3 export/import."
sources: ["https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/switching.capacitymode.html", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/warm-throughput.html", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/metrics-dimensions.html", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ServiceQuotas.html", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transaction-apis.html", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadConsistency.html", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/contributorinsights_HowItWorks.html", "https://github.com/boto/botocore/blob/develop/botocore/data/dynamodb/2012-08-10/service-2.json", "https://github.com/boto/botocore/blob/develop/botocore/data/dax/2017-04-19/service-2.json", "https://github.com/boto/botocore/blob/develop/botocore/data/application-autoscaling/2016-02-06/service-2.json", "https://github.com/boto/botocore/blob/develop/botocore/data/lambda/2015-03-31/service-2.json"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# DynamoDB operations: capacity, Streams, TTL, DAX

**Goal:** a table that never throttles at the traffic you expect, costs the least of the
two capacity modes for that traffic, emits every change to downstream consumers exactly
as needed, expires data on its own, and can be restored to a point in time.
(Key/index design is in `computing-software.cloud-infrastructure-engineering.aws.dynamodb-data-modelling`.)

## 1. Capacity mode
| | On-demand | Provisioned (+ auto scaling) |
|---|---|---|
| Pay for | Per request (read/write request units) | Per provisioned RCU/WCU-hour, whether used or not |
| Scaling | Serves up to the table's warm throughput instantly; warm throughput adjusts as usage grows and can be raised in advance | Auto scaling triggers when consumption breaches the target for two consecutive minutes, then `UpdateTable` takes several minutes, and requests above the old capacity are throttled meanwhile |
| Cost | Compare with the pricing page for your traffic | Cheaper at steady high utilisation; reserved capacity is available |
| Choose when | Spiky, unknown, new tables, dev | Predictable sustained load, cost-sensitive |
```bash
aws dynamodb update-table --table-name app --billing-mode PAY_PER_REQUEST
# or provisioned with auto scaling (table and each GSI separately)
aws dynamodb update-table --table-name app --billing-mode PROVISIONED --provisioned-throughput ReadCapacityUnits=100,WriteCapacityUnits=50
aws application-autoscaling register-scalable-target --service-namespace dynamodb --resource-id table/app \
  --scalable-dimension dynamodb:table:WriteCapacityUnits --min-capacity 50 --max-capacity 2000
aws application-autoscaling put-scaling-policy --service-namespace dynamodb --resource-id table/app \
  --scalable-dimension dynamodb:table:WriteCapacityUnits --policy-name w70 --policy-type TargetTrackingScaling \
  --target-tracking-scaling-policy-configuration '{"TargetValue":70,"PredefinedMetricSpecification":{"PredefinedMetricType":"DynamoDBWriteCapacityUtilization"}}'
```
Index capacity uses `--resource-id table/app/index/<INDEX>` with the `dynamodb:index:WriteCapacityUnits`
dimension.
- Units: a strongly consistent read of up to 4 KB is 1 RCU (an eventually consistent read is half that); a write
  of up to 1 KB is 1 WCU; transactions use two underlying reads or writes per item. A 6 KB item read strongly = 2 RCU.
- Mode switching: provisioned to on-demand up to four times per 24-hour rolling window; on-demand to
  provisioned at any time. A table switched to on-demand for the first time is scaled to at least 4,000 write
  and 12,000 read units per second (or its previous provisioned or peak level if higher). Warm throughput can be
  raised ahead of a launch (`--warm-throughput`); the increase is charged and cannot later be decreased.
- Provisioned decreases are limited: a table or GSI starts each UTC day with 4 decreases available and gains 1
  per hour up to 4, so at most 27 in a full day. Auto scaling scales down when 15 consecutive data points
  are below the target.
- GSIs have their own provisioned capacity; a GSI short of write capacity throttles **table writes**.
  Configure GSI auto scaling too.
- Table class `STANDARD_INFREQUENT_ACCESS` exists alongside `STANDARD`; compare costs on the pricing page.

## 2. Reading throttles
`ThrottledRequests`, `ReadThrottleEvents` / `WriteThrottleEvents` (per table and per GSI via the
`GlobalSecondaryIndexName` dimension), `ConsumedRead/WriteCapacityUnits` (use `Sum` / 60) vs
`ProvisionedRead/WriteCapacityUnits`. Throttle-cause metrics (`...KeyRangeThroughputThrottleEvents` for
partition limits, `...ProvisionedThroughputThrottleEvents`, `...MaxOnDemandThroughputThrottleEvents`,
`...AccountLimitThrottleEvents`) say why. If consumed is well below provisioned and you still throttle: a
**hot key** (the documented per-item ceiling is 1,000 write or 3,000 read units per second); Contributor Insights
(`update-contributor-insights --contributor-insights-action ENABLE`) names the keys. Exhausted SDK retries
surface throttling exceptions to the application.

## 3. Streams and change data capture
- **DynamoDB Streams**: `--stream-specification StreamEnabled=true,StreamViewType=NEW_AND_OLD_IMAGES`
  (other view types: `KEYS_ONLY`, `NEW_IMAGE`, `OLD_IMAGE`). Design for up to two simultaneous readers per shard
  on a single-Region, non-global table (one for global tables). Reading with Lambda:
  `aws lambda create-event-source-mapping --function-name proj --event-source-arn <STREAM_ARN> --starting-position TRIM_HORIZON --batch-size 100 --maximum-batching-window-in-seconds 5 --bisect-batch-on-function-error --maximum-retry-attempts 3 --destination-config '{"OnFailure":{"Destination":"<SQS_ARN>"}}' --function-response-types ReportBatchItemFailures --parallelization-factor 4`
  The retry, bisect, on-failure destination and partial-batch-response options are all event source mapping
  settings; see the Lambda documentation for their exact semantics before relying on them to isolate bad records.
  After a transaction completes its changes propagate gradually: stream records of one transaction can appear at
  different times and interleaved with other transactions, so do not assume transaction atomicity in consumers.
- **Kinesis Data Streams for DynamoDB** (`enable-kinesis-streaming-destination`): delivers change records to a
  Kinesis stream you own. Metrics for it use the `DelegatedOperation` dimension (for example
  `AgeOfOldestUnreplicatedRecord`, `FailedToReplicateRecordCount`).
- Stream records carry `eventName` (`INSERT|MODIFY|REMOVE`), `Keys` and, depending on the view, `NewImage` /
  `OldImage` in DynamoDB JSON; deserialise with the SDK's type deserializer.
- TTL deletions are recorded in the stream as service deletions rather than user deletions, which is the hook
  for archiving expired items instead of losing them.

## 4. TTL
`aws dynamodb update-time-to-live --table-name app --time-to-live-specification Enabled=true,AttributeName=expiresAt`
- The attribute must be a **Number in Unix epoch seconds**; items whose TTL attribute is not a Number are ignored.
- Deletion is a background process that consumes no write throughput; expired items might be deleted at any
  time, typically within a few days after expiry, so **filter expired items on read**
  (`FilterExpression: expiresAt > :now`) because they are still returned until deleted. `TimeToLiveDeletedItemCount`
  tracks deletions.
- You can still update an expired item pending deletion; moving the TTL attribute to a future time (or removing it)
  stops the deletion. Use a condition expression when updating expired items.
- TTL deletes replicate to global tables (version 2019.11.21): the original delete uses no WCU, but each replicated
  delete consumes replicated write units in the replica Regions. Items are removed from local and global secondary
  indexes like other deletes.

## 5. DAX
DynamoDB Accelerator is an in-memory cache cluster managed through the `aws dax` commands; it supports
`TransactWriteItems` and `TransactGetItems` (writes pass through to DynamoDB, and `TransactGetItems` calls are
passed through without caching, as with strongly consistent reads).
```bash
aws dax create-cluster --cluster-name app-dax --node-type <NODE_TYPE> --replication-factor 3 \
  --iam-role-arn arn:aws:iam::<ACCOUNT_ID>:role/dax --subnet-group-name private --security-group-ids sg-dax \
  --cluster-endpoint-encryption-type TLS --parameter-group-name app-dax-pg
```
- `create-cluster` takes the options shown (`NodeType`, `ReplicationFactor`, `IamRoleArn`, `SubnetGroupName`,
  `SecurityGroupIds`, `ClusterEndpointEncryptionType`, `ParameterGroupName`); cache TTL settings live in the
  parameter group.
- Contributor Insights does not show DAX cache responses, only requests that reach the table or index.
- For cache behaviour (item and query cache TTLs, consistency of cached reads, what bypasses the cache), read the
  DAX guide before relying on it; this skill does not restate those details.

## 6. Global tables, backups, export
- **Global tables** (version 2019.11.21): add a replica with
  `aws dynamodb update-table --replica-updates '[{"Create":{"RegionName":"us-east-1"}}]'`. Consistency modes: MREC
  (default, replicates typically within a second) and MRSC (synchronous replication, strongly consistent reads on
  any replica); track `ReplicationLatency` (dimension `ReceivingRegion`). Transactions provide ACID guarantees
  only within the Region where the write API was invoked; replicas can show partially replicated transactions.
- **PITR**: `update-continuous-backups --point-in-time-recovery-specification PointInTimeRecoveryEnabled=true,RecoveryPeriodInDays=35`
  (retention 1-35 days, default 35). `restore-table-to-point-in-time` creates a new table (`--target-table-name`);
  check indexes, auto scaling, TTL, Streams and IAM on the restored table before cutting over.
- **Export to S3** (`export-table-to-point-in-time`) requires PITR; formats `DYNAMODB_JSON` or `ION`.
  **Import from S3** (`import-table`) creates a new table from CSV, DynamoDB JSON or Ion.
- `--deletion-protection-enabled` is available on `create-table` and `update-table`.

## Gotchas
- A Lambda consumer slower than the write rate builds `IteratorAge` on the stream; alarm on it.
- A brand-new table has default warm throughput that grows with usage; pre-warm before a known spike.
- Consumed capacity metrics smooth sub-minute spikes, so a throttled table can look under-utilised.

## Verify
- [ ] Load test at 2x expected peak: `ThrottledRequests` = 0 on table and every GSI; auto scaling (if used) reached target within your agreed time.
- [ ] Stream consumer: `IteratorAge` stays low under load; injecting a bad record sends it to the failure destination without blocking others.
- [ ] Item with `expiresAt` in the past is filtered out by reads immediately and is deleted by TTL within the documented window (typically a few days); the stream shows a service deletion.
- [ ] PITR restore to 5 minutes ago into a new table succeeds and TTL/auto scaling are re-applied by IaC.

## Checked
Checked 2026-10-24 against the DynamoDB guide pages for switching capacity modes, warm throughput, metrics,
Quotas, TTL, Transactions, read consistency and Contributor Insights, plus the botocore models for DynamoDB,
DAX, Application Auto Scaling and Lambda. Corrected: the mode switch is four provisioned-to-on-demand switches
per 24 hours (not once per day); TTL deletion takes typically a few days, not minutes (TTL deletes also consume
replicated write units in global table replicas); DAX does support transactions (the old Gotcha said it does
not); first-switch on-demand levels are described by the capacity-mode page (the old "2x previous peak" rule
is not in it). Confirmed CLI and API parameter names for update-table, update-time-to-live, Application Auto
Scaling (`DynamoDBWriteCapacityUtilization`, `dynamodb:table:WriteCapacityUnits`), Lambda event source
mapping options, DAX create-cluster, global table replica updates, PITR `RecoveryPeriodInDays` 1-35 (default 35)
and export prerequisites. Removed unchecked figures: pricing multipliers, burst-capacity seconds, DAX cache
TTL defaults and hit-rate thresholds, Streams retention and ordering statements, Kinesis retention and
ordering, PITR restore exclusions, the five-year TTL rule and TTL attribute change rule.
Method: documentation only; no commands were run.
