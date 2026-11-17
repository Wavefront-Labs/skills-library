---
id: computing-software.messaging-and-integration.rabbitmq.rabbitmq-diagnostics
name: rabbitmq-diagnostics
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, rabbitmq-diagnostics]
level: practitioner
status: docs-checked
description: "Use rabbitmq-diagnostics for read-only checks: ping, alarms, listeners, memory breakdown and health checks."
sources:
  - https://www.rabbitmq.com/docs/man/rabbitmq-diagnostics.8
  - https://www.rabbitmq.com/docs/monitoring
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rabbitmq-diagnostics

**Goal:** Diagnose without changing state.

## Steps
1. `rabbitmq-diagnostics check_running`, `check_local_alarms`, `check_port_connectivity`, `memory_breakdown`, `listeners`.
2. Health check commands can be used as readiness probes during deployment and upgrades.
3. `rabbitmq-diagnostics observer` for live runtime inspection.

## Failure modes
- The most basic check (`ping`) only shows the runtime is up and CLI authentication works; higher stages are more comprehensive but more prone to false positives.

## Verify
- Exit code 0 on each check.

## Checked

Date: 2026-11-02. Confirmed on the rabbitmq-diagnostics man page and Monitoring guide (health check stages, readiness probes). Removed: "ping success does not mean healthy; add alarm checks" in that wording.

Method: documentation only; no commands were run.
