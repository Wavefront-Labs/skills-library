---
id: computing-software.messaging-and-integration.rabbitmq.ports-and-firewalls
name: ports-and-firewalls
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, ports-and-firewalls, rmq-networking]
level: practitioner
status: docs-checked
description: "Know and restrict the ports RabbitMQ uses: 5672, 5671, 15672, 15692, 25672 and 4369."
sources:
  - https://www.rabbitmq.com/docs/networking
  - https://www.rabbitmq.com/docs/clustering
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ports and firewalls

**Goal:** Open only what is needed.

## Steps
1. Client-facing: 5672/5671 AMQP (plain/TLS), 15672/15671 management HTTP/HTTPS, 15692 Prometheus, 1883/8883 MQTT (plain/TLS), 61613 STOMP, 5552/5551 streams (plain/TLS), each only when the corresponding plugin or protocol is enabled.
2. 4369 (epmd) and 25672 (Erlang distribution, inter-node and CLI tools) only between cluster nodes and hosts that run CLI tools.
3. Do not expose inter-node ports to clients or the public Internet.

## Failure modes
- Exposing epmd or the distribution port to untrusted networks is a serious risk.

## Verify
- `rabbitmq-diagnostics listeners` shows the interfaces and ports in use.

## Checked

2026-11-02. Confirmed in docs/networking and docs/clustering: 5672/5671, 15672/15671, 15692, 1883/8883, 61613, 5552/5551, 4369, 25672 and the advice to expose inter-node ports only to cluster peers and CLI hosts. Removed: the `ss -ltn` check (OS tool, not in docs).
Method: documentation only; no commands were run.
