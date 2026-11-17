---
id: computing-software.messaging-and-integration.apache-activemq-artemis.paging-overview-and-page-files
name: paging-overview-and-page-files
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,paging,page-mode,page-files,page-size-bytes,paging-directory,selectors,activemq-artemis]
level: practitioner
status: docs-checked
description: "Understand how the broker pages an address to disk per address, where page files live, and the restrictive-selector trap."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/paging.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Paging: modes and page files

**Goal:** hold queues of millions of messages with limited memory.

The broker starts paging an address to disk when the size of all its messages in memory exceeds the configured maximum. The default configuration uses paging. Only the address that exceeds its limit enters page mode; if `max-size-bytes` or `max-size-messages` is 0, the address always pages.

## Page files
Each address gets a folder of page files, each holding messages up to `page-size-bytes` (default 10MB). A page file is removed once all its messages are acknowledged. The location is set by `paging-directory` in `broker.xml` (default `data/paging`). Browsers read through the page-cursor system; consumers with selectors navigate page files and skip non-matching messages.

## Traps
- **Restrictive selectors:** if a selector matches a message sitting a million messages deep (for example `color='red'` when the first million are blue), you cannot read the red one until the earlier messages are consumed. Browsing differs: it scans the whole queue.
- **Per address, not total:** `max-size-bytes` limits each matching address separately. Use `global-max-size` or `global-max-messages` for a total.
- **Multicast queues:** an address with several multicast queues holds one copy of each message, freed only when all queues delivered it. One lazy subscription makes the whole address page, so the other queues read from the paging system too even if empty-looking. Ten queues with one stuck will still push the other nine through paged storage.
- **Many queues:** the system keeps at least one page file cached ahead and each active subscription may hold one, so with many queues reduce `page-size-bytes`.

## Checked
2026-11-03. Confirmed against the Artemis user manual page paging: page mode per address, page files, paging-directory default, the selector warning, multicast-queue caution and memory note. Removed: the Verify step.
Method: documentation only; no commands were run.
