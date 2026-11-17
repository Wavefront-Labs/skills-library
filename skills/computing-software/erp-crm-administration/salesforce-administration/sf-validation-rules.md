---
id: computing-software.erp-crm-administration.salesforce-administration.sf-validation-rules
name: sf-validation-rules
category: computing-software
field: erp-crm-administration
product: salesforce-administration
tags: [salesforce-administration, sf-validation-formula, sf-validation-rules]
level: practitioner
status: draft
description: "Block bad data with a formula that returns TRUE for an error."
sources: ['https://help.salesforce.com/', 'https://trailhead.salesforce.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Write validation rules
**Goal:** Block bad data with a formula that returns TRUE for an error.

- Object Manager > Validation Rules: the formula evaluates to TRUE when the data is invalid; set an error message and location (field or top of page).
- Guard against nulls with `ISBLANK()`, `ISNEW()`, `ISCHANGED()` and bypass flags using a custom permission.
- Test with API and data loads too: validation applies to them.

## Gotchas
- Validation rules run on integration and flow updates and can break them.

## Self-check
Saving an invalid record shows the message; a valid one saves.
