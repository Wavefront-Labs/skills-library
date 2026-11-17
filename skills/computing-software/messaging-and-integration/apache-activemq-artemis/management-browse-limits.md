---
id: computing-software.messaging-and-integration.apache-activemq-artemis.management-browse-limits
name: management-browse-limits
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,management-browse-page-size,management-message-attribute-size-limit,browse,queue-control,activemq-artemis]
level: practitioner
status: docs-checked
description: "Tune how many messages management browse/list return and how many bytes of each attribute are kept using two address-settings."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/address-settings.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Management browse limits

**Goal:** keep browsing a queue from the console or management API stable and informative.

Two address-settings affect the `browse`, `list` and `count-with-filter` management methods on the queue control:
- `management-browse-page-size` (default `200`): the number of messages a management resource can browse.
- `management-message-attribute-size-limit` (bytes, default `256`, `-1` switches the limit off): bytes collected from the message for `browse` and `list`. Longer attributes appear truncated.

Memory is allocated for all messages visible at a given moment, so setting the attribute limit too high, or turning it off for queues with large messages, may reduce browser stability.

```xml
<address-setting match="#">
   <management-browse-page-size>500</management-browse-page-size>
   <management-message-attribute-size-limit>1024</management-message-attribute-size-limit>
</address-setting>
```
(Values are illustrative.)

## Verify
Browse a queue holding more than the page size via the console and confirm the result is capped; inspect a large body and confirm it is truncated at the limit.

## Notes
Both settings are address-settings, so they can differ by address using wildcards, for example a larger limit for a small diagnostic queue and the default elsewhere.

## Checked

Method: docs-checked 2026-11-09 against address-settings.adoc (raw, management-browse-page-size and management-message-attribute-size-limit entries)
