---
id: computing-software.messaging-and-integration.rabbitmq.memory-alarm
name: memory-alarm
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, memory-alarm, rmq-alarms]
level: advanced
status: docs-checked
description: "Understand vm_memory_high_watermark, publisher blocking and how to relieve the alarm."
sources:
  - https://www.rabbitmq.com/docs/memory
  - https://www.rabbitmq.com/docs/alarms
  - https://www.rabbitmq.com/docs/production-checklist
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Memory alarm

**Goal:** Prevent memory exhaustion.

## Steps
1. The default `vm_memory_high_watermark.relative` is 0.6 (60% of detected RAM). Set an absolute limit with `vm_memory_high_watermark.absolute` instead; the guide recommends absolute in containers.
2. When the limit is hit a memory alarm blocks all connections that are publishing; it clears when memory use falls, for example as consumers acknowledge deliveries.
3. Inspect usage with `rabbitmq-diagnostics memory_breakdown`.
4. The recommended relative range is 0.4 to 0.7. Leave at least 30% of memory to the OS and file system.

## Failure modes
- Values above 0.7 need solid memory monitoring: the guide says to use them with care.

## Verify
- `rabbitmq-diagnostics check_local_alarms`.

## Checked

Date: 2026-11-02. Confirmed on the Memory guide, Resource Alarms and Production Checklist: default 0.6, absolute setting, blocking publishers, `memory_breakdown`, 0.4 to 0.7 range, 30% headroom, `check_local_alarms`. Removed: the OOM-during-GC claim, "purging" as relief, the paging-threshold step.

Method: documentation only; no commands were run.
