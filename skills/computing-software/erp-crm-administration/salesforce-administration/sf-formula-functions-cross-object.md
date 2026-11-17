---
id: computing-software.erp-crm-administration.salesforce-administration.sf-formula-functions-cross-object
name: sf-formula-functions-cross-object
category: computing-software
field: erp-crm-administration
product: salesforce-administration
tags: [salesforce-administration, sf-formula-functions-cross-object]
level: practitioner
status: draft
description: "Reference parent fields and build text, date and logical formulas."
sources: ['https://help.salesforce.com/', 'https://trailhead.salesforce.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Use cross-object formulas and functions
**Goal:** Reference parent fields and build text, date and logical formulas.

- Cross-object formulas traverse relationships such as `Account.Industry`; use `CASE`, `IF`, `BLANKVALUE`, `TEXT`, `TODAY()`.
- Mind the compile size limit and the number of cross-object spans.
- Use `HYPERLINK` for dynamic links.

## Gotchas
- `TEXT()` is required to compare picklists in formulas.

## Self-check
Preview a test record to check outputs.
