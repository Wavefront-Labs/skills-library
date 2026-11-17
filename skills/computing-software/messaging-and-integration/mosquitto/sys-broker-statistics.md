---
id: computing-software.messaging-and-integration.mosquitto.sys-broker-statistics
name: sys-broker-statistics
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [sys-broker, clients-connected, load-averages, heap]
level: practitioner
status: docs-checked
description: "Read Mosquitto broker health from $SYS/broker topics: clients, bytes, messages, dropped publishes, load averages and heap."
sources:
  - https://mosquitto.org/man/mosquitto-8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: know which $SYS topics report what.

Examples documented in mosquitto(8):
- `$SYS/broker/version` (static) and `$SYS/broker/clients/total`: total connected plus disconnected sessions registered.
- `$SYS/broker/clients/connected` (alias `active`, deprecated) counts connected clients; `clients/disconnected` (alias `inactive`, deprecated) counts persistent clients registered but disconnected; `clients/maximum` is the peak concurrent clients; `clients/expired` counts sessions removed by `persistent_client_expiration`.
- `$SYS/broker/bytes/received` and `bytes/sent`: totals since start.
- `$SYS/broker/messages/received` and `sent`: all message types since start.
- `$SYS/broker/connections/socket/count`: sockets made, whether or not MQTT connect succeeded.
- `$SYS/broker/mqtt/publish/dropped` (also `publish/messages/dropped`): PUBLISH messages dropped for inflight or queuing limits.
- `$SYS/broker/subscriptions/count`: active subscriptions.
- `$SYS/broker/heap/current` and `heap/maximum`: memory in use; may be unavailable depending on compile-time options.
- `$SYS/broker/load/<metric>/+` where the final level is `1min`, `5min` or `15min`: moving averages per minute, over connections, bytes received and sent, messages received and sent, publish dropped, received and sent, and sockets.
- `$SYS/broker/connection/#`: bridge state, 1 active or 0 not.

Updates are every `sys_interval` seconds.

## Checked

2026-11-08. Confirmed against the mosquitto(8) Broker Status section: client counters and deprecated aliases, bytes and message totals, socket count, dropped publish topics, subscriptions, heap availability note, load averages, bridge state and sys_interval updates. Claims unchanged.

Method: documentation only; no commands were run.
