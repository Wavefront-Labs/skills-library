---
id: computing-software.messaging-and-integration.apache-activemq-artemis.address-full-policy
name: address-full-policy
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,address-full-policy,max-size-bytes,max-size-bytes-reject-threshold,disk-full-policy,page,block,drop,fail,activemq-artemis]
level: advanced
status: docs-checked
description: "Choose PAGE, DROP, FAIL or BLOCK for a full address and BLOCK, DROP or FAIL for a full disk, with max-size-bytes and the AMQP reject threshold."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/address-settings.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Address full and disk full policies

**Goal:** define what the broker does when an address reaches its size limit or the disk fills.

## address-full-policy (applies where `max-size-bytes` is set)
- `PAGE` (default): further messages are paged to disk.
- `DROP`: further messages are silently dropped.
- `FAIL`: further messages are dropped and an exception is thrown on the client.
- `BLOCK`: producers block when they try to send more.

`max-size-bytes-reject-threshold` (default `-1`, no limit) is used with `BLOCK`: the size an address can reach before messages start being rejected. It works with `max-size-bytes` for AMQP clients only.

## disk-full-policy
Values `DROP`, `FAIL` or `BLOCK`, default `BLOCK`, with the same meanings applied when a disk becomes full. See `paging` for the disk monitoring settings.

```xml
<address-setting match="orders.#">
   <max-size-bytes>104857600</max-size-bytes>
   <address-full-policy>BLOCK</address-full-policy>
   <disk-full-policy>FAIL</disk-full-policy>
</address-setting>
```
## Related
`max-size-messages` offers a message-count limit, and `page-size-bytes`, `max-read-page-messages`, `max-read-page-bytes` tune paging (see the paging chapter). Ring queues should not be combined with `PAGE`.

## Checked
2026-11-03. Confirmed against the Artemis user manual pages address-settings (address-full-policy, disk-full-policy, max-size-bytes-reject-threshold, defaults) and ring-queues (avoid paging with ring queues). Removed: the Verify step and the unsupported 100MB value.
Method: documentation only; no commands were run.
