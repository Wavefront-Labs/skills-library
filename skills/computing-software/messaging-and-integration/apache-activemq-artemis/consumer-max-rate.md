---
id: computing-software.messaging-and-integration.apache-activemq-artemis.consumer-max-rate
name: consumer-max-rate
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,consumermaxrate,rate-limiting,throttling,consumer-flow-control,activemq-artemis]
level: practitioner
status: docs-checked
description: "Throttle a consumer to a maximum messages-per-second with the consumerMaxRate URI parameter; combine with consumerWindowSize to avoid a filling buffer."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/flow-control.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Consumer rate limiting

**Goal:** make sure a consumer never consumes faster than a given rate.

Set `consumerMaxRate` on the connection URI to a positive integer: the maximum desired consumption rate in messages per second. `-1` (the default) disables rate-limited flow control.

```
tcp://localhost:61616?consumerMaxRate=10
```

## Interaction with the window
Rate-limited flow control can be combined with window-based flow control, but it limits only how many messages the client consumes per second, not how many are buffered. With a slow rate and a large `consumerWindowSize`, the client's internal buffer fills quickly with messages it cannot yet consume, hiding them from other consumers. Pair a low rate with a small window (see `consumer-window-size`).

## Checked
2026-11-03. Confirmed against the Artemis user manual page flow-control, section Rate limited flow control (consumer) and its note on combining with window-based flow control. Removed: the Verify step and a sizing section with claims the page does not make.
Method: documentation only; no commands were run.
