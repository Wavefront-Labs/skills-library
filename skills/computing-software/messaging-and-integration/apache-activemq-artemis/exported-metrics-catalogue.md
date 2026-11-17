---
id: computing-software.messaging-and-integration.apache-activemq-artemis.exported-metrics-catalogue
name: exported-metrics-catalogue
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,metrics,artemis-broker-tag,message-count,messages-added,address-memory-usage,consumer-count,activemq-artemis]
level: practitioner
status: docs-checked
description: "Know which broker, address and queue metrics Artemis exports (all tagged with broker) so you can build dashboards and alerts from the Micrometer names."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/metrics.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exported metrics

Every metric carries the `broker` tag (the `<name>` in `broker.xml`); broker-specific metrics are prefixed `artemis.`. Descriptions are exported with the metrics.

## Broker
`connection.count`, `total.connection.count`, `address.memory.usage`, `address.memory.usage.percentage`, `disk.store.usage`, `replica.sync`, `active`, and `authentication.count` / `authorization.count` tagged by `result` (`success` or `failure`).

## Address (tag `address`)
`routed.message.count`, `unrouted.message.count`, `address.size`, `number.of.pages`.

## Queue (tags `address`, `queue`)
`message.count`, `durable.message.count`, `persistent.size`, `delivering.message.count`, `scheduled.message.count` (plus their durable and persistent-size variants), `messages.acknowledged`, `messages.added`, `messages.killed`, `messages.expired`, `consumer.count`.

Totals such as total message count are not exported; aggregate the per-queue `message.count` across queues instead.

Metrics for all addresses and queues are enabled by default; disable them for chosen addresses with the `enable-metrics` address-setting set to `false`.

## Checked

Method: docs-checked 2026-11-09 against metrics.adoc (read in full). Removed the Verify step, alerting ideas and naming claims not on the page.
