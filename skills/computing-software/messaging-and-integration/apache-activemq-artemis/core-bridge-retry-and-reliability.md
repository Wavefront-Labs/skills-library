---
id: computing-software.messaging-and-integration.apache-activemq-artemis.core-bridge-retry-and-reliability
name: core-bridge-retry-and-reliability
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,bridge-retry-interval,retry-interval-multiplier,reconnect-attempts,confirmation-window-size,use-duplicate-detection,bridge-ha,activemq-artemis]
level: advanced
status: docs-checked
description: "Tune core bridge reconnection and delivery guarantees: retry-interval and multiplier, attempts, check-period, connection-ttl, duplicate detection and confirmation-window-size."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/core-bridges.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Core bridge retry and delivery guarantees

A bridge retries until the target is back, then resumes. These parameters control it (defaults in brackets):
- `retry-interval` (2000 ms) and `retry-interval-multiplier` (1.0): with 1000 and 2.0 the waits are 1000, 2000, 4000 ms. `max-retry-interval` (2000) caps growth.
- `initial-connect-attempts` and `reconnect-attempts` (both -1 = unlimited): number of tries before giving up and shutting down.
- `reconnect-attempts-same-node` (10): tries on the same topology node before reverting to the initial connector(s).
- `check-period` (30000 ms; -1 disables): how often to check for missing pings from the server. `connection-ttl` (60000 ms): how long the remote keeps the connection with no data; should exceed `check-period`.
- `use-duplicate-detection` (true): the bridge inserts a duplicate id into forwarded messages so the target can discard those the bridge resends after a failure, giving once-and-only-once without XA (see `duplicate-id-detection`).
- `producer-window-size` (1048576, -1 disables): flow control through the bridge. `min-large-message-size` (102400): above this, messages go in chunks.
- `confirmation-window-size`: warning from the manual: when forwarding to an address with `BLOCK` full policy from a queue with `max-size-bytes` set, keep `confirmation-window-size` less than or equal to `max-size-bytes`, or the message flow can cease.

## Checked

Method: docs-checked 2026-11-09 against core-bridges.adoc (read in full). Removed the Verify step.
