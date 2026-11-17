---
id: computing-software.messaging-and-integration.apache-activemq-artemis.address-setting-matching
name: address-setting-matching
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,address-settings,address-setting,match,wildcards,specificity,hierarchical,activemq-artemis]
level: practitioner
status: docs-checked
description: "Apply per-address policy with address-setting match in broker.xml and predict which setting wins when several wildcard matches overlap."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/address-settings.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Address-setting matching and layering

**Goal:** attach a block of policy (dead-letter, expiry, paging, auto-create and so on) to the addresses whose names fit a `match`.

```xml
<address-settings>
   <address-setting match="order.foo">
      <dead-letter-address>DLA</dead-letter-address>
      <max-delivery-attempts>3</max-delivery-attempts>
   </address-setting>
</address-settings>
```
`match` can be an exact address or use wildcards: `queue.#` applies to every address starting with `queue.`. The any-words delimiter defaults to `#` and the single-word delimiter to `*`.

## Resolution rules
Settings are hierarchical. When more than one `address-setting` matches, the more specific match wins, and settings can be layered so details need not be repeated:
- a match containing the any-words delimiter (`#`) is less specific than one without;
- a match with the single-word delimiter (`*`) is less specific than an exact name.
Matches can also be made literal so wildcard characters are matched literally: define two characters in `literal-match-markers` in the core section of `broker.xml` (no value by default, so literal matches are off), then wrap the match in them, for example `match="(orders.#)"`.

## Practical use
Put broad defaults on `#`, then override only the keys that differ on narrower matches.

## Verify
After editing, send a test message to a matching address and observe the policy (for example dead-lettering after max-delivery-attempts).

## Checked

Method: docs-checked 2026-11-09 against address-settings.adoc (raw, intro on hierarchy and the Literal Matches section)
