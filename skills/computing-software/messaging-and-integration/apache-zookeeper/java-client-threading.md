---
id: computing-software.messaging-and-integration.apache-zookeeper.java-client-threading
name: java-client-threading
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, java-client, event-thread, io-thread, callbacks, client-properties]
level: advanced
status: docs-checked
description: "Java client binding behaviour: IO thread and event thread, callback ordering, blocking-callback hazard, handle invalidation and key client system properties."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Java binding threading

- Two threads: an IO thread (sessions, heartbeats, sync responses) and an event thread (async callbacks and watches).
- Callbacks run in order, one at a time; a blocking callback holds up all later callbacks and watch events but not the IO thread or synchronous calls.
- Hazard: a synchronous read inside a completion callback can return the new value before the queued watch event is processed.
- After close, SESSION_EXPIRED or AUTH_FAILED, the handle is invalid.
- Properties: `zookeeper.sasl.client` (false disables SASL), `zookeeper.disableAutoWatchReset`, `zookeeper.client.secure` (3.5.5+, needs the Netty client), `zookeeper.clientCnxnSocket` (NIO default, or Netty), `zookeeper.kerberos.shutdownTimeoutMs` (3.9.7+, default 5000).
- The client server list must match the ensemble (a subset is fine, outsiders are not).

Verify: callbacks stay short; no handler blocks on ZooKeeper calls from the event thread.

## Checked

Method: docs-checked 2026-11-09 against the ZooKeeper Programmer's Guide (Java Binding and Client Configuration Parameters sections); the SSL keystore/truststore property claim was dropped as unconfirmed.
