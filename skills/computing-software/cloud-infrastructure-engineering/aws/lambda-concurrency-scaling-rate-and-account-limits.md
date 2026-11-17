---
id: computing-software.cloud-infrastructure-engineering.aws.lambda-concurrency-scaling-rate-and-account-limits
name: lambda-concurrency-scaling-rate-and-account-limits
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, lambda, concurrency-scaling-rate, unreserved-concurrency, account-concurrency, reserved-concurrency, capacity-planning]
level: advanced
status: docs-checked
description: "Plan Lambda concurrency: estimate it from RPS x duration, the 1,000-per-10-seconds scaling rate, account quota and unreserved pool, and partition with reserved concurrency."
sources: ["https://docs.aws.amazon.com/lambda/latest/dg/lambda-concurrency.html", "https://docs.aws.amazon.com/lambda/latest/dg/configuration-concurrency.html", "https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html", "https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-scaling.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lambda concurrency planning

## 1. Estimate concurrency
Concurrency = average requests per second x average request duration in seconds.
200 RPS x 0.3 s = 60 concurrent. 200 RPS x 3 s = 600. Long-running functions consume
concurrency fast; shaving duration (memory tuning, async downstream calls) frees capacity.

## 2. Limits
- **Account concurrency quota**: default 1,000 per Region (new accounts can have reduced quotas that AWS raises
  from usage; check `aws lambda get-account-settings`, fields `AccountLimit.ConcurrentExecutions` and
  `UnreservedConcurrentExecutions`). Increase via Service Quotas; the quotas page lists "tens of thousands".
- **Reservable amount**: Lambda always keeps 100 units unreserved for functions without reserved concurrency,
  so with a 1,000 limit you can reserve at most 900 across all functions.
- **Scaling rate**: for each function in each Region, 1,000 execution environment instances every 10
  seconds (or 10,000 requests per second every 10 seconds), independent of other functions, until the account limit.
  So 0 to 5,000 takes about 50 s; faster bursts are throttled.
- **Requests per second cap**: 10 x the concurrency quota (10,000 RPS at the default 1,000). Sub-100 ms functions
  can hit this before the concurrency limit.

## 3. Reserved concurrency (partitioning)
```bash
aws lambda put-function-concurrency --function-name payments --reserved-concurrent-executions 300
aws lambda get-function-concurrency --function-name payments
aws lambda delete-function-concurrency --function-name payments
```
- Acts as both a floor and a ceiling: 300 are exclusively available to the function and it cannot exceed 300.
- Protects critical functions from noisy neighbours and downstream systems (a database that tolerates 100
  connections: cap the writer function at 100).
- Setting 0 intentionally throttles the function: it processes no events until the limit is removed.
- No charge.

## 4. Provisioned concurrency (warm capacity)
Pre-initialised environments (configured on versions and aliases) that remove cold starts for that
amount; it costs extra and counts toward your account limit and Regional quotas. Lambda can allocate up to 6,000
provisioned environments per function per minute, and none are usable until the whole request is allocated.
Application Auto Scaling can schedule or target-track it. You cannot allocate more provisioned than reserved
concurrency when both are set; if provisioned on versions and aliases adds up to the reserved amount, `$LATEST`
is throttled.

## 5. Monitoring
- `ConcurrentExecutions` per function (the metric AWS names for estimating reserved concurrency), `Throttles`,
  and `ProvisionedConcurrencySpilloverInvocations` for traffic beyond provisioned capacity.
- Alarm on account concurrency usage before it reaches the quota (for example at 80%).

## 6. Event sources and concurrency
- SQS standard queue mappings start with five concurrent invocations and add up to 300 more per minute, to a
  maximum of 1,250 per mapping. Use `MaximumConcurrency` (2 to 1,000) on the mapping to limit consumption
  without throttled-message retries. Keep reserved concurrency at or above the sum of `MaximumConcurrency` across
  the function's SQS mappings, or messages can be throttled. Provisioned mode and `MaximumConcurrency` are
  mutually exclusive; provisioned mode scales to 100,000 concurrent invocations.
- Kinesis and DynamoDB streams: concurrency is shards x `ParallelizationFactor` (1 to 10).
- Amazon MQ mappings are fixed at 5 (ActiveMQ) or 1 (RabbitMQ) concurrent environments regardless of reserved
  or provisioned concurrency.

## Gotchas
- A reserved concurrency limit lower than an SQS consumer needs causes throttles; messages return to the queue and
  their receive count rises toward the DLQ threshold. Use `MaximumConcurrency` instead.
- Concurrency quota is per Region; multi-Region failover adds demand in the target Region.

## Verify
- [ ] Peak estimated concurrency per function documented and under the account quota with headroom.
- [ ] Critical functions have reserved concurrency; downstream-sensitive functions are capped.
- [ ] An account-level concurrency alarm exists.

## Checked
Date 2026-10-23. Lambda Developer Guide: scaling, reserved concurrency, quotas and SQS scaling pages.
Confirmed: the concurrency formula, 1,000 default quota, 100 always unreserved (900 reservable), 1,000 per 10 s per
function scaling rate, 10x RPS cap, reserved concurrency as floor and cap, 0 to throttle, no charge, provisioned
concurrency rules and 6,000 per minute allocation, SQS 5 + 300 per minute to 1,250, MaximumConcurrency 2 to 1,000,
mutual exclusion with provisioned mode, ParallelizationFactor range, MQ concurrency. Wrong in the old text: SQS
scaling was "60 per minute" (documented 300), and it stated provisioned concurrency is exempt from the scaling
ramp (documented 6,000 per minute allocation). Removed unconfirmed target-tracking value, 6 hour async retry
claim and the SnapStart remark.
Method: documentation only; no commands were run.
