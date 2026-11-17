---
id: computing-software.messaging-and-integration.apache-activemq-artemis.message-expiry-addresses
name: message-expiry-addresses
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,message-expiry,expiry-address,time-to-live,amq-actual-expiry,dropping-expired,activemq-artemis]
level: practitioner
status: docs-checked
description: "Route expired messages to an expiry-address in an address-setting, or drop them by unsetting it, and set TTL on Core and JMS messages."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/message-expiry.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Message expiry and expiry addresses

**Goal:** control what happens to messages whose time-to-live passes.

The broker never delivers an expired message to a consumer, and may discard it if undelivered at expiry. With an expiry address, expired messages are moved there for inspection; many queues can be bound to it.

## Setting a TTL
- Core: `message.setExpiration(System.currentTimeMillis() + 5000);`
- JMS: `producer.setTimeToLive(5000);`

## Expiry address
```xml
<address-setting match="exampleQueue">
   <expiry-address>expiryQueue</expiry-address>
</address-setting>
```
Expired messages get the copied-message properties plus `_AMQ_ACTUAL_EXPIRY`, a `Long` holding the actual expiry time.

## Dropping
With no expiry address, or one explicitly unset using `<expiry-address/>`, expired messages are removed and dropped. To unset for one address under a wildcard rule, add a more specific setting:
```xml
<address-setting match="#"><expiry-address>expiryQueue</expiry-address></address-setting>
<address-setting match="exampleQueue"><expiry-address/></address-setting>
```

## Expiring the expired
```xml
<address-setting match="expiryQueue">
   <expiry-address/>
   <expiry-delay>600000</expiry-delay>
</address-setting>
```
Messages sitting in a queue bound to `expiryQueue` then expire after 5 minutes and are dropped.

## Reaper
`message-expiry-scan-period` (broker.xml, ms, default 30000, `-1` disables) controls how often queues are scanned for expired messages.

## Checked
2026-11-03. Confirmed against the Artemis user manual page message-expiry: Core and JMS TTL calls, expiry address, _AMQ_ACTUAL_EXPIRY, dropping, expiring expired messages and message-expiry-scan-period. Removed: the Verify step.
Method: documentation only; no commands were run.
