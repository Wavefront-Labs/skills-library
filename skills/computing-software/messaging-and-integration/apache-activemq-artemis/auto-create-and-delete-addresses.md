---
id: computing-software.messaging-and-integration.apache-activemq-artemis.auto-create-and-delete-addresses
name: auto-create-and-delete-addresses
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,auto-create-addresses,auto-delete-addresses,auto-delete-addresses-delay,default-address-routing-type,default-queue-routing-type,activemq-artemis]
level: practitioner
status: docs-checked
description: "Control automatic address creation and deletion plus the default routing type used when the protocol does not say."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/address-settings.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Auto-created addresses

**Goal:** decide whether addresses are created on demand, when they are removed, and which routing type they get.

- `auto-create-addresses` (default `true`): create an address when a message is sent, or a consumer uses a queue mapped to an address, whose name fits the `match`. Not available to the Core client.
- `auto-delete-addresses` (default true): delete auto-created addresses once they have no queues.
- `auto-delete-addresses-delay` (ms, default `0`, immediate). The broker setting `address-queue-scan-period` (ms, default `30000`, `-1` to disable) controls how often addresses are scanned.
- `auto-delete-addresses-skip-usage-check` (default `false`): normally an address is deleted only if it was "used" (queues were created on it). If you enable the skip you must set `auto-delete-addresses-delay` above 0, otherwise addresses may be deleted almost immediately; deletion is then relative to creation time.
- `default-address-routing-type` and `default-queue-routing-type` (default `MULTICAST`): used only when the broker cannot determine the routing type from client or protocol semantics.

```xml
<address-setting match="jms.#">
   <auto-create-addresses>true</auto-create-addresses>
   <auto-delete-addresses>true</auto-delete-addresses>
   <auto-delete-addresses-delay>60000</auto-delete-addresses-delay>
</address-setting>
```

## Config reload
`config-delete-addresses`, `config-delete-queues` and `config-delete-diverts` (`OFF` or `FORCE`, default `OFF`) define what happens to items removed from `broker.xml` on a configuration reload.

## Verify
Send to a new address name, confirm it exists, remove its queues, and confirm it is deleted after the delay and scan period.

## Checked

Method: docs-checked 2026-11-09 against address-settings.adoc (raw, auto-create/delete address, routing-type and config-delete entries)
