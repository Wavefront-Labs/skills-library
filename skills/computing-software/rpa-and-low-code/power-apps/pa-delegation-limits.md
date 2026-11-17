---
id: computing-software.rpa-and-low-code.power-apps.pa-delegation-limits
name: pa-delegation-limits
category: computing-software
field: rpa-and-low-code
product: power-apps
tags: [power-apps, pa-power-fx-data, pa-delegation-limits]
level: advanced
status: draft
description: "Make queries run at the source, not on the first rows."
sources: ['https://learn.microsoft.com/en-us/power-apps/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Design for delegation
**Goal:** Make queries run at the source, not on the first rows.

- Non-delegable queries only process the first 500 records by default, configurable up to 2,000 in settings.
- Use delegable functions and operators for the data source (Filter with supported predicates, SortByColumns); check blue-underline warnings.
- Pre-filter in the source with views or Dataverse columns.

## Gotchas
- Wrong results from non-delegation are silent at runtime.

## Self-check
Large tables return correct counts in testing with more than 2,000 rows.
