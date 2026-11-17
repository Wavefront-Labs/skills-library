---
id: computing-software.data-engineering.apache-pinot.apache-pinot-kafka-stream-ingestion-config
name: apache-pinot-kafka-stream-ingestion-config
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, kafka, stream-ingestion, streamconfigs, streamtype, stream-kafka-topic-name, stream-kafka-broker-list, stream-kafka-decoder-class-name, stream-kafka-consumer-factory-class-name, auto-offset-reset, jsonformat, addtable]
level: practitioner
status: docs-checked
description: "Pinot realtime streamConfigs for Kafka: topic, brokers, decoder and consumer factory, offset reset, JSON formats, partitions, AddTable."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/build-with-pinot/ingestion/stream-ingestion/import-from-apache-kafka.md", "https://github.com/pinot-contrib/pinot-docs/blob/latest/build-with-pinot/ingestion/stream-ingestion/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kafka stream ingestion config

Inside `tableIndexConfig.streamConfigs` (or an entry of `ingestionConfig.streamIngestionConfig.streamConfigMaps`) a Kafka realtime table needs:
```
"streamType": "kafka",
"stream.kafka.topic.name": "events",
"stream.kafka.broker.list": "kafka:9092",
"stream.kafka.decoder.class.name": "org.apache.pinot.plugin.inputformat.json.JSONMessageDecoder",
"stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory",
"stream.kafka.consumer.prop.auto.offset.reset": "smallest"
```

- Pinot ships one Kafka connector, `pinot-kafka-4.0` (consumer factory `org.apache.pinot.plugin.stream.kafka40.KafkaConsumerFactory`), the default when the factory is unset. It works with Kafka brokers 2.1 and newer, including KRaft. Existing `kafka20` and `kafka30` factory names resolve to Kafka 4 automatically, so older configs need no change. The kafka-0.9, 2.x and 3.x modules are removed.
- There is no high-level consumer; Pinot uses low-level partition consumers.
- `stream.kafka.consumer.prop.auto.offset.reset` accepts `smallest`, `largest`, time periods or timestamps and picks the start only for a partition with no stored Pinot offset. It is different from the raw Kafka property `auto.offset.reset` (`earliest`/`latest`), which governs recovery when a stored offset has expired in Kafka.
- `stream.kafka.decoder.prop.jsonFormat` (JSON decoder; default is UTF-8 text) takes `TEXT`, `POSTGRES_JSONB`, `SQLITE_JSONB`, `SMILE`, `CBOR` or `AUTO`. Use `AUTO` only for topics that legitimately mix encodings.
- Flush keys (`realtime.segment.flush.threshold.rows`, `.time`, `.segment.size`) live in the same map.
- Secrets can come from a Kafka ConfigProvider: list the alias in `config.providers` and reference it as `${file:/path:key}`. Use Kafka property names without the `stream.kafka.consumer.prop.` prefix.
- By default a table consumes all partitions of the topic; `stream.kafka.partition.ids` (for example `"0-3,6,8-9"`) restricts it to a subset.

Create the table:
```
bin/pinot-admin.sh AddTable -schemaFile events.schema -tableConfigFile events_realtime.json -exec
```

## Checked

2026-11-09. Read the Pinot docs page `import-from-apache-kafka.md` through the ConfigProvider section and the offset-reset, header and subset-partition sections by search; read the multi-stream sections of the stream-ingestion `README.md` by search only. Confirmed the properties, connector facts, jsonFormat values, offset-reset semantics, partition subset setting and AddTable usage. Corrected: the draft presented `kafka30` as the current connector; the docs now say a single Kafka 4 connector exists and the older factory names resolve to it. Removed: the unverified "one consuming segment per partition equals parallelism" line.
Method: documentation only; no commands were run.
