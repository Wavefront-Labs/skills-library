---
id: computing-software.messaging-and-integration.apache-kafka.kafka-quota-enforcement
name: kafka-quota-enforcement
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, quota-enforcement, request-percentage, network-bandwidth-quota, throttle-time]
level: advanced
status: docs-checked
description: "Understand how brokers enforce byte-rate and request-rate quotas, precedence order and why quotas are per broker."
sources:
  - https://kafka.apache.org/42/design/design/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: predict how a client quota is matched and enforced.

Two quota types exist: network bandwidth (byte-rate thresholds) and request rate (percentage of request-handler I/O and network thread time). A request quota of n% is n% of one thread, against a total capacity of ((num.io.threads + num.network.threads) * 100)%.

Quota groups are (user, client-id), user, or client-id; the most specific match applies, and all connections in a group share the quota. Precedence, highest first:
1. matching user and client-id
2. matching user and default client-id
3. matching user
4. default user and matching client-id
5. default user and default client-id
6. default user
7. matching client-id
8. default client-id

User and (user, client-id) overrides are written to the metadata log, read by all brokers and effective immediately, with no rolling restart.

Quotas are per broker, not cluster-wide, because sharing usage across brokers would be harder than the quota itself.

On violation the broker computes the delay needed, returns a response carrying it (a fetch response contains no data), and mutes the client channel until the delay ends. Compliant clients also stop sending during the delay. Usage is measured over many small windows (for example 30 windows of 1 second) because large windows cause bursts followed by long delays.

## Checked

2026-11-04: claims, commands, flags and config names confirmed against the Kafka 4.2 Design page (Quotas section). Removed: nothing.

Method: documentation only; no commands were run.
