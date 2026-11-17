---
id: computing-software.messaging-and-integration.redpanda.thread-per-core-and-platform-optimizations
name: thread-per-core-and-platform-optimizations
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [seastar, thread-per-core, dma, xfs, irq, architecture]
level: advanced
status: docs-checked
description: "How the Redpanda Seastar thread-per-core model pins threads to cores and which kernel and hardware features it relies on."
sources:
  - https://docs.redpanda.com/streaming/current/get-started/architecture/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Redpanda uses a thread-per-core programming model through the Seastar library. Each application thread is pinned to a CPU core to avoid context switching and blocking, and the threads communicate by asynchronous message passing instead of locks. The docs conclude that Redpanda can scale up to use all available hardware before you need to scale out.

**Platform features it uses**
- Direct Memory Access (DMA) for disk I/O.
- Sparse file system support with XFS.
- Distribution of interrupt request (IRQ) processing between CPU cores.
- Isolated processes with control groups (cgroups).
- Disabled CPU power-saving modes.
- Upfront memory allocation, partitioned and pinned to CPU cores.

Redpanda has tuners that detect your hardware configuration to optimize itself automatically.

**Related points on the same page**
- The thread-per-core design means Redpanda can use all available hardware and scale up before you are forced to scale out.
- Tiered Storage: consumers of recent offsets read local storage while historical reads come from object storage with the same API; metadata for old segments is archived in object storage and cached on disk, loaded only when historical data is read.

## Checked

2026-11-08. Read the whole How Redpanda Works page. Confirmed: thread-per-core and Seastar, core pinning, message passing, the platform feature list, hardware-detecting tuners, scale-up sizing remark, Tiered Storage summary. Removed: the `rpk redpanda tune` command, the sizing-lever claims (NVMe, memory per core) and the power-saving inference, none of which the page states.
Method: documentation only; no commands were run.
