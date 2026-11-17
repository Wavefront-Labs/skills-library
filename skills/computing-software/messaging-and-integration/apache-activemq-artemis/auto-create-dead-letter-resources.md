---
id: computing-software.messaging-and-integration.apache-activemq-artemis.auto-create-dead-letter-resources
name: auto-create-dead-letter-resources
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,auto-create-dead-letter-resources,dead-letter-queue-prefix,dead-letter-queue-suffix,dlq,amq-orig-address,activemq-artemis]
level: advanced
status: docs-checked
description: "Auto-create a per-original-address DLQ filtered on _AMQ_ORIG_ADDRESS using auto-create-dead-letter-resources and the dead-letter-queue prefix and suffix."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/undelivered-messages.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Auto-created dead letter resources

**Goal:** segregate undelivered messages by original address (`DLQ.stocks`, `DLQ.orders`) in environments that rely on auto-created addresses and queues, without hand-writing an address-setting, address and queue per case.

Set `auto-create-dead-letter-resources` to `true` (default `false`). The broker creates the address named by `dead-letter-address` and a `MULTICAST` queue on it, named after the address the message was previously sent to, with a filter on the property `_AMQ_ORIG_ADDRESS` so it receives only messages from that address.

| address-setting | default |
|---|---|
| `dead-letter-queue-prefix` | `DLQ.` |
| `dead-letter-queue-suffix` | empty string |

```xml
<address-setting match="#">
   <dead-letter-address>DLA</dead-letter-address>
   <max-delivery-attempts>3</max-delivery-attempts>
   <auto-create-dead-letter-resources>true</auto-create-dead-letter-resources>
   <dead-letter-queue-prefix></dead-letter-queue-prefix>
   <dead-letter-queue-suffix>.DLQ</dead-letter-queue-suffix>
</address-setting>
```
The queue is read like any other, by its name (Core client) or fully qualified name (JMS). Since it is auto-created it is also auto-deleted according to the relevant address-settings.

## Checked
2026-11-03. Confirmed against the Artemis user manual page undelivered-messages, Automatically Creating Dead Letter Resources: setting, default, queue creation, filter, prefix and suffix defaults and the example. Removed: the Verify step.
Method: documentation only; no commands were run.
