---
id: computing-software.rpa-and-low-code.power-automate.pau-request-limits-licensing
name: pau-request-limits-licensing
category: computing-software
field: rpa-and-low-code
product: power-automate
tags: [power-automate, pau-limits-throttling, pau-request-limits-licensing]
level: advanced
status: draft
description: "Design flows within platform request limits."
sources: ['https://learn.microsoft.com/en-us/power-automate/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Understand request limits
**Goal:** Design flows within platform request limits.

- Power Platform requests are limited per user licence per 24 hours (confirm current figures for each licence in Microsoft documentation).
- Reduce actions, loops and polling frequency.
- Move heavy workloads to Azure services.

## Gotchas
- Throttled flows slow down or fail with 429 responses.

## Self-check
Daily action count is under the licence allowance.
