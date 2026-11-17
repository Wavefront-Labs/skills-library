---
id: computing-software.rpa-and-low-code.power-automate.pau-pagination-large-data
name: pau-pagination-large-data
category: computing-software
field: rpa-and-low-code
product: power-automate
tags: [power-automate, pau-pagination-large-data]
level: advanced
status: draft
description: "Retrieve more than the default page."
sources: ['https://learn.microsoft.com/en-us/power-automate/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Handle pagination and large data
**Goal:** Retrieve more than the default page.

- Turn on Pagination in action settings with a threshold; use Filter Query and Top Count.
- Use Select to reduce payload size.
- Avoid loading entire tables.

## Gotchas
- Without pagination, results stop at the default page size.

## Self-check
Item count equals the source count.
