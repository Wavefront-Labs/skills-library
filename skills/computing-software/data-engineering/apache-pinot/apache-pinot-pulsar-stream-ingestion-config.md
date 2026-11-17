---
id: computing-software.data-engineering.apache-pinot.apache-pinot-pulsar-stream-ingestion-config
name: apache-pinot-pulsar-stream-ingestion-config
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, pulsar, stream-ingestion, plugins-include, stream-pulsar-topic-name, stream-pulsar-bootstrap-servers, stream-pulsar-authenticationtoken, oauth, stream-pulsar-metadata-populate]
level: practitioner
status: docs-checked
description: "Pulsar realtime ingestion: the pinot-pulsar plugin, topic and bootstrap keys, token, OAuth2 and TLS settings, metadata columns."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/build-with-pinot/ingestion/stream-ingestion/apache-pulsar.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pulsar stream ingestion config

Pinot consumes Pulsar through the `pinot-pulsar` plugin. Enable it at Pinot setup with `-Dplugins.include=pinot-pulsar`. The plugin ships in the official binary distribution since Pinot 0.11.0; older versions need it downloaded into the `plugins` directory. The page says Pinot relies on Pulsar client version 5.0.0, so make sure the Pulsar broker is compatible.

Sample `streamConfigs` (sits inside `tableIndexConfig` in the page's REALTIME table sample):
```
"streamType": "pulsar",
"stream.pulsar.topic.name": "<your pulsar topic name>",
"stream.pulsar.bootstrap.servers": "pulsar://<host1>:6650,pulsar://<host2>:6651",
"stream.pulsar.consumer.prop.auto.offset.reset": "smallest",
"stream.pulsar.fetch.timeout.millis": "30000",
"stream.pulsar.decoder.class.name": "org.apache.pinot.plugin.inputformat.json.JSONMessageDecoder",
"stream.pulsar.consumer.factory.class.name": "org.apache.pinot.plugin.stream.pulsar.PulsarConsumerFactory",
"realtime.segment.flush.threshold.rows": "1000000",
"realtime.segment.flush.threshold.time": "6h"
```
(the values for fetch timeout, offset reset and flush thresholds are the page's sample, not defaults.)

Authentication, all inside `streamConfigs`:
- Token: `"stream.pulsar.authenticationToken": "<token>"` (token generated per the Pulsar JWT docs).
- OAuth2 (for example a StreamNative cluster): `stream.pulsar.issuerUrl`, `stream.pulsar.credsFilePath` (a file URL) and `stream.pulsar.audience`.
- TLS: `stream.pulsar.tlsTrustCertsFilePath` with the trust certificate file location, and change the broker URL scheme from `pulsar://` to `pulsar+ssl://`.

Metadata and headers as columns: set `stream.pulsar.metadata.populate` to `true`. `__key`, `__header$<HeaderKeyName>` (one column per property), `__metadata$publishTime`, `__metadata$brokerPublishTime` and `__metadata$eventTime` are populated by default. List more in `stream.pulsar.metadata.fields` (comma separated, by Pulsar field name), which makes columns such as `__metadata$messageId`, `__metadata$messageBytes`, `__metadata$producerName`, `__metadata$sequenceId`, `__metadata$topicName` available. To use any of these columns you must list them explicitly in the table schema (dimension fields of type `STRING`); then they behave like any other column for transforms and indexes. Follow the schema evolution guidelines when updating an existing table's schema.

## Checked

2026-11-08. Read the whole pinot-docs Apache Pulsar page. Confirmed the plugin flag and version note, the table and OAuth/TLS/token keys, the metadata mapping and defaults, and the schema requirement. Replaced the example topic, broker and path values with placeholders, added the missing keys from the sample, and flagged sample values as non-defaults. The OAuth key names are prefixed `stream.pulsar.`, which the earlier version omitted.

Method: documentation only; no commands were run.
