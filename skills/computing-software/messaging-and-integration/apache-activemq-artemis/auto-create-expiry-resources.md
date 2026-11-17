---
id: computing-software.messaging-and-integration.apache-activemq-artemis.auto-create-expiry-resources
name: auto-create-expiry-resources
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,auto-create-expiry-resources,expiry-queue-prefix,expiry-queue-suffix,amq-orig-address,expiry-address,activemq-artemis]
level: advanced
status: docs-checked
description: "Auto-create per-address expiry queues filtered on _AMQ_ORIG_ADDRESS with auto-create-expiry-resources and the expiry-queue-prefix and suffix."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/message-expiry.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Auto-created expiry resources

**Goal:** segregate expired messages by original address (for example `EXP.stocks`, `EXP.orders`) without hand-defining an address-setting, address and queue for each, which is awkward when addresses are auto-created.

Set `auto-create-expiry-resources` to `true` (default `false`) in the address-setting. The broker then creates the address named by `expiry-address`, and a `MULTICAST` queue on it named after the address the message was originally sent to. That queue has a filter on the property `_AMQ_ORIG_ADDRESS` so it only receives messages from that address. The name can be decorated with:

| address-setting | default |
|---|---|
| `expiry-queue-prefix` | `EXP.` |
| `expiry-queue-suffix` | empty string |

## Example
```xml
<address-setting match="#">
   <expiry-address>expiryAddress</expiry-address>
   <auto-create-expiry-resources>true</auto-create-expiry-resources>
   <expiry-queue-prefix></expiry-queue-prefix>
   <expiry-queue-suffix>.EXP</expiry-queue-suffix>
</address-setting>
```
The queue can be consumed by its name alone (Core client) or its fully qualified queue name (JMS), like any queue. Because it is auto-created it is also auto-deleted according to the relevant address-settings.

## Checked
2026-11-03. Confirmed against the Artemis user manual page message-expiry, Configuring Automatic Creation of Expiry Resources: setting, default, queue creation, filter, prefix and suffix defaults and the example. Removed: the Verify step.
Method: documentation only; no commands were run.
