---
id: computing-software.erp-crm-administration.salesforce-administration.sf-field-types-formula-rollup
name: sf-field-types-formula-rollup
category: computing-software
field: erp-crm-administration
product: salesforce-administration
tags: [salesforce-administration, sf-custom-objects-fields, sf-field-types-formula-rollup]
level: practitioner
status: draft
description: "Select the right field type before creating it."
sources: ['https://help.salesforce.com/', 'https://trailhead.salesforce.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choose field types, formulas and roll-ups
**Goal:** Select the right field type before creating it.

- Types include text, picklist, number, currency, date, formula (read-only calculated), and roll-up summary (on the master of a master-detail relationship).
- Formula fields are recalculated on read and cannot be triggered by themselves; compile size limits apply.
- Changing the data type later is limited and can lose data.

## Gotchas
- Roll-up summaries exist only on master-detail masters (use a flow for lookups).

## Self-check
Formula field shows the right value on a test record.
