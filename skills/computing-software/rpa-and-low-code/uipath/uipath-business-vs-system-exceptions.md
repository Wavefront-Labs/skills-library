---
id: computing-software.rpa-and-low-code.uipath.uipath-business-vs-system-exceptions
name: uipath-business-vs-system-exceptions
category: computing-software
field: rpa-and-low-code
product: uipath
tags: [uipath, uipath-business-vs-system-exceptions]
level: practitioner
status: draft
description: "Distinguish data problems from technical failures."
sources: ['https://docs.uipath.com/', 'https://academy.uipath.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Separate business and system exceptions
**Goal:** Distinguish data problems from technical failures.

- BusinessRuleException marks a transaction as business failure (no retry); system exceptions trigger retry and may restart apps.
- Record reasons on the queue item.
- Alert on system exception counts.

## Gotchas
- Retrying business exceptions wastes time and duplicates side effects.

## Self-check
Queue items show Failed with the correct reason type.
