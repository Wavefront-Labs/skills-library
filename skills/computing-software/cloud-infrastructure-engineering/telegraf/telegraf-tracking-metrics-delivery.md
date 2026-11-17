---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-tracking-metrics-delivery
name: telegraf-tracking-metrics-delivery
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [tracking-metrics, max-undelivered-messages, delivery, kafka, mqtt]
level: practitioner
status: docs-checked
description: "Covers tracking metrics, which delay acknowledging queue-based inputs until the output has the data, and the max_undelivered_messages setting. Use for MQTT, Kafka or AMQP inputs."
sources: ["https://docs.influxdata.com/telegraf/v1/concepts/metrics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tracking metrics and delivery acknowledgement

Tracking metrics make sure data is passed from an input and handed to an output before Telegraf acknowledges the message back to the input. Use them with queue-based sources so a message is not removed from the source before it has reached the destination.

For example, with an MQTT, Kafka or AMQP input, Telegraf reads the message and waits until the metric is handed to the output before telling the source it was read. If Telegraf stops or the host crashes, messages that were not completely delivered are re-read later.

## Limits

Acknowledgement applies only to internal plugins. For external plugins, Telegraf acknowledges metrics regardless of what the actual output did.

## max_undelivered_messages

An input that uses tracking metrics exposes `max_undelivered_messages`. It sets how many messages Telegraf reads before it requires acknowledgements. In practice Telegraf may not read new messages at every collection interval.

Be careful with large values. Setting it too high can make Telegraf push constant batches to an output and ignore the flush interval.

## Checked

2026-11-03. Confirmed against docs-v2 Telegraf v1 pages (influxdata/docs-v2 source on GitHub): Metrics concepts page, Tracking metrics and Undelivered messages sections. Removed: the closing remark about the disk buffer strategy, which the page does not state in that context.

Method: documentation only; no commands were run.
