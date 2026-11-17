---
id: computing-software.database-administration.cloud-nosql-databases.dynamodb-auto-scaling-and-throttling
name: dynamodb-auto-scaling-and-throttling
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [dynamodb-auto-scaling-and-throttling, dynamodb-capacity, dynamodb, amazon-dynamodb, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Provision with auto scaling and handle throttles with retries."
sources:
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/capacity-mode.html
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Auto scaling and throttling

**Goal:** Provision with auto scaling and handle throttles with retries.

## Steps
- Application Auto Scaling target tracking: register a scalable target for dynamodb:table:WriteCapacityUnits with min/max and a target utilisation of about 70 percent.
- Scaling responds to sustained workload changes over several minutes; bursts above provisioned use unused throughput saved for up to 300 seconds.
- Throttled calls raise ProvisionedThroughputExceededException; AWS SDKs retry with exponential backoff, so tune max attempts.
- Alarm on ThrottledRequests and WriteThrottleEvents.

## Gotcha
Autoscaling reacts to sustained load, not a sharp spike; use on-demand or a higher minimum before known events.

## Verify
- [ ] Alarms are configured and a load test shows throttle events remain at zero or are absorbed by SDK retries.

## Checked
Checked 2026-11-03 against the capacity mode, Application Auto Scaling and GSI online operations pages: 70 percent target utilisation as the docs example, the dynamodb:table:WriteCapacityUnits dimension, several-minute scaling response, 300 seconds of burst capacity, SDK exponential backoff and the ThrottledRequests/WriteThrottleEvents metrics match. Removed "and jitter" and the ReadThrottleEvents alarm name (not on the pages read); resolved the burst "(confirm)".
Method: documentation only; no commands were run.
