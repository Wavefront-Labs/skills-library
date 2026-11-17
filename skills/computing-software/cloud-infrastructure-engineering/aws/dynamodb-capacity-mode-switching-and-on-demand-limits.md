---
id: computing-software.cloud-infrastructure-engineering.aws.dynamodb-capacity-mode-switching-and-on-demand-limits
name: dynamodb-capacity-mode-switching-and-on-demand-limits
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, dynamodb, capacity-mode-switch, on-demand-throughput-limit, warm-throughput, on-demand]
level: advanced
status: docs-checked
description: "Switch DynamoDB tables between provisioned and on-demand safely, cap on-demand spend with maximum throughput, and pre-warm with warm throughput before launches."
sources: ["https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/switching.capacitymode.html", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/on-demand-capacity-mode-max-throughput.html", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/warm-throughput.html", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/metrics-dimensions.html", "https://github.com/boto/botocore/blob/develop/botocore/data/dynamodb/2012-08-10/service-2.json"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Switching capacity modes and on-demand maximum throughput

## 1. Switch
```bash
aws dynamodb update-table --table-name orders --billing-mode PAY_PER_REQUEST
aws dynamodb update-table --table-name orders --billing-mode PROVISIONED \
  --provisioned-throughput ReadCapacityUnits=500,WriteCapacityUnits=200 \
  --global-secondary-index-updates '[{"Update":{"IndexName":"GSI1","ProvisionedThroughput":{"ReadCapacityUnits":100,"WriteCapacityUnits":200}}}]'
```
- Provisioned to on-demand: up to four switches in a 24-hour rolling window. On-demand to provisioned: any time.
- Going to on-demand takes several minutes; during the switch the table delivers throughput consistent with its
  previously provisioned capacity. Through the AWS CLI or SDK, existing auto scaling settings are preserved
  (the console deletes them) and apply again when you return to provisioned mode.
- Going to provisioned: the table delivers throughput consistent with the previous peak reached in on-demand mode.
  Choose provisioned values (table and every GSI) from CloudWatch `ConsumedReadCapacityUnits` /
  `ConsumedWriteCapacityUnits`, and set them high enough for the transition. For the console the
  documented auto scaling suggestion is 70% target utilisation, minimum 5 units, maximum the Region maximum.
- First switch to on-demand: a table provisioned below 4,000 WCU / 12,000 RCU (and never provisioned higher)
  is scaled to sustain at least 4,000 write units/s and 12,000 read units/s; a table that had a higher
  provisioned or previous peak keeps at least that level.

## 2. When each mode wins
| Traffic | Mode |
|---|---|
| Spiky, unpredictable, new | on-demand |
| Steady and predictable | provisioned + auto scaling (reserved capacity is also available); compare against the pricing page |

## 3. Cap on-demand
```bash
aws dynamodb update-table --table-name orders \
  --on-demand-throughput MaxReadRequestUnits=20000,MaxWriteRequestUnits=5000
```
Requests above the cap are throttled with `ThrottlingException`: protects against runaway cost (bug loops) and
downstream systems fed by streams. The cap is best effort, so burst capacity can let some traffic through. Reads
and writes are set independently, per table and per GSI; the minimum is 1 request unit per second, and the cap
must be below the default on-demand table-level quota (40,000 read and write request units). Setting `-1` removes
a cap. Watch the CloudWatch metrics `OnDemandMaxReadRequestUnits` and `OnDemandMaxWriteRequestUnits`.

## 4. Warm throughput
```bash
aws dynamodb update-table --table-name orders --warm-throughput ReadUnitsPerSecond=50000,WriteUnitsPerSecond=20000
aws dynamodb describe-table --table-name orders --query 'Table.WarmThroughput'
```
Warm throughput is what a table or GSI can instantaneously support; defaults are visible for every table at no
cost and adjust with usage. Raising it proactively (pre-warming) for a launch is charged, can be done for
tables, GSIs and global tables, cannot later be decreased, and does not change the billing mode. The time to
complete depends on the values and the size of the table or index.

## Verify
- [ ] Throttle alarms (`ThrottledRequests`, `ReadThrottleEvents`, `WriteThrottleEvents`) quiet after the change; cost tracked for a week.

## Checked
Checked 2026-10-24 against the DynamoDB Developer Guide pages for switching capacity modes, maximum throughput
for on-demand tables, warm throughput and CloudWatch metrics, plus the botocore model. Corrected: the old text
said switching is limited to a few times per day (the real rule is four provisioned-to-on-demand switches per
24 hours, on-demand-to-provisioned any time), said auto scaling policies are not carried over (CLI/SDK
preserve them), and said warm throughput is a one-time charge set days ahead (it is charged when raised and cannot
be lowered). Confirmed parameter names `OnDemandThroughput` (`MaxReadRequestUnits`/`MaxWriteRequestUnits`) and
`WarmThroughput` (`ReadUnitsPerSecond`/`WriteUnitsPerSecond`) in the service model, including `-1` to remove a
cap and `Table.WarmThroughput` in `DescribeTable`. Removed the unchecked 30% utilisation crossover figure.
Method: documentation only; no commands were run.
