---
id: computing-software.erp-crm-administration.salesforce-administration.sf-record-triggered-before-after
name: sf-record-triggered-before-after
category: computing-software
field: erp-crm-administration
product: salesforce-administration
tags: [salesforce-administration, sf-flow-record-triggered, sf-record-triggered-before-after]
level: advanced
status: draft
description: "Use before-save for fast field updates and after-save for related records and actions."
sources: ['https://help.salesforce.com/', 'https://trailhead.salesforce.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choose before-save versus after-save flows
**Goal:** Use before-save for fast field updates and after-save for related records and actions.

- Setup > Flows > New > Record-Triggered Flow: trigger on create, update or both; set entry conditions and run asynchronously options.
- Before-save flows can update the triggering record without DML and are faster; after-save flows can create other records and call actions.
- Avoid multiple flows on the same object and event where order matters; use Flow Trigger Explorer to see order.

## Gotchas
- Do not update the same record in an after-save flow without entry conditions, to avoid recursion.

## Self-check
Debug run on a record shows the expected path and element order.
