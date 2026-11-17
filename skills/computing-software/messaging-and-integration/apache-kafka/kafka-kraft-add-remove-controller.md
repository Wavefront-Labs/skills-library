---
id: computing-software.messaging-and-integration.apache-kafka.kafka-kraft-add-remove-controller
name: kafka-kraft-add-remove-controller
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, kraft, kafka-metadata-quorum-sh, add-controller, remove-controller]
level: advanced
status: docs-checked
description: "Grow or shrink a dynamic KRaft controller quorum with kafka-metadata-quorum.sh add-controller and remove-controller."
sources:
  - https://kafka.apache.org/42/operations/kraft/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: change KRaft controller membership in a cluster running a dynamic quorum (KIP-853).

Add a controller:
1. Provision the new controller with `kafka-storage.sh format ... --no-initial-controllers` and start it.
2. Watch replication catch up: `bin/kafka-metadata-quorum.sh describe --replication`
3. Once it has caught up with the active controller, add it:

`bin/kafka-metadata-quorum.sh --command-config config/controller.properties --bootstrap-server localhost:9092 add-controller`

Use `--bootstrap-controller localhost:9093` instead of `--bootstrap-server` when talking to controller endpoints. Any Admin Client configs, such as authentication settings, must also be placed in the file passed as `--command-config` (controller.properties in the example).

Remove a controller: run remove-controller before shutting the controller down, so it leaves the quorum first.
`bin/kafka-metadata-quorum.sh --bootstrap-server localhost:9092 remove-controller --controller-id <id> --controller-directory-id <directory-id>`

Static versus dynamic: the quorum type is fixed at format time. It is dynamic if `controller.quorum.voters` is absent and one of `--standalone`, `--initial-controllers` or `--no-initial-controllers` was used. Check with `bin/kafka-features.sh --bootstrap-controller localhost:9093 describe`: `kraft.version` at level 0 or absent means static; 1 or above means dynamic.

## Checked

2026-11-04: claims, commands, flags and config names confirmed against the Kafka 4.2 KRaft operations page (Controller membership changes). Removed: nothing.

Method: documentation only; no commands were run.
