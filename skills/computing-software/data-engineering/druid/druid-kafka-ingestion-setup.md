---
id: computing-software.data-engineering.druid.druid-kafka-ingestion-setup
name: druid-kafka-ingestion-setup
category: computing-software
field: data-engineering
product: druid
tags: [kafka, kafka-indexing-service, exactly-once, extension, offsets]
level: practitioner
status: docs-checked
description: "Enable the Kafka indexing service and submit a Kafka supervisor."
sources:
  - https://github.com/apache/druid/blob/master/docs/ingestion/kafka-ingestion.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Kafka indexing service needs Apache Kafka 0.11.x or higher. Enabling it lets you configure supervisors on the Overlord that manage the creation and lifetime of Kafka indexing tasks.

Tasks read events by Kafka partition and offset, which is how Druid guarantees exactly-once ingestion. The supervisor oversees the tasks, coordinating handoffs, handling failures and keeping scalability and replication targets.

Setup: load the `druid-kafka-indexing-service` extension on both the Overlord and the Middle Manager. Then submit a supervisor spec whose `type` is `kafka`. The example in the docs sets a `dataSchema` with `dataSource` (for example `metrics-kafka`), a `timestampSpec` with column `timestamp` and format `auto`, a `dimensionsSpec` including `dimensionExclusions` for the timestamp and value columns, and a `metricsSpec`. Properties shared with other streaming methods are in the supervisor spec reference; only Kafka-specific ones are on the Kafka page.

Kafka-specific `ioConfig` properties from the page:
- `topic` (required unless `topicPattern` is set; cannot be changed once established) or `topicPattern`, a regex for multiple topics (for example `clicks|impressions`; partial matches such as `my-metrics-12` for `metrics-.*` are not included). Migrating an existing supervisor between `topic` and `topicPattern` is not supported; suspend, reset offsets and resubmit to force it. Enabling multi-topic ingestion means downgrading to a version older than 28.0.0 fails that datasource.
- `consumerProperties` (required, at minimum `bootstrap.servers`).
- `partitionIds`: optional non-empty set of non-negative partition IDs for a single topic; null (default) reads all partitions; cannot combine with `topicPattern`.
- `pollTimeout`: milliseconds, default 100.
- `useEarliestOffset`: default false; only used on the first run of a supervisor for a datasource.
- `headerBasedFilterConfig` and `idleConfig` (experimental; `enabled`, `inactiveAfterMillis`): default null.

Consumer notes: Druid defaults `isolation.level` to `read_committed` (standard Kafka consumers default to `read_uncommitted`); setting `read_uncommitted` removes Druid's offset gap check. Set `group.id` in `consumerProperties` if consumer group ACLs are enabled. For SSL or SASL secrets use the environment-variable dynamic config provider (`druid.dynamic.config.provider` with `"type": "environment"`), not plain text.

Kafka metadata can be ingested with the `kafka` input format (`valueFormat`, `headerFormat`, `keyFormat`, and column names defaulting to `kafka.timestamp`, `kafka.topic`, `kafka.header.` prefix and `kafka.key`). Supported `inputFormat` types listed: csv, tvs (as spelled on the page), json, kafka, avro_stream, protobuf, thrift.

Tuning: `numPersistThreads` defaults to 1. A task keeps writing to one segment per segment-granularity interval until `maxRowsPerSegment`, `maxTotalRows` or `intermediateHandoffPeriod`, then hands off incrementally; small segments can result, which re-indexing can merge (the page cites an ideal ~500-700 MB per segment).

## Checked

Confirmed against the Druid docs page "Apache Kafka ingestion": Kafka version floor, extension setup on Overlord and Middle Manager, the example supervisor spec, the ioConfig table defaults, isolation level behaviour, input format defaults and the segment handoff notes. Added the ioConfig and tuning details above from that page.

Method: docs-only read of cited pages, 2026-11-08
