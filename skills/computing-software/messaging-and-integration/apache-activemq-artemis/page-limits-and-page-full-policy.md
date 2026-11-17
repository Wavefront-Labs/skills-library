---
id: computing-software.messaging-and-integration.apache-activemq-artemis.page-limits-and-page-full-policy
name: page-limits-and-page-full-policy
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,page-limit-bytes,page-limit-messages,page-full-policy,paging-limits,activemq-artemis]
level: advanced
status: docs-checked
description: "Limit how much an address can page with page-limit-bytes or page-limit-messages and choose DROP or FAIL with page-full-policy (since 2.28.0)."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/paging.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Page limits and page full policy

**Goal:** stop one destination whose consumers vanished from consuming the whole disk. Available since version 2.28.0.

Set either `page-limit-bytes` or `page-limit-messages`, together with `page-full-policy`, in the address-setting:
```xml
<address-setting match="jms.someaddress">
   <page-limit-bytes>10G</page-limit-bytes>
   <page-limit-messages>1000000</page-limit-messages>
   <page-full-policy>FAIL</page-full-policy>
</address-setting>
```
`page-full-policy` takes `DROP` (messages silently dropped, clients get no exception) or `FAIL` (producers get a JMS exception).

## How the byte limit works
`page-limit-bytes` is converted to a number of page files (`page-limit-bytes` / `page-size-bytes`) and compared with the current page file count. It must be greater than or equal to `page-size-bytes`, or paging blocks immediately. If the current number of page files exceeds the limit, paging is blocked per `page-full-policy` until the count drops to or below it, and blocks again when exceeded.

## Checked
2026-11-03. Confirmed against the Artemis user manual page paging, section Page Limits and Page Full Policy: version 2.28.0, the three settings, DROP and FAIL behaviour and the page-file conversion rule. Removed: the Verify step and a derived sizing example not stated on the page.
Method: documentation only; no commands were run.
