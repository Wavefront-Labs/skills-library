---
id: computing-software.messaging-and-integration.apache-kafka.kafka-kraft-process-roles
name: kafka-kraft-process-roles
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, kraft, process-roles, combined-mode]
level: intro
status: docs-checked
description: "Choose process.roles for each KRaft node: broker, controller or combined, and know why combined mode is for development only."
sources:
  - https://kafka.apache.org/42/operations/kraft/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: decide what role each Kafka server plays in KRaft mode.

The `process.roles` property takes:
- `broker` - the server acts as a broker.
- `controller` - the server acts as a controller.
- `broker,controller` - a "combined" server doing both.

Combined servers are simpler to operate for small use cases such as a development environment. The key disadvantage is that the controller is less isolated from the rest of the system; for example, you cannot roll or scale the controllers separately from the brokers. Combined mode is not recommended in critical deployment environments, so use separate `broker` and `controller` nodes there.

Controller count: select 3 or 5 servers, depending on cost and how many concurrent failures you need to survive. A majority of controllers must be alive to maintain availability. With 3 controllers the cluster tolerates 1 failure; with 5 it tolerates 2. In general, to withstand N concurrent failures you need 2N + 1 controllers.

Sizing: controllers keep all cluster metadata in memory and on disk. The docs state that for a typical cluster, 5GB of main memory and 5GB of disk space on the metadata log directory is sufficient.

Each controller is either the active controller or a hot standby for it.

## Checked

Method: docs-checked 2026-11-09 against the kafka.apache.org 4.2 KRaft operations page (Process Roles, Controllers and the controller sizing paragraph).
