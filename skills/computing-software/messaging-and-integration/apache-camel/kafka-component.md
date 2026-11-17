---
id: computing-software.messaging-and-integration.apache-camel.kafka-component
name: kafka-component
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, component, kafka, consumer, producer, offsets]
level: practitioner
status: docs-checked
description: "Camel kafka component: URI form, groupId, autoOffsetReset, manual commit, breakOnFirstError, producer key and partition, CamelKafka headers and KafkaIdempotentRepository."
sources:
  - https://camel.apache.org/components/next/kafka-component.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kafka:

`kafka:topic[?options]` (artifact `camel-kafka`). Consumers may list several topics comma-separated; producers send to one. `brokers` has no default.

Consumer (defaults): `groupId` required; `autoOffsetReset` `latest` (also `earliest`, `none`, `by_duration:`); `autoCommitEnable` true; `allowManualCommit` false (puts `KafkaManualCommit` in header `CamelKafkaManualCommit`); `breakOnFirstError` false (true breaks out on a failure so the failed message is retried: the default NoopCommitManager leaves the offset uncommitted, while the Sync and Async commit managers seek back to it; pair with an error handler to avoid endless poison-message loops); `consumersCount` 1; `maxPollRecords` 500; `batching` false; `pollTimeoutMs` 5000; `pollOnError` `ERROR_HANDLER` (or `DISCARD`, `RECONNECT`, `RETRY`, `STOP`); `topicIsPattern` false; `seekTo` `BEGINNING` or `END`; `sessionTimeoutMs` 45000; `heartbeatIntervalMs` 3000.

Producer: `key` beats header `CamelKafkaKey`; `partitionKey` beats `CamelKafkaPartitionKey`; `requestRequiredAcks` `all`; `enableIdempotence` true; `deliveryTimeoutMs` 120000; `lingerMs` 5; `maxBlockMs` 60000; `transacted` false; `useIterator` true (one record per element); `recordMetadata` false.

Headers: `CamelKafkaKey`, `CamelKafkaPartition`, `CamelKafkaTopic`, `CamelKafkaOffset`, `CamelKafkaTimestamp`, `CamelKafkaOverrideTopic` (one-time dynamic topic).

Bodies: String by default; a Map or POJO is sent as `toString()`, so marshal first.

`KafkaIdempotentRepository` needs `topic` and `bootstrapServers`; `maxCacheSize` 1000, `pollDurationMs` 100; startup replays the topic, up to 30 seconds.

Verify: a consumer with `groupId` and `autoOffsetReset=earliest` reads existing records after start.

## Checked

Method: docs-checked 2026-11-09 against the camel.apache.org kafka-component page (option tables, message headers, body section, breakOnFirstError and the KafkaIdempotentRepository section; manual commit examples only skimmed). The breakOnFirstError wording was corrected to match the page.
