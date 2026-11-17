---
id: computing-software.messaging-and-integration.rabbitmq.file-descriptor-limits
name: file-descriptor-limits
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, file-descriptor-limits]
level: practitioner
status: docs-checked
description: "Raise the file descriptor limit and size sockets for the connection count."
sources:
  - https://www.rabbitmq.com/docs/networking
  - https://www.rabbitmq.com/docs/production-checklist
  - https://www.rabbitmq.com/docs/configure
  - https://www.rabbitmq.com/docs/monitoring
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# File descriptor limits

**Goal:** Avoid 'out of file handles' under load.

## Steps
1. Allow at least 50K open file descriptors. Guideline from the checklist: 2 times the 95th percentile of concurrent connections plus the total number of queues.
2. On systemd, set `LimitNOFILE` in the unit override (the install guides show 64000).
3. When raising the limit, also override the `ERL_MAX_PORTS` environment variable accordingly. A very high limit can increase the runtime's upfront memory allocation.
4. Compare used and total descriptors (`fd_used`, `fd_total`) in `rabbitmq-diagnostics status` or monitoring.

## Failure modes
- At the limit the node cannot open files or accept new TCP connections.

## Verify
- Compare used and total file descriptors in `rabbitmq-diagnostics status`.

## Checked

Date: 2026-11-02. Confirmed on the Networking, Production Checklist and Configuration pages and the Monitoring guide. Removed: "value above 65536", "each connection uses one socket plus handles" as exact accounting.

Method: documentation only; no commands were run.
