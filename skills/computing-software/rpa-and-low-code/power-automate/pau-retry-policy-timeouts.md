---
id: computing-software.rpa-and-low-code.power-automate.pau-retry-policy-timeouts
name: pau-retry-policy-timeouts
category: computing-software
field: rpa-and-low-code
product: power-automate
tags: [power-automate, pau-retry-policy-timeouts]
level: advanced
status: draft
description: "Control retries and timeouts on actions."
sources: ['https://learn.microsoft.com/en-us/power-automate/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Configure retry policies
**Goal:** Control retries and timeouts on actions.

- Action settings retry policy: default, none, fixed or exponential interval; retry on 408, 429 and 5xx.
- Set timeouts for long-running calls.
- Avoid retrying non-idempotent actions.

## Gotchas
- Retry on create actions can duplicate records.

## Self-check
Observed retries appear in run history.
