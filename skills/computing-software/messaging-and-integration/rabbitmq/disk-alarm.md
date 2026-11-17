---
id: computing-software.messaging-and-integration.rabbitmq.disk-alarm
name: disk-alarm
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, disk-alarm]
level: advanced
status: docs-checked
description: "Set disk_free_limit so the broker blocks publishers before the disk fills."
sources:
  - https://www.rabbitmq.com/docs/disk-alarms
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Disk alarm

**Goal:** Keep free space for persistence and recovery.

## Steps
1. Set a limit such as `disk_free_limit.absolute = 1GB` (default 50 MB). `disk_free_limit.relative` is the alternative; if both are set the absolute value wins, and absolute is the recommended form.
2. When free space drops below the limit, an alarm triggers and all producers are blocked.
3. Alert before the limit and expand storage.

## Failure modes
- A limit set too low can let paged-out messages fill the disk and crash RabbitMQ between disk checks (at least 10 seconds apart); a more conservative limit equals the installed memory.

## Verify
- `rabbitmq-diagnostics check_local_alarms` reports disk alarm status.

## Checked

Date: 2026-11-02. Confirmed in the Disk Alarms page (docs/disk-alarms) and the rabbitmq-diagnostics man page (`check_local_alarms`): default, absolute and relative settings, blocking, check interval. Removed: the 5GB figure and the corruption wording.

Method: documentation only; no commands were run.
