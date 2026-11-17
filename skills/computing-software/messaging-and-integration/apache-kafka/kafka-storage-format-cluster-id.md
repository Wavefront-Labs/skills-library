---
id: computing-software.messaging-and-integration.apache-kafka.kafka-storage-format-cluster-id
name: kafka-storage-format-cluster-id
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, kafka-storage-sh, standalone, initial-controllers]
level: practitioner
status: docs-checked
description: "Generate a cluster ID and format KRaft nodes with kafka-storage.sh using --standalone, --initial-controllers or --no-initial-controllers."
sources:
  - https://kafka.apache.org/42/operations/kraft/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: provision storage for new KRaft nodes correctly.

`bin/kafka-storage.sh random-uuid` generates a cluster ID, and that same ID must be used when formatting every server in the cluster with `kafka-storage.sh format`. Kafka no longer auto-formats blank storage directories or invents a cluster ID, because auto-formatting can hide an error: if a majority of controllers could start with an empty log directory, a leader might be elected with missing committed data.

Bootstrap a standalone first controller (recommended; add the rest dynamically):
`bin/kafka-storage.sh format --cluster-id <CLUSTER_ID> --standalone --config config/controller.properties`
This creates `meta.properties` in `metadata.log.dir` with a random `directory.id`, and a snapshot `00000000000000000000-0000000000.checkpoint` that makes this node the only voter.

Bootstrap with several controllers:
```
bin/kafka-storage.sh format --cluster-id ${CLUSTER_ID} \
  --initial-controllers "0@controller-0:1234:${CONTROLLER_0_UUID},1@controller-1:1234:${CONTROLLER_1_UUID},2@controller-2:1234:${CONTROLLER_2_UUID}" \
  --config config/controller.properties
```
Each entry is `replica-id@host:port:directory-id`. The value must be identical on every controller with the same cluster ID.

New brokers and controllers joining an existing cluster:
`bin/kafka-storage.sh format --cluster-id <CLUSTER_ID> --config config/server.properties --no-initial-controllers`

## Checked

2026-11-04: claims, commands, flags and config names confirmed against the Kafka 4.2 KRaft operations page (Provisioning Nodes). Removed: nothing.

Method: documentation only; no commands were run.
