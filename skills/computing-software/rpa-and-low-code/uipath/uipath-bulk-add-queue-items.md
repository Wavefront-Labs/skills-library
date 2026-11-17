---
id: computing-software.rpa-and-low-code.uipath.uipath-bulk-add-queue-items
name: uipath-bulk-add-queue-items
category: computing-software
field: rpa-and-low-code
product: uipath
tags: [uipath, uipath-bulk-add-queue-items]
level: advanced
status: draft
description: "Load many items efficiently."
sources: ['https://docs.uipath.com/', 'https://academy.uipath.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Add queue items in bulk
**Goal:** Load many items efficiently.

- Bulk Add Queue Items from a DataTable; specific data columns go into SpecificContent.
- Use Add Queue Item for single items with a reference.
- Respect throughput limits.

## Gotchas
- A failed bulk add can load part of the data; check the result and the failed rows.

## Self-check
Count in Orchestrator equals source rows.
