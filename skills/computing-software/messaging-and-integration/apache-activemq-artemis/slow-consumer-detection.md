---
id: computing-software.messaging-and-integration.apache-activemq-artemis.slow-consumer-detection
name: slow-consumer-detection
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,slow-consumer,slow-consumer-threshold,slow-consumer-policy,slow-consumer-check-period,consumer-slow,activemq-artemis]
level: advanced
status: docs-checked
description: "Detect and kill or notify slow consumers with slow-consumer-threshold, its measurement unit, slow-consumer-policy and slow-consumer-check-period."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/slow-consumers.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Slow consumer detection

**Goal:** stop a slow consumer with a server-side queue (for example a JMS topic subscriber) from filling broker memory and forcing paging. Detection is off by default; enable it through address-settings.

## Settings
- `slow-consumer-threshold`: minimum consumption rate before a consumer is "slow". Default `-1` (disabled); any enabled value should be greater than 0 so the check requires the queue to have messages, and `0` lets a consumer with no messages pending count as slow.
- `slow-consumer-threshold-measurement-unit`: `MESSAGES_PER_SECOND` (default), `MESSAGES_PER_MINUTE`, `MESSAGES_PER_HOUR` or `MESSAGES_PER_DAY`.
- `slow-consumer-policy`: `KILL` kills the consumer's connection (affecting other client threads sharing it); `NOTIFY` sends a `CONSUMER_SLOW` management notification an application can act on.
- `slow-consumer-check-period`: how often to check, in seconds, default `5`.

```xml
<address-setting match="jms.topic.#">
   <slow-consumer-threshold>1</slow-consumer-threshold>
   <slow-consumer-policy>KILL</slow-consumer-policy>
   <slow-consumer-check-period>120</slow-consumer-check-period>
</address-setting>
```

## Rules of thumb from the docs
- Set the check period to at least 2x the maximum time a consumer needs to process one message; with a per-minute unit that means at least 2 x 60 s, i.e. 120 s.
- The calculation counts only messages the consumer has acknowledged; it ignores flow control and large-message streaming.
- Checks run on the scheduled thread pool, one entry per queue with detection enabled, so many queues plus a low check period can delay checks (accuracy is unaffected).

## Checked
2026-11-03. Confirmed against the Artemis user manual pages slow-consumers and address-settings: the four settings, defaults, units, policies and the check-period note. Removed: the Verify step.
Method: documentation only; no commands were run.
