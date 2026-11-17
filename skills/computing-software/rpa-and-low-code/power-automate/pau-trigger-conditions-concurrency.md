---
id: computing-software.rpa-and-low-code.power-automate.pau-trigger-conditions-concurrency
name: pau-trigger-conditions-concurrency
category: computing-software
field: rpa-and-low-code
product: power-automate
tags: [power-automate, pau-cloud-flow-triggers, pau-trigger-conditions-concurrency]
level: advanced
status: draft
description: "Limit unwanted runs and control parallelism."
sources: ['https://learn.microsoft.com/en-us/power-automate/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tune trigger conditions and concurrency
**Goal:** Limit unwanted runs and control parallelism.

- Trigger conditions (expressions in settings) filter events before the flow runs; concurrency control limits parallel runs (1 to 50).
- Use split on to process array items individually.
- Combine with retry policy.

## Gotchas
- Concurrency on after-the-fact cannot be turned off once enabled on some triggers (confirm in docs).

## Self-check
Runs drop for non-matching events.
