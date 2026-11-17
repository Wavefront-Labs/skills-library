---
id: computing-software.messaging-and-integration.apache-activemq-artemis.retroactive-addresses
name: retroactive-addresses
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,retroactive-message-count,retroactive-address,ring-queue,internal-naming-prefix,activemq-artemis]
level: advanced
status: docs-checked
description: "Keep the last N messages on an address for queues created later using retroactive-message-count, and understand the internal divert and ring queues it creates."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/retroactive-addresses.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Retroactive addresses

**Goal:** let a subscriber that connects late still receive the last N messages sent to an address before its queue existed (typical publish-subscribe use).

## Configure
Set `retroactive-message-count` in an address-setting:
```xml
<address-settings>
   <address-setting match="orders">
      <retroactive-message-count>100</retroactive-message-count>
   </address-setting>
</address-settings>
```
It works for both anycast and multicast queues, and can be changed at runtime through `broker.xml` or the management API.

## Internal resources
For each retroactive address the broker creates four internal resources: a non-exclusive divert, an address receiving from the divert, and two ring queues (anycast and multicast) on that address, each with `ring-size` equal to the count. Names follow `<internal-naming-prefix><delimiter><source-address><delimiter>(divert|address|queue<delimiter>(anycast|multicast))<delimiter>retro`. With the default prefix `$.artemis.internal.` and address `myAddress` the divert is `$.artemis.internal.myAddress.divert.retro`. They appear in the console and metrics. Custom address-settings for them can use the match `*.*.*.<source-address>.*.retro`.

## Gotchas
- Changing the broker's `internal-naming-prefix` after the resources exist breaks the feature.
- Lowering `retroactive-message-count` does not trim the ring queues (to avoid unintended message loss); an administrator must reduce the messages via the management API.
- Ring-queue caveats apply.

## Verify
Send messages, then create a new multicast queue on the address and check it receives up to N copies.

## Checked

Method: docs-checked 2026-11-09 against retroactive-addresses.adoc (read in full)
