---
id: computing-software.messaging-and-integration.apache-activemq-artemis.dead-letter-addresses
name: dead-letter-addresses
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,dead-letter-address,max-delivery-attempts,dlq,dead-letter,poison-message,activemq-artemis]
level: practitioner
status: docs-checked
description: "Move poison messages to a dead-letter address after max-delivery-attempts and know the default of 10 and how -1 allows infinite redelivery."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/undelivered-messages.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dead letter addresses

**Goal:** stop a message that keeps failing from being redelivered forever, and park it for inspection.

```xml
<address-setting match="exampleQueue">
   <dead-letter-address>deadLetterAddress</dead-letter-address>
   <max-delivery-attempts>3</max-delivery-attempts>
</address-setting>
```
After the given number of unsuccessful delivery attempts the message is removed from its queue and sent to the dead letter address, from which it can be consumed later. It is not delivered again from the original queue.

## Defaults and edge cases
- No `dead-letter-address`: the message is simply removed after `max-delivery-attempts` attempts.
- Default is 10 attempts at most.
- `max-delivery-attempts` of `-1` means infinite redelivery. You can set a dead-letter address globally (for example with the `#` wildcard) and override `-1` for one address so only it redelivers forever.
- Address wildcards work for dead-letter settings.
- Dead-letter messages carry the special copied-message properties.

Combine with delayed redelivery for back-off before dead-lettering (see `delayed-redelivery`), and use `send-to-dla-on-no-route` for unroutable messages.

## Checked
2026-11-03. Confirmed against the Artemis user manual page undelivered-messages, Dead Letter Addresses section: the address-setting, default of 10, -1 behaviour, wildcards and properties. Removed: the Verify step.
Method: documentation only; no commands were run.
