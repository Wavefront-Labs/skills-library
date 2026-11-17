---
id: computing-software.messaging-and-integration.apache-pulsar.dispatch-throttling
name: dispatch-throttling
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [dispatch-throttling, dispatch-rate, rate-period-in-second, precise-dispatcher-flow-control, throttling-levels]
level: practitioner
status: docs-checked
description: "Rate-limit Pulsar message dispatch per broker, topic or subscription: broker.conf keys, policy priority, the two mutually exclusive accuracy flags and over-delivery limits."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/concepts-throttling.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: protect BookKeeper, brokers and slow clients from backlog-drain surges by capping delivery rate.

How it works: the broker estimates how many entries to read from bookies from the remaining quota, reads, dispatches, then decrements the counter; a scheduled task refreshes the quota at the end of each throttling period. The quota cannot be reduced before dispatch because the broker does not know messages per entry or entry size until it reads. `seek` and redeliveries are counted as new messages.

Levels: per broker (all subscriptions share the quota), per topic (shared by its subscriptions; for partitioned topics the quota applies per partition, so the effective topic limit is N times the configured one for N partitions), per subscription. Limits at several levels apply together (logical AND).

Where to set it:
- broker.conf (or dynamic broker config): `dispatchThrottlingRateInMsg`, `dispatchThrottlingRateInByte`, with topic-level `dispatchThrottlingRatePerTopicInMsg`/`...InByte` and subscription-level `dispatchThrottlingRatePerSubscriptionInMsg`/`...InByte`.
- Namespace policies and topic policies, via the admin API.
Priority: topic policies over namespace policies over broker configuration.

Other keys: `ratePeriodInSecond` (counter reset interval; for 10,000 messages per minute set the period to 60), `preciseDispatcherFlowControl` (considers messages per entry when reading from bookies), `dispatchThrottlingOnBatchMessageEnabled` (counts by entry/batch, ignoring messages per entry, at the cost of an inaccurate message count but higher throughput), `dispatchThrottlingOnNonBacklogConsumerEnabled` (enabled by default).

Gotcha: enable only one of `preciseDispatcherFlowControl` and `dispatchThrottlingOnBatchMessageEnabled`; they are mutually exclusive. Throttling can still over-deliver because the broker may read more entries or bytes than the limit before counting.

Verify: set a low message rate on one subscription and measure consumer receive rate over a few periods.

## Checked

Method: docs-checked 2026-11-09 against pulsar-site docs/concepts-throttling.md (read in full)
