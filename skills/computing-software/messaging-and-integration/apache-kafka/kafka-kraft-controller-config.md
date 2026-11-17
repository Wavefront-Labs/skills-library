---
id: computing-software.messaging-and-integration.apache-kafka.kafka-kraft-controller-config
name: kafka-kraft-controller-config
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, kraft, controller-quorum-bootstrap-servers, controller-listener-names]
level: practitioner
status: docs-checked
description: "Write a dedicated KRaft controller server config using controller.quorum.bootstrap.servers and controller.listener.names."
sources:
  - https://kafka.apache.org/42/operations/kraft/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: configure a dedicated KRaft controller so every node can discover the active controller.

Every broker and every controller must set `controller.quorum.bootstrap.servers`. All servers use it to discover the active controller. Enumerate all controllers, each as host and port:

`controller.quorum.bootstrap.servers=host1:port1,host2:port2,host3:port3`

Example config for controller1 in a three-controller cluster:
```
process.roles=controller
node.id=1
listeners=CONTROLLER://controller1.example.com:9093
controller.quorum.bootstrap.servers=controller1.example.com:9093,controller2.example.com:9093,controller3.example.com:9093
controller.listener.names=CONTROLLER
```

With a dynamic quorum, `controller.quorum.voters` must not be set; `controller.quorum.bootstrap.servers` is set instead. It need not list every controller, but should list as many as possible, much like `bootstrap.servers` for clients. With a static quorum, each broker and controller must instead specify the IDs, hostnames and ports of all controllers in `controller.quorum.voters`.

`controller.quorum.voters` was deprecated by KRaft version 1.

Failure mode: if a controller or broker lacks `controller.quorum.bootstrap.servers`, it cannot locate the active controller.

The controllers selected through this property participate in the metadata quorum, and each is either the active controller or a hot standby.

## Checked

Method: docs-checked 2026-11-09 against the kafka.apache.org 4.2 KRaft operations page (Configuration, Upgrade and Controller membership changes sections). An unsupported closing sentence was removed.
