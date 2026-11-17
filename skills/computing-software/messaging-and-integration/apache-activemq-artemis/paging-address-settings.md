---
id: computing-software.messaging-and-integration.apache-activemq-artemis.paging-address-settings
name: paging-address-settings
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,max-size-bytes,max-size-messages,max-read-page-messages,max-read-page-bytes,prefetch-page-messages,page-size-bytes,activemq-artemis]
level: advanced
status: docs-checked
description: "Configure paging thresholds and read-ahead limits per address: max-size-bytes, max-size-messages, page-size-bytes and the max-read-page and prefetch-page settings."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/paging.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Paging address-setting reference

**Goal:** set when an address pages and how much paged data is read back into memory.

```xml
<address-setting match="jms.someaddress">
   <max-size-bytes>104857600</max-size-bytes>
   <max-size-messages>1000</max-size-messages>
   <page-size-bytes>10485760</page-size-bytes>
   <address-full-policy>PAGE</address-full-policy>
</address-setting>
```
| setting | meaning | default |
|---|---|---|
| `max-size-bytes` | memory the address may use before page mode | -1 (disabled) |
| `max-size-messages` | message count before page mode | -1 (disabled) |
| `page-size-bytes` | size of each page file | 10MB |
| `address-full-policy` | must be `PAGE` for paging | `PAGE` |
| `max-read-page-messages` | paged messages readable into memory per queue | -1 |
| `max-read-page-bytes` | memory for paged messages read in per queue, counting delivering and ready messages | 2 * page-size-bytes (usually 20 MB) |
| `prefetch-page-messages` / `prefetch-page-bytes` | read-ahead per queue | from the max-read values |

If both byte and message limits are set the policy starts on whichever is reached first. The read limits are satisfied together; if all are -1 the broker keeps reading while consumers ask for more, leaving it unprotected from huge transactions or consumers without flow control. If consumers are slow to acknowledge, raise `max-read-page-bytes` so pending-ack messages do not starve the broker of messages.

With JDBC storage, effective `page-size-bytes` is capped by `jdbc-max-page-size-bytes`. Management-address settings cannot be overridden: management messages never page, block or fail.

## Checked
2026-11-03. Confirmed against the Artemis user manual pages paging and address-settings: the address-setting keys, defaults, JDBC page-size cap, management-address rule and the read-limit behaviour. Removed: the console Verify step, which no page describes.
Method: documentation only; no commands were run.
