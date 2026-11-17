---
id: computing-software.messaging-and-integration.apache-kafka.kafka-quickstart-single-node
name: kafka-quickstart-single-node
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, quickstart, kafka-storage-sh, random-uuid]
level: intro
status: docs-checked
description: "Start a single-node Kafka 4.2 broker from the downloaded tarball, then create a topic, produce and consume events."
sources:
  - https://kafka.apache.org/42/getting-started/quickstart/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: get a local Kafka environment running and move events through it. Requires Java 17+.

1. Generate a cluster ID: `KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"`
2. Format the log directories: `bin/kafka-storage.sh format --standalone -t $KAFKA_CLUSTER_ID -c config/server.properties`
3. Start the server: `bin/kafka-server-start.sh config/server.properties`

Docker alternatives: `docker run -p 9092:9092 apache/kafka:4.2.2` (JVM image) or `apache/kafka-native:4.2.2` (GraalVM native image).

Create and inspect a topic:
```
bin/kafka-topics.sh --create --topic quickstart-events --bootstrap-server localhost:9092
bin/kafka-topics.sh --describe --topic quickstart-events --bootstrap-server localhost:9092
```

Write events (each line is one event; Ctrl-C to stop):
`bin/kafka-console-producer.sh --topic quickstart-events --bootstrap-server localhost:9092`

Read them back:
`bin/kafka-console-consumer.sh --topic quickstart-events --from-beginning --bootstrap-server localhost:9092`

Events are durably stored, so any number of consumers can re-read them. Running any CLI tool with no arguments prints its usage.

To delete all local data after the quickstart, remove /tmp/kafka-logs and /tmp/kraft-combined-logs.

Verify: the describe output shows PartitionCount and a Leader/Replicas/Isr line for each partition, and the console consumer prints the lines you produced.

## Checked

2026-11-04: claims, commands, flags and config names confirmed against the Kafka 4.2 Quickstart page. Removed: nothing.

Method: documentation only; no commands were run.
