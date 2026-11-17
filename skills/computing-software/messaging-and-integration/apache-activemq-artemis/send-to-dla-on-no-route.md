---
id: computing-software.messaging-and-integration.apache-activemq-artemis.send-to-dla-on-no-route
name: send-to-dla-on-no-route
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,send-to-dla-on-no-route,unroutable-messages,dead-letter-address,activemq-artemis]
level: practitioner
status: docs-checked
description: "Send messages that match no queue to the dead-letter address instead of discarding them with send-to-dla-on-no-route."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/address-settings.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sending unroutable messages to the DLA

**Goal:** stop silently discarding messages that the broker cannot route to any queue.

A message sent to an address may route nowhere, for example because no queue is bound to the address or no bound queue has a filter that matches. Normally it is discarded. If `send-to-dla-on-no-route` is `true` (default `false`) in the address-setting, the message is instead sent to the `dead-letter-address` for that address, if one exists.

```xml
<address-setting match="orders">
   <dead-letter-address>DLA</dead-letter-address>
   <send-to-dla-on-no-route>true</send-to-dla-on-no-route>
</address-setting>
```
If no `dead-letter-address` is defined for the address, the message cannot go anywhere and is still discarded. See `dead-letter-addresses` for how undeliverable messages are handled and `message-expiry-addresses` for the expiry equivalent.

## Verify
Send to an address with no matching queue and confirm the message arrives on the DLA queue rather than disappearing.

## Notes
The setting is per address through the address-setting match, so it can be turned on for important business addresses and left off for chatty ones. `auto-create-dead-letter-resources` makes the broker create the defined `dead-letter-address` and a corresponding dead-letter queue automatically, and `dead-letter-queue-prefix` and `dead-letter-queue-suffix` (both empty by default) shape the names of the automatically created dead-letter queues.

## Checked

Method: docs-checked 2026-11-09 against address-settings.adoc (raw, send-to-dla-on-no-route, auto-create-dead-letter-resources, dead-letter-queue-prefix/suffix entries)
