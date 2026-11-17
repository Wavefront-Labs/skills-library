---
id: computing-software.rpa-and-low-code.power-automate.pau-scope-run-after
name: pau-scope-run-after
category: computing-software
field: rpa-and-low-code
product: power-automate
tags: [power-automate, pau-control-error-handling, pau-scope-run-after]
level: advanced
status: draft
description: "Handle failures in flows."
sources: ['https://learn.microsoft.com/en-us/power-automate/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Implement try/catch with Scope and run after
**Goal:** Handle failures in flows.

- Wrap actions in a Scope; add a catch scope with Configure run after set to has failed/timed out and a finally scope for cleanup.
- Use `result('Scope')` to read errors.
- Terminate with failed status when needed.

## Gotchas
- Without run-after, a failure stops silently with a failed run.

## Self-check
Forced error reaches the catch scope.
