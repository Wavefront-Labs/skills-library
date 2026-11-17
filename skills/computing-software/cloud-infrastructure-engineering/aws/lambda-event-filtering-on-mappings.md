---
id: computing-software.cloud-infrastructure-engineering.aws.lambda-event-filtering-on-mappings
name: lambda-event-filtering-on-mappings
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, lambda, event-filtering, filter-criteria, event-source-mapping, sqs, dynamodb-streams, cost-optimization]
level: practitioner
status: docs-checked
description: "Filter events before Lambda runs with FilterCriteria on SQS, Kinesis, DynamoDB Streams, MQ and Kafka mappings: per-source keys, OR logic and the SQS deletion gotcha."
sources: ["https://docs.aws.amazon.com/lambda/latest/dg/invocation-eventfiltering.html", "https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-event-patterns.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lambda event filtering on event source mappings

**Goal:** stop paying for (and coding around) invocations that immediately return because the
event isn't interesting.

## 1. Syntax
Filters use EventBridge pattern syntax. By default a mapping can have 5 filters (a quota increase allows up to
10). Filters are ORed: a record that satisfies any filter is passed on. Multiple fields inside one pattern are
ANDed. Event filtering is not supported for DocumentDB.
```bash
aws lambda update-event-source-mapping --uuid "$UUID" --filter-criteria '{"Filters":[
  {"Pattern":"{\"body\":{\"type\":[\"order.created\"],\"amount\":[{\"numeric\":[\">\",100]}]}}"},
  {"Pattern":"{\"body\":{\"priority\":[\"high\"]}}"}]}'
```
Remove all filters with `--filter-criteria "{}"`.

## 2. Where the data lives per source
| Source | Data key to filter on |
|---|---|
| SQS | `body` (plus metadata such as `attributes`, `messageAttributes`) |
| Kinesis | `data` |
| DynamoDB Streams | `dynamodb` (for example `dynamodb.NewImage.status.S`), plus metadata such as `eventName` |
| MSK / self-managed Kafka | `value` |
| Amazon MQ | `data` |
DynamoDB example, only inserts where status = PENDING:
```json
{"eventName": ["INSERT"], "dynamodb": {"NewImage": {"status": {"S": ["PENDING"]}}}}
```
Supported operators: null, empty, equals, `equals-ignore-case`, `anything-but`, `numeric`, `exists`,
`prefix`, `suffix` and `$or`. Strings match exactly character by character, and numbers match on their string
form (300, 300.0 and 3.0e2 are not equal). `exists` works only on leaf nodes.

## 3. What happens to records that do not match
- **SQS**: Lambda removes non-matching messages from the queue. If another consumer needs them, filtering
  here loses data; use separate queues with SNS filter policies instead.
- **Kinesis and DynamoDB**: the iterator advances past the record; the record just ages out of the stream.
- **MSK, self-managed Kafka**: non-matching messages are dropped and offsets are committed. **Amazon MQ**:
  unmatched messages are acknowledged when filtered.

## 4. Testing patterns
```bash
aws events test-event-pattern --event-pattern '{"body":{"type":["order.created"]}}' \
  --event '{"id":"1","source":"x","detail-type":"x","account":"1","time":"2026-10-16T00:00:00Z","region":"eu-west-1","resources":[],"body":{"type":"order.created"}}'
```
(EventBridge's tester needs its envelope fields; Lambda uses the same pattern syntax.)

## Gotchas
- Patterns on an SQS `body` apply to JSON bodies; keep the body valid JSON.
- Filter criteria can be encrypted with a customer managed KMS key (`--kms-key-arn`); then list calls show
  `FilterCriteria` as null and you need `kms:Decrypt` to read it with get-event-source-mapping.

## Verify
- [ ] Send one matching and one non-matching event; only one invocation recorded.
- [ ] For SQS, confirm non-matching messages were intended to be dropped (no other consumer).
- [ ] Invocation count/cost drops in line with the expected filter ratio.

## Checked
Date 2026-10-23. Lambda Developer Guide, event filtering page (current release). Confirmed: default 5 filters and
increase to 10, OR across filters, per-source data keys (MQ is `data`, Kafka `value`), operator list, SQS
removal versus stream and Kafka and MQ behaviour, CLI syntax and empty `{}` to remove, KMS encryption, no
DocumentDB support. Wrong in the old text: Amazon MQ key was listed as `value` (documented `data`); filter
metrics `FilteredOutEventCount` and the "changes apply within minutes" note were removed as unconfirmed.
Method: documentation only; no commands were run.
