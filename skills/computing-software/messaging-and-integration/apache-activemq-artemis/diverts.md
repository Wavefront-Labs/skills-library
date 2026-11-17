---
id: computing-software.messaging-and-integration.apache-activemq-artemis.diverts
name: diverts
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,divert,exclusive-divert,non-exclusive-divert,composite-divert,forwarding-address,routing-type,activemq-artemis]
level: practitioner
status: docs-checked
description: "Redirect or copy messages from one address to others with exclusive, non-exclusive and composite diverts, optional filter, transformer and routing-type."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/diverts.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diverts

**Goal:** transparently route messages sent to one address to other addresses on the same broker, with no client change.

A divert is defined in `broker.xml` at the `core` level (zero or more). Key elements: `address`, `forwarding-address`, `exclusive`, optional `filter`, optional `transformer-class-name`, and `routing-type`.

## Exclusive vs non-exclusive
- Exclusive: matching messages go only to the new address, not the old.
```xml
<divert name="prices-divert">
   <address>priceUpdates</address>
   <forwarding-address>priceForwarding</forwarding-address>
   <filter string="office='New York'"/>
   <exclusive>true</exclusive>
</divert>
```
Non-matching messages continue to the original address. With no filter, all messages match.
- Non-exclusive: a copy goes to the new address and the original continues (splitting the flow).
```xml
<divert name="order-divert">
   <address>orders</address>
   <forwarding-address>spyTopic</forwarding-address>
   <exclusive>false</exclusive>
</divert>
```
- Composite (fan-out): a comma-separated `forwarding-address`, for example `dallas, chicago, denver`.

When an address has both kinds, exclusive diverts run first, and if one diverted the message the non-exclusive ones are skipped.

## Routing type
`routing-type` is `ANYCAST`, `MULTICAST`, `PASS` or `STRIP` (default `STRIP`). An anycast message is not routed to multicast queues and vice versa, so set it when the target uses a different type.

## Limits
- All diverts on an address receive the same original message, so one divert's transformer result is not visible to another's filter.
- A divert targets only an address on the same server; for another broker divert to a local store-and-forward queue and consume it with a core bridge.
- Diverted messages carry the special copied-message properties.

## Checked

Method: docs-checked 2026-11-09 against diverts.adoc (read in full). Removed the Verify step.
