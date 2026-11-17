---
id: computing-software.messaging-and-integration.apache-activemq-artemis.message-expiry-delay-settings
name: message-expiry-delay-settings
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,expiry-delay,min-expiry-delay,max-expiry-delay,no-expiry,address-settings,activemq-artemis]
level: advanced
status: docs-checked
description: "Override message expiration broker-side with no-expiry, expiry-delay, min-expiry-delay and max-expiry-delay, applied in that order of precedence."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/message-expiry.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Expiry delay settings

**Goal:** enforce or default message expiration on the broker regardless of what producers set.

Four address-settings apply exclusively in this order of precedence: `no-expiry`, then `expiry-delay`, then `max-expiry-delay` and `min-expiry-delay`. If `no-expiry` and `expiry-delay` are both set, `expiry-delay` is ignored completely.

## no-expiry
`<no-expiry>true</no-expiry>` forces messages never to expire: an arriving message with expiration `10` is changed to `0`. Default `false`.

## expiry-delay
Applies only to messages using the default expiration `0`. With `<expiry-delay>10</expiry-delay>`, a message with expiration `0` becomes `10`; one with `20` stays `20`. Milliseconds; default `-1` (disabled).

## Range
```xml
<address-setting match="exampleQueue">
   <min-expiry-delay>10</min-expiry-delay>
   <max-expiry-delay>100</max-expiry-delay>
</address-setting>
```
- A message without expiration gets `max-expiry-delay`; if that is undefined, `min-expiry-delay`; if neither, unchanged.
- Above max becomes max; below min becomes min; inside the range is unchanged.
Both default to `-1` (disabled), in milliseconds.

## Warnings
- `max-expiry-delay` of `0` makes messages expire immediately.
- If you apply any of these settings to the address used as `expiry-address`, expired messages receive new expiry delays and may themselves expire and vanish from the broker.

## Checked
2026-11-03. Confirmed against the Artemis user manual page message-expiry, Configuring Expiry Delay sections: precedence, no-expiry, expiry-delay, range semantics, defaults, units and both warnings. Removed: the Verify step.
Method: documentation only; no commands were run.
