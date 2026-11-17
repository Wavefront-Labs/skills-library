---
id: computing-software.messaging-and-integration.apache-activemq-artemis.graceful-shutdown
name: graceful-shutdown
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,graceful-shutdown,graceful-shutdown-enabled,graceful-shutdown-timeout,broker-stop,activemq-artemis]
level: practitioner
status: docs-checked
description: "Stop the broker without cutting clients off by enabling graceful-shutdown-enabled and bounding the wait with graceful-shutdown-timeout."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/graceful-shutdown.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Graceful server shutdown

**Goal:** stop the broker while letting existing clients finish and disconnect, instead of dropping them immediately.

## Settings (broker configuration)
- `graceful-shutdown-enabled` (boolean, default `false`): when `true`, on shutdown the broker first refuses new client connections, then waits for existing connections to be closed by the clients before completing shutdown.
- `graceful-shutdown-timeout` (milliseconds, default `-1`): how long to wait for all clients to disconnect before the broker forcibly disconnects them and proceeds. `-1` means wait indefinitely.

## Failure mode
A client holding its connection open forever prevents a graceful shutdown when the timeout is `-1`. Set a finite `graceful-shutdown-timeout` when the broker is stopped by automation, such as a service manager or container orchestrator, so a stuck client cannot block the stop indefinitely.

## Example
```xml
<graceful-shutdown-enabled>true</graceful-shutdown-enabled>
<graceful-shutdown-timeout>30000</graceful-shutdown-timeout>
```
(The values are illustrative; the page documents the parameter names and defaults only.)

## Checked

Method: docs-checked 2026-11-09 against graceful-shutdown.adoc (read in full). Removed the Verify step and an unsupported config location.
