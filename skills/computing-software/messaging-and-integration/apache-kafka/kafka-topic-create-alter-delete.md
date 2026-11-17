---
id: computing-software.messaging-and-integration.apache-kafka.kafka-topic-create-alter-delete
name: kafka-topic-create-alter-delete
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, kafka-topics-sh, partitions, replication-factor]
level: intro
status: docs-checked
description: "Create, grow, reconfigure and delete topics with kafka-topics.sh and kafka-configs.sh, including the partition and name limits."
sources:
  - https://kafka.apache.org/42/operations/basic-kafka-operations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: manage topics from the command line.

Create:
`bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic my_topic_name --partitions 20 --replication-factor 3 --config x=y`

Replication factor is how many servers replicate each message; the docs recommend 2 or 3 so machines can be bounced without interrupting consumption. Partition count is the number of logs the topic is sharded into; each partition must fit on a single server, and it caps maximum consumer parallelism. Command-line configs override server defaults such as retention.

Add partitions: `--alter --topic my_topic_name --partitions 40`. Adding partitions does not redistribute existing data, so if data is partitioned by hash(key) % number_of_partitions the mapping can shuffle for consumers that rely on it. Kafka does not support reducing the partition count.

Per-topic configs:
```
bin/kafka-configs.sh --bootstrap-server localhost:9092 --entity-type topics --entity-name my_topic_name --alter --add-config x=y
bin/kafka-configs.sh --bootstrap-server localhost:9092 --entity-type topics --entity-name my_topic_name --alter --delete-config x
```

Delete: `bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic my_topic_name`

Name limit: each partition lives in a folder named topic-name, a dash and the partition id, and folder names cannot exceed 255 characters. Assuming at most 100,000 partitions, topic names cannot be longer than 249 characters.

## Checked

2026-11-04: claims, commands, flags and config names confirmed against the Kafka 4.2 Basic Kafka operations page. Removed: nothing.

Method: documentation only; no commands were run.
