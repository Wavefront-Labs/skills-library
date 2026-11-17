---
id: computing-software.messaging-and-integration.debezium.debezium-server-configuration
name: debezium-server-configuration
category: computing-software
field: messaging-and-integration
product: debezium
tags: [debezium-server, application-properties, sink, microprofile]
level: practitioner
status: docs-checked
description: "Configure Debezium Server with application.properties: one source connector, a sink, formats, transforms and predicates."
sources:
  - https://debezium.io/documentation/reference/stable/operations/debezium-server.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Debezium Server streams changes to a non-Kafka sink without Kafka Connect. Download and unpack the distribution; the `debezium-server` directory holds `config`, `connectors`, `lib`, `run.sh` and `run.bat`. Start with `./run.sh` (Linux) or `run.bat` (Windows). For Oracle copy the JDBC driver into `lib`, plus the XStream API files for XStream.

Configuration uses MicroProfile Config (files, environment variables, system properties). The main file is `config/application.properties`, with sections:

- `debezium.source`: exactly one connector per server instance.
- `debezium.sink`: the destination.
- `debezium.format`: serialisation.
- `debezium.transforms` and `debezium.predicates`: SMTs and conditions.

```
debezium.sink.type=kinesis
debezium.sink.kinesis.region=eu-central-1
debezium.source.connector.class=io.debezium.connector.postgresql.PostgresConnector
debezium.source.offset.storage.file.filename=data/offsets.dat
debezium.source.offset.flush.interval.ms=0
debezium.source.database.hostname=localhost
debezium.source.database.port=5432
debezium.source.topic.prefix=tutorial
debezium.source.schema.include.list=inventory
```

For the built-in PostgreSQL plug-in set `debezium.source.plugin.name=pgoutput`.

Transforms: `debezium.transforms=<names>`, then `debezium.transforms.<name>.type`, `.predicate` and `.negate` (default `false`).

Gotchas:

- The offsets directory (here `data`) must exist before startup.
- A value containing `${...}` is expanded by Quarkus; escape with a second dollar, `$${my.property}`.
- Scripting (the filter SMT) is off until you set `ENABLE_DEBEZIUM_SCRIPTING=true`.

## Checked

2026-11-08. Confirmed against the Debezium page operations/debezium-server, read in part (installation and start, configuration sections, example properties, the dollar-escape note, the transforms and predicates tables and the message filtering section). Nothing removed.

Method: documentation only; no commands were run.
