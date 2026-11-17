---
id: computing-software.rpa-and-low-code.automation-governance.rpa-exception-monitoring
name: rpa-exception-monitoring
category: computing-software
field: rpa-and-low-code
product: automation-governance
tags: [automation-governance, rpa-resilience-roi, rpa-exception-monitoring]
level: advanced
status: draft
description: "Detect failures and recover quickly."
sources: ['https://learn.microsoft.com/en-us/power-platform/guidance/coe/starter-kit', 'https://docs.uipath.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Monitor and recover automations
**Goal:** Detect failures and recover quickly.

- Track success rate, queue age, mean time to recover; alert on failure and stalled queues.
- Plan for application UI changes with regression tests.
- Keep a runbook with restart steps.

## Gotchas
- Silent failures lose data; always alert.

## Self-check
Mean time to detect and recover are tracked.
