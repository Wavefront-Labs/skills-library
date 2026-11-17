---
id: computing-software.cloud-infrastructure-engineering.aws.dynamodb-monitoring-and-contributor-insights
name: dynamodb-monitoring-and-contributor-insights
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, dynamodb, contributor-insights-dynamodb, throttled-requests, hot-keys, cloudwatch-metrics, successfulrequestlatency]
level: practitioner
status: docs-checked
description: "Monitor DynamoDB: the metrics and alarms that matter (throttles, latency, consumed vs provisioned, system errors) and CloudWatch Contributor Insights to find hot keys."
sources: ["https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/metrics-dimensions.html", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/contributorinsights_HowItWorks.html", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/on-demand-capacity-mode-max-throughput.html", "https://github.com/boto/botocore/blob/develop/botocore/data/dynamodb/2012-08-10/service-2.json"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DynamoDB monitoring and Contributor Insights

## 1. Metrics and alarms (namespace `AWS/DynamoDB`)
| Metric | Alarm idea |
|---|---|
| `ThrottledRequests` (dimensions `TableName`, `Operation`) and `ReadThrottleEvents` / `WriteThrottleEvents` (table, and per GSI with `GlobalSecondaryIndexName`) | > 0 sustained |
| `ConsumedReadCapacityUnits` / `ConsumedWriteCapacityUnits` (use `Sum` / 60) vs `ProvisionedReadCapacityUnits` / `ProvisionedWriteCapacityUnits` | consumed above a chosen share of provisioned (provisioned mode) |
| `SuccessfulRequestLatency` (by `Operation`; percentile statistics such as p99 can be typed into CloudWatch) | p99 above your SLO |
| `SystemErrors` (HTTP 500; publish only on `TableName` + `Operation`, so alarm on both dimensions) | > 0 |
| `UserErrors` (HTTP 400, account/Region level; excludes throttles and failed conditional writes) | spikes (validation or permission bugs in clients) |
| `ConditionalCheckFailedRequests` | unexpected rise (concurrency conflicts) |
| `TransactionConflict` | rise (competing transactions on the same items) |
| `ReplicationLatency` (global tables, dimension `ReceivingRegion`) | sustained high values |
| `AccountProvisionedReadCapacityUtilization` | near account quota |
| `OnDemandMaxReadRequestUnits` / `OnDemandMaxWriteRequestUnits` | when using on-demand max throughput limits |
Consumed capacity metrics are aggregated per minute: divide the `Sum` by 60 for units per second (short spikes
inside a minute are smoothed out). Throttle-cause metrics also exist, for example
`ReadKeyRangeThroughputThrottleEvents` / `WriteKeyRangeThroughputThrottleEvents` (partition limits),
`...ProvisionedThroughputThrottleEvents`, `...MaxOnDemandThroughputThrottleEvents` and `...AccountLimitThrottleEvents`.
Client side: log `ConsumedCapacity` (`ReturnConsumedCapacity=TOTAL`) for expensive queries.

## 2. Contributor Insights
Shows the most accessed and most throttled **partition keys** (and partition+sort key pairs) for a table or GSI.
```bash
aws dynamodb update-contributor-insights --table-name orders --contributor-insights-action ENABLE
aws dynamodb update-contributor-insights --table-name orders --index-name byCustomer --contributor-insights-action ENABLE
aws dynamodb update-contributor-insights --table-name orders --contributor-insights-action ENABLE \
  --contributor-insights-mode THROTTLED_KEYS
aws dynamodb describe-contributor-insights --table-name orders
```
Modes: `ACCESSED_AND_THROTTLED_KEYS` and `THROTTLED_KEYS` (throttled only, which processes events only when
throttling occurs and is the cheaper option to leave on continuously). DynamoDB creates CloudWatch rules named
`DynamoDBContributorInsights-PKC-<name>-<timestamp>` (most accessed partition keys),
`...-PKT-...` (most throttled partition keys) and, for tables or indexes with sort keys, `...-SKC-...`
(most accessed partition+sort keys) and `...-SKT-...` (most throttled partition+sort keys). You cannot edit
or delete these rules directly; disabling the feature removes them. A report returns at most 25 contributors.
Billing is a fixed monthly charge per rule plus a charge per event processed (in accessed-and-throttled mode every
item read or written is an event; a `Query` is always one event), so enable it on hot tables or while investigating.

## 3. Reading the results
- One key dominates accesses: hot item or partition key. Options: write sharding, caching (DAX or
  ElastiCache) for reads, splitting the entity.
- The throttled-keys graph names the keys hitting limits (the documented per-item ceiling is 1,000 write units
  or 3,000 read units per second). Write throttling caused by short GSI write capacity is not measured by it.
- Correlate with application logs by key to find the noisy tenant.
- Contributor Insights does not show DAX cache hits and does not support PartiQL requests. Primary key values
  are published to CloudWatch, so skip it for tables whose keys are sensitive.

## 4. Dashboards
Per table: requests by operation, latency p50/p99, throttles, consumed vs provisioned, plus top keys from
Contributor Insights.

## Gotchas
- Throttling at table level with plenty of capacity usually means hot keys or GSI
  back-pressure, not under-provisioning.
- `ThrottledRequests` is incremented per request only if an event in it is throttled; for batch requests it
  increments only when every request in the batch is throttled, so compare it with `ReadThrottleEvents` and
  `WriteThrottleEvents`.
- `SuccessfulRequestLatency` is server-side only; client latency includes network and retries.

## Verify
- [ ] Alarms exist for throttles, system errors, latency p99 and (provisioned) utilisation per critical table.
- [ ] Contributor Insights enabled on tables with known skew; top keys reviewed.
- [ ] Hot key remediation reduced throttled-key events to zero.

## Checked
Checked 2026-10-24 against the DynamoDB guide pages "DynamoDB Metrics and dimensions" and "CloudWatch
Contributor Insights for DynamoDB: How it works", plus the botocore model. Corrected a swapped rule description:
the old text said `PKT` is most accessed and `PKC` is throttled, but the page defines `PKC` as most accessed and
`PKT` as most throttled (and adds `SKC`/`SKT`). Confirmed metric names, units, dimensions and the
`SystemErrors` dimension note; the two modes and the `THROTTLED_KEYS` / `ACCESSED_AND_THROTTLED_KEYS` API
values; billing structure; the 25-contributor limit; `describe-contributor-insights` operation exists.
Removed the unchecked "GetItem typically single-digit ms" and automatic service-dashboard claims.
Method: documentation only; no commands were run.
