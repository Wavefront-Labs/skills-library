---
id: computing-software.messaging-and-integration.apache-kafka.kafka-replace-kraft-controller-disk
name: kafka-replace-kraft-controller-disk
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, kraft, ignore-formatted, describe-replication, metadata-log-dir]
level: advanced
status: docs-checked
description: "Replace a lost KRaft controller metadata disk safely: wait for majority catch-up, then format and restart."
sources:
  - https://kafka.apache.org/42/operations/hardware-and-os/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: re-provision a controller whose metadata directory (metadata.log.dir, or the first log directory if unset) was lost.

Do not format and start the new controller until a majority of controllers already hold all committed data.

1. Check replication with `kafka-metadata-quorum.sh --bootstrap-server localhost:9092 describe --replication`.
2. Wait until Lag is small on a majority of controllers. If the leader's end offset is not increasing, wait for lag 0 on a majority. LastFetchTimestamp and LastCaughtUpTimestamp should be close together on most controllers.
3. Format: `bin/kafka-storage.sh format --cluster-id uuid --config config/server.properties`
4. Start: `bin/kafka-server-start.sh config/server.properties`

Failure mode: format can report the directory is already formatted. This can happen in combined mode when only the metadata log directory was lost. Only in that case, rerun format with `--ignore-formatted`.

## Checked

Method: 2026-11-08 docs-only read of the cited Kafka 4.2 hardware-and-os page. Removed the listed column names and the pick-latest-end-offset wording as unconfirmed; steps otherwise match the page. No hands-on run.
