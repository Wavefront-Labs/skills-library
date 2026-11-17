---
id: computing-software.messaging-and-integration.apache-activemq-artemis.producer-max-rate
name: producer-max-rate
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,producermaxrate,rate-limiting,throttling,producer-flow-control,activemq-artemis]
level: practitioner
status: docs-checked
description: "Cap a producer's send rate with the producerMaxRate URL parameter in messages per second; -1 (default) disables the limit."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/flow-control.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Producer rate limiting

**Goal:** ensure a producer never sends faster than a set rate, regardless of the broker's address limits.

Set `producerMaxRate` on the URL to a positive integer, the maximum production rate in messages per second. `-1` (the default) disables it.

```
tcp://localhost:61616?producerMaxRate=100
```
It is separate from window-based credits (`producerWindowSize`, see `producer-window-size-and-blocking`) and address policies such as `BLOCK`.

## Checked
2026-11-03. Confirmed against the Artemis user manual page flow-control, section Rate limited flow control (producer): producerMaxRate, positive integer, messages per second, -1 default. Removed: the Verify step, the sizing advice and the claim about how a low rate presents, none of which the page states.
Method: documentation only; no commands were run.
