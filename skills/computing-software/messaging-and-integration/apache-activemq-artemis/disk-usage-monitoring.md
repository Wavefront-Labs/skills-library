---
id: computing-software.messaging-and-integration.apache-activemq-artemis.disk-usage-monitoring
name: disk-usage-monitoring
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,max-disk-usage,min-disk-free,disk-full-policy,disk-scan,disk-space,activemq-artemis]
level: practitioner
status: docs-checked
description: "Block, fail or drop producers before the disk fills using max-disk-usage, min-disk-free and disk-full-policy; the broker shuts down if disk runs out."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/paging.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Disk usage monitoring

**Goal:** stop producers before the data disk fills; the broker shuts itself down automatically if it runs out of disk space, because the disk is critical to data integrity.

The broker scans the disk and applies `disk-full-policy` when a limit is exceeded: `DROP`, `FAIL` or `BLOCK` (default `BLOCK`).

## Limits
- `max-disk-usage`: a percentage of disk used. With a 500GiB disk and value `50`, producers block once 250GiB is used.
- `min-disk-free`: a specific amount of free space, not a percentage. With 500GiB and `100GiB`, producers block once 400GiB is used.
- If both are configured, `min-disk-free` takes priority.

## Protocol caveat
If the sending protocol does not support flow control (for example STOMP), an exception is thrown and the client connection is dropped so it can no longer send messages and consume disk.

## Page sync
`page-sync-timeout` (nanoseconds) sets how often pages are synced. With the NIO journal it defaults to the same value as `journal-buffer-timeout`; with ASYNCIO the default is `3333333`.

## Checked
2026-11-03. Confirmed against the Artemis user manual page paging, sections Monitoring Disk, Max Disk Usage, Minimum Disk Free and Page Sync Timeout. Removed: the Verify step.
Method: documentation only; no commands were run.
