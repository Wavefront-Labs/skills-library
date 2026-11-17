---
id: computing-software.data-engineering.trino.trino-kafka-event-listener
name: trino-kafka-event-listener
category: computing-software
field: data-engineering
product: trino
tags: [event-listener, kafka-event-listener, query-history, anonymization, sasl]
level: practitioner
status: docs-checked
description: "Publish Trino query created and completed events to Kafka topics, including SASL client properties, anonymization and size limits."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/admin/event-listeners-kafka.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino kafka event listener

The Kafka event listener streams query events to a Kafka-compatible system, giving you cluster query history that can be read in Kafka, through a Trino Kafka-connector catalog, or by downstream systems. Events include CPU and memory metrics, which columns were accessed, and processing metadata.

Minimal `etc/kafka-event-listener.properties`:

```properties
event-listener.name=kafka
kafka-event-listener.broker-endpoints=kafka.example.com:9093
kafka-event-listener.created-event.topic=query_create
kafka-event-listener.completed-event.topic=query_complete
kafka-event-listener.client-id=trino-example
```

Add the file to `event-listener.config-files` in `config.properties`.

For specialised authentication, point `kafka-event-listener.config.resources` at a Kafka client properties file, for example with `sasl.mechanism=SCRAM-SHA-512`, `security.protocol=SASL_SSL` and a `sasl.jaas.config` line. Values set explicitly in the listener file override the resource file.

Other properties and defaults:
- `anonymization.enabled` (`false`): anonymise event data before sending.
- `client-id`: identifies the cluster when several Trino clusters share Kafka.
- `max-request-size` (`5MB`): larger messages fail.
- `batch-size` (`16kB`).
- `publish-created-event` and `publish-completed-event` (both `true`).
- `excluded-fields`: comma-separated names replaced with null, such as `payload,user`.
- `request-timeout` (`10s`, minimum 1ms), `terminate-on-initialization-failure` (`true`), `env-var-prefix` (adds metadata from matching environment variables).

## Checked

2026-11-04. Read against the Trino docs page `admin/event-listeners-kafka.md` (GitHub source of the public docs): property names, defaults, allowed values, error messages, examples and behaviour described above match it. Removed nothing except an unspecific pointer to the page's property table (replaced by the listed properties).
Method: documentation only; no commands were run.
