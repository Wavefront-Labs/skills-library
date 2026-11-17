---
id: computing-software.messaging-and-integration.apache-pulsar.message-deduplication
name: message-deduplication
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [message-deduplication, broker-deduplication-enabled, set-deduplication, producer-name, send-timeout]
level: practitioner
status: docs-checked
description: "Enable Pulsar broker-side message deduplication at broker, namespace or topic level and configure producers (name, sendTimeout 0) so ordering survives retries."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/cookbooks-deduplication.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make sure a message produced more than once is persisted only once.

Deduplication is disabled by default at broker, namespace and topic level. Enable it in one of three ways: set `brokerDeduplicationEnabled=true` in `broker.conf` and restart (default for all namespaces and topics), or use `pulsar-admin namespaces` or `pulsar-admin topics`. A namespace or topic setting made through the admin CLI overrides the broker default in either direction.

```bash
bin/pulsar-admin namespaces set-deduplication public/default --enable   # or -e
bin/pulsar-admin namespaces set-deduplication public/default --disable  # or -d
```

Other broker.conf parameters (defaults from the page):
- `brokerDeduplicationMaxNumberOfProducers`: producers whose info is stored, default 10000.
- `brokerDeduplicationEntriesInterval`: entries between deduplication snapshots; a larger interval means fewer snapshots but longer topic recovery.
- `brokerDeduplicationSnapshotIntervalSeconds`: time between snapshots, default 120.
- `brokerDeduplicationProducerInactivityTimeoutMinutes`: how long dedup info for a disconnected producer is kept, default 360 (6 hours).

Client requirements: retry until success, otherwise timed-out requests can break ordering. So (1) give every producer a name, because the broker uses the producer name to filter duplicates, and (2) set the send timeout to 0 (no timeout). Java: `newProducer().producerName("producer-1").topic(...).sendTimeout(0, TimeUnit.SECONDS).create()`. Python: `create_producer(topic, producer_name="producer-1", send_timeout_millis=0)`.

Deduplication can affect broker performance during its informational snapshots.

## Checked

2026-11-03. Confirmed against the pulsar-site page cookbooks-deduplication: levels and default, the five broker.conf parameters and defaults, admin commands with `--enable`/`-e` and `--disable`/`-d`, client requirements and the Java and Python snippets. Removed the unsourced tuning advice and the invented Verify step.

Method: documentation only; no commands were run.
