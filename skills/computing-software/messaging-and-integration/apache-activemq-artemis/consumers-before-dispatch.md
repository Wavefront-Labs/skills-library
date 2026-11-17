---
id: computing-software.messaging-and-integration.apache-activemq-artemis.consumers-before-dispatch
name: consumers-before-dispatch
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,consumers-before-dispatch,delay-before-dispatch,default-consumers-before-dispatch,activemq-artemis]
level: advanced
status: docs-checked
description: "Hold dispatch until a number of consumers have attached using consumers-before-dispatch and delay-before-dispatch (queue or address-setting)."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/address-settings.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Delaying dispatch until consumers attach

**Goal:** avoid the first consumer to connect taking all messages while others are still starting.

- `default-consumers-before-dispatch` (address-setting, default `0`): number of consumers needed on a queue bound to the matching address before messages are dispatched. Can be overridden per queue with `consumers-before-dispatch`.
- `default-delay-before-dispatch` (address-setting, ms, default `-1` = wait forever): how long the broker waits for that number of consumers to connect before it starts dispatching anyway. Tunable per queue with `delay-before-dispatch`.

```xml
<address-setting match="work.#">
   <default-consumers-before-dispatch>3</default-consumers-before-dispatch>
   <default-delay-before-dispatch>10000</default-delay-before-dispatch>
</address-setting>
```
With the default delay of `-1` and a consumer count that never arrives, messages are never dispatched, so set a delay when you cannot guarantee the consumer count.

## Per-queue override
Both settings exist at queue level as `consumers-before-dispatch` and `delay-before-dispatch`, and the address-setting names carry the `default-` prefix. The queue-level value overrides the address-setting default.

## Checked
2026-11-03. Confirmed against the Artemis user manual pages address-settings (default-consumers-before-dispatch, default-delay-before-dispatch, queue-level override) and configuration-index (queue attributes and defaults). Removed: the Verify step and the work-queue advice.
Method: documentation only; no commands were run.
