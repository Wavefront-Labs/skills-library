---
id: computing-software.erp-crm-administration.salesforce-administration.sf-mass-delete-hard-delete
name: sf-mass-delete-hard-delete
category: computing-software
field: erp-crm-administration
product: salesforce-administration
tags: [salesforce-administration, sf-mass-delete-hard-delete]
level: practitioner
status: draft
description: "Remove data in bulk safely."
sources: ['https://help.salesforce.com/', 'https://trailhead.salesforce.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mass delete and recycle bin
**Goal:** Remove data in bulk safely.

- Mass Delete Records tool for common objects; Data Loader Delete and Hard Delete (requires the Bulk API Hard Delete permission).
- Recycle Bin retains deleted records for a limited period.
- Take an export backup first.

## Gotchas
- Hard delete bypasses the Recycle Bin and is irreversible.

## Self-check
Counts after delete match the intended scope.
