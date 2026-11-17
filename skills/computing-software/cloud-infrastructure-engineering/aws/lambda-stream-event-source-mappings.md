---
id: computing-software.cloud-infrastructure-engineering.aws.lambda-stream-event-source-mappings
name: lambda-stream-event-source-mappings
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, lambda, event-source-mapping, stream-esm, bisect-on-error, parallelization-factor, tumbling-window, kinesis]
level: practitioner
status: docs-checked
description: "Tune Lambda mappings for Kinesis and DynamoDB Streams: batching, parallelization factor, bisect on error, retry caps, partial failures and tumbling windows."
sources: ["https://docs.aws.amazon.com/lambda/latest/dg/with-ddb.html", "https://docs.aws.amazon.com/lambda/latest/dg/services-dynamodb-errors.html", "https://docs.aws.amazon.com/lambda/latest/dg/services-ddb-batchfailurereporting.html", "https://docs.aws.amazon.com/lambda/latest/dg/services-ddb-windows.html", "https://docs.aws.amazon.com/lambda/latest/api/API_CreateEventSourceMapping.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lambda stream event source mappings (Kinesis, DynamoDB Streams)
**The failure mode to prevent:** with default settings a bad record can block the affected shard for up to
one day, because retries and record age default to infinite and Lambda keeps retrying the batch.

## 1. A safe mapping
```bash
aws lambda create-event-source-mapping --function-name processor:live \
  --event-source-arn arn:aws:kinesis:<REGION>:<ACCOUNT_ID>:stream/clicks \
  --starting-position LATEST \
  --batch-size 500 --maximum-batching-window-in-seconds 5 \
  --parallelization-factor 4 \
  --bisect-batch-on-function-error \
  --maximum-retry-attempts 5 --maximum-record-age-in-seconds 3600 \
  --function-response-types ReportBatchItemFailures \
  --destination-config '{"OnFailure":{"Destination":"arn:aws:sqs:<REGION>:<ACCOUNT_ID>:clicks-failed"}}'
```
- **Retries/age**: `MaximumRetryAttempts` (-1 to 10,000) and `MaximumRecordAgeInSeconds` (-1, or 60 to 604,800)
  default to -1 (infinite); cap them. Retries cover function errors; throttles before invocation retry until
  the record expires or exceeds the max age.
- **Bisect**: with `BisectBatchOnFunctionError` a failed batch is split in two to isolate bad records; splits
  do not consume the retry quota.
- **ReportBatchItemFailures**: return `{"batchItemFailures":[{"itemIdentifier":"<SequenceNumber>"}]}`. With
  several failures Lambda checkpoints at the lowest sequence number and retries from there. An empty or null
  list means full success; an empty or null `itemIdentifier` (or a bad key name) means total failure. The
  setting must be turned on in the mapping or the response is ignored.
- **On-failure destination**: SNS, SQS or S3 (or a Kafka topic). It receives a JSON invocation record with
  batch metadata (shard ID, sequence numbers, stream ARN), not the records; for S3 destinations Lambda also writes
  the full invocation record as `payload`. Fetch the records from the stream before they expire. The role needs
  `sqs:SendMessage`, `sns:Publish` or `s3:PutObject` plus `s3:ListBucket`.
- **Parallelization factor** 1 to 10 (default 1): concurrent batches per shard, with records for the same
  partition key kept in order.

## 2. Tumbling windows (stateful aggregation)
`--tumbling-window-in-seconds 120` (0 to 900): the function receives `state` from the previous invocation and must
return `{"state": {...}}` (a response without `state` is a failed invocation). On the final invocation of a window
`isFinalInvokeForWindow` is true and the state is then dropped. State is limited to 1 MB per shard or the window
ends early (`isWindowTerminatedEarly`). Windows do not support resharding.

## 3. Filtering
`--filter-criteria` drops non-matching records before invocation. Kinesis data goes under `data`, DynamoDB
under `dynamodb`.

## 4. DynamoDB Streams specifics
Lambda polls shards 4 times per second at the base rate. Use `TRIM_HORIZON` to avoid missing events during
mapping creation or updates (`LATEST` can miss them). For single-Region tables that are not global tables you can
design for up to two Lambda functions reading the same shard; more can cause throttling (for global tables,
keep to one).

## Gotchas
- `IteratorAge` on the function is the health signal for stream backlog.
- Raising batch size without raising the function timeout can create timeouts that look like poison records.

## Verify
- [ ] Inject a poison record: the shard keeps flowing and the failure record lands in the destination within the retry budget.
- [ ] `aws lambda get-event-source-mapping` shows finite retries/age and ReportBatchItemFailures.

## Checked
Date 2026-10-23. Lambda Developer Guide DynamoDB pages (errors, batch failure reporting, windows) and the CreateEventSourceMapping API
reference. Confirmed: infinite defaults and ranges, bisect behaviour, response syntax and checkpoint rules,
destinations and permissions, destination record is metadata (S3 adds the payload), ParallelizationFactor
1 to 10 and ordering, tumbling window max 900 s, 1 MB state, state requirement, two-reader guidance, 4 polls per
second, LATEST caveat. Wrong in the old text: the S3 destination also receives the payload; tumbling-window
and state details were unqualified. Removed unconfirmed claims: the 24 hour stream record expiry, and the
note that bisect can reorder records.
Method: documentation only; no commands were run.
