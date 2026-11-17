---
id: computing-software.database-administration.cloud-nosql-databases.dynamodb-on-demand-vs-provisioned
name: dynamodb-on-demand-vs-provisioned
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [dynamodb-on-demand-vs-provisioned, dynamodb-capacity, dynamodb, amazon-dynamodb, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Pick the billing mode that fits traffic shape and change it deliberately."
sources:
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/capacity-mode.html
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-switching-capacity-modes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# On-demand versus provisioned capacity

**Goal:** Pick the billing mode that fits traffic shape and change it deliberately.

## Steps
- On-demand (PAY_PER_REQUEST) bills per request and instantly accommodates up to double the previous peak traffic; good for spiky or unknown load. Growing past double the previous peak within 30 minutes can throttle.
- Provisioned bills per RCU/WCU-hour and suits steady, predictable load.
- Switching provisioned to on-demand is limited to four times in a rolling 24-hour window; on-demand to provisioned can be done at any time.
- 1 RCU = one strongly consistent 4 KB read per second (two eventually consistent); 1 WCU = one 1 KB write per second; transactional operations cost double.

## Gotcha
On-demand can cost more than provisioned for steady heavy traffic; review the bill after a month.

## Verify
- [ ] ConsumedRead/WriteCapacityUnits compared with cost shows the chosen mode is the cheaper one for the workload.

## Checked
Checked 2026-11-03 against the capacity mode and switching pages: previous-peak doubling and the 30-minute caveat, read/write unit definitions and transactional double cost match. Fixed the switch limit (it was "about once per 24 hours"; the docs allow four provisioned-to-on-demand switches per rolling 24 hours, and on-demand to provisioned any time). Removed the unconfirmed reserved-capacity and "several times more" cost claims.
Method: documentation only; no commands were run.
