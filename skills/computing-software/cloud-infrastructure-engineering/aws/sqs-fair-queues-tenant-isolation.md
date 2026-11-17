---
id: computing-software.cloud-infrastructure-engineering.aws.sqs-fair-queues-tenant-isolation
name: sqs-fair-queues-tenant-isolation
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, sqs, fair-queues, tenant-isolation-sqs, noisy-neighbor, multi-tenant, message-group-id, standard-queue, backlog, quiet-tenant-latency, queue-per-tenant, shuffle-sharding, messaging]
level: practitioner
status: docs-checked
description: "Stop one tenant's burst from starving everyone on a shared standard SQS queue: enable fair queues with MessageGroupId per tenant, read the new metrics, and know when queue-per-tenant is still better."
sources: ["https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-fair-queues.html", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-available-cloudwatch-metrics.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQS fair queues for multi-tenant isolation

**Goal:** a shared standard queue where a tenant that dumps 500k messages does not push every
other tenant's 10 messages behind it — without running one queue per tenant.

## 1. What fair queues do
Standard queues accept `MessageGroupId` as a **tenant identifier**. SQS watches the distribution of
in-flight messages per tenant; a tenant with a disproportionately large share in flight is treated as a
noisy neighbour and SQS prioritises returning messages from the other tenants. `MessageGroupId` on a
standard queue does not enforce ordering (use FIFO for that). SQS does not limit the consumption rate per
tenant: consumers still receive noisy-tenant messages when there is spare capacity and nothing else to return.
Throughput stays as for standard queues (virtually unlimited) with no limit on the number of tenants.

Nothing to enable on the queue: fairness is applied automatically to all standard queues for
messages that carry a `MessageGroupId`, with no consumer change and no impact on API latency.

```python
sqs.send_message(QueueUrl=q, MessageBody=body, MessageGroupId=f"tenant-{tenant_id}")
# batch: each entry carries its own MessageGroupId
```

## 2. Choosing the group
- Group = the fairness unit, almost always the **tenant** (or customer, or API key). Too fine
  (per request) defeats the purpose; too coarse (per region) hides the noisy tenant inside a
  big group.
- Consumers do nothing special; they keep calling `ReceiveMessage`.
- Fair queues suit queues that are multi-tenant, high-throughput and sensitive to dwell time (time from
  arrival to processing). At low throughput one tenant's burst rarely hurts the others.

## 3. Metrics to watch
Fair queues add these CloudWatch metrics (`AWS/SQS`, dimension `QueueName`):
`ApproximateNumberOfNoisyGroups`, `ApproximateNumberOfMessagesVisibleInQuietGroups`,
`ApproximateNumberOfMessagesNotVisibleInQuietGroups`, `ApproximateNumberOfMessagesDelayedInQuietGroups`
and `ApproximateAgeOfOldestMessageInQuietGroups`. Each quiet-group metric is a subset of the queue-level
metric that excludes noisy groups.
- `ApproximateNumberOfNoisyGroups` — a noisy tenant is a backlog from one tenant; alert on it to find who.
- Compare `...InQuietGroups` with the queue-level metrics: during one tenant's surge the queue-level backlog
  and age grow while the quiet-group values stay low.
- `ApproximateNumberOfGroupsWithInflightMessages` is documented for FIFO queues only.
- To see which tenant is responsible, AWS suggests CloudWatch Contributor Insights.

## 4. When queue-per-tenant is still right
- Hard isolation requirements (tenant-specific KMS keys, policies, retention, or a tenant
  that must be pausable) — fairness is scheduling, not isolation.
- Very different processing profiles (one tenant needs 10-minute visibility timeouts).
- Premium tiers with guaranteed throughput — fair queues equalise, they do not prioritise.
Hybrid: a shared fair queue for the long tail plus dedicated queues for the top N tenants,
routed by the producer.

## Gotchas
- FIFO semantics are **not** implied: adding `MessageGroupId` to a standard queue does not
  order messages. If you need both ordering and fairness, FIFO queues already give per-group
  isolation (a slow group never blocks others) — at FIFO throughput.
- Fairness is per queue; if tenants also share the downstream database, de-prioritising at
  the queue does not stop a noisy tenant from monopolising the DB — add per-tenant
  concurrency limits in the consumer.

## Verify
- [ ] Load test: tenant A sends 100k messages, then tenant B sends 100; with 10 consumers, B's messages are all processed within seconds rather than after A's backlog.
- [ ] `ApproximateNumberOfNoisyGroups` rises during the burst and returns to 0 after.
- [ ] Per-tenant p99 latency for quiet tenants stays within SLA during the burst.

## Checked

Date 2026-10-23. Documentation release: current Amazon SQS Developer Guide (fair queues, CloudWatch metrics, FIFO pages).
Confirmed: fair queues apply automatically to standard queues via `MessageGroupId`; detection is by in-flight distribution; no ordering; no per-tenant rate limit; no throughput limit; no consumer change; the five fair-queue metric names and quiet-group semantics. Corrected: `ApproximateNumberOfGroupsWithInflightMessages` is FIFO-only, not a fair-queue metric.
Removed (not in docs): shared-group treatment of messages without an ID, group cardinality advice, returning `MessageGroupId` as a receive attribute, Lambda batch mixing, DLQ redrive preserving group ID.
Sources: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-fair-queues.html ; .../sqs-available-cloudwatch-metrics.html

Method: documentation only; no commands were run.
