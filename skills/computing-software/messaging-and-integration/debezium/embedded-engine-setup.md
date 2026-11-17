---
id: computing-software.messaging-and-integration.debezium.embedded-engine-setup
name: embedded-engine-setup
category: computing-software
field: messaging-and-integration
product: debezium
tags: [embedded-engine, debezium-engine, java, offsets]
level: advanced
status: docs-checked
description: "Embed a Debezium connector in a Java application with DebeziumEngine, file offset storage and schema history."
sources:
  - https://debezium.io/documentation/reference/stable/development/engine.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Debezium Engine runs a connector inside your application, without Kafka or Kafka Connect, and hands each change event to a callback. Use it when you do not need Kafka's fault tolerance.

Dependencies: `io.debezium:debezium-api`, `io.debezium:debezium-embedded` and one connector module such as `debezium-connector-mysql`, all at the same version.

Packaging: Debezium loads implementations through the Java `ServiceLoader`, so merge `META-INF/services` files. With the Maven shade plug-in add `ServicesResourceTransformer`; with the assembly plug-in use the `metaInf-services` handlers.

Configuration example:

```java
props.setProperty("name", "engine");
props.setProperty("connector.class", "io.debezium.connector.mysql.MySqlConnector");
props.setProperty("offset.storage", "org.apache.kafka.connect.storage.FileOffsetBackingStore");
props.setProperty("offset.storage.file.filename", "/path/to/storage/offsets.dat");
props.setProperty("offset.flush.interval.ms", "60000");
props.setProperty("topic.prefix", "my-app-connector");
props.setProperty("schema.history.internal", "io.debezium.storage.file.history.FileSchemaHistory");
props.setProperty("schema.history.internal.file.filename", "/path/to/storage/schemahistory.dat");
try (DebeziumEngine<ChangeEvent<String, String>> engine = DebeziumEngine.create(Json.class)
   .using(props).notifying(record -> System.out.println(record)).build()) {
  Executors.newSingleThreadExecutor().execute(engine);
}
```

Engines: `AsyncEmbeddedEngine` is the default from 3.2.0.Alpha1; `EmbeddedEngine` is no longer available. The async engine can process records on multiple threads and run multiple tasks if the connector supports it (SQL Server and MongoDB).

Failures: after a crash you receive some events again, depending on `offset.flush.interval.ms` and batch size. Flushing happens only after each batch, so handlers must be idempotent. Connection retries use `errors.max.retries` (default `-1`, unlimited).

Gotcha: stop the engine with `close()` (the try block does this), not by shutting down the executor, which can leave duplicate records after restart.

## Checked

2026-11-08. Confirmed against the Debezium page development/engine, read in full: dependencies, ServiceLoader packaging, the configuration example, AsyncEmbeddedEngine default from 3.2.0.Alpha1, multi-task support, failure behaviour and errors.max.retries default of -1. Removed the claim that data directories must exist, which only the Debezium Server page makes, and replaced it with the page's guidance on stopping the engine.

Method: documentation only; no commands were run.
