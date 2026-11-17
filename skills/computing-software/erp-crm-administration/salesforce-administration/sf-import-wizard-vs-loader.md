---
id: computing-software.erp-crm-administration.salesforce-administration.sf-import-wizard-vs-loader
name: sf-import-wizard-vs-loader
category: computing-software
field: erp-crm-administration
product: salesforce-administration
tags: [salesforce-administration, sf-data-import, sf-import-wizard-vs-loader]
level: practitioner
status: draft
description: "Match the import tool to size and complexity."
sources: ['https://help.salesforce.com/', 'https://trailhead.salesforce.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choose Data Import Wizard or Data Loader
**Goal:** Match the import tool to size and complexity.

- Data Import Wizard: up to 50,000 records for common objects; Data Loader: insert, update, upsert, delete, hard delete and export, up to 5 million records.
- Use upsert with an External ID field to avoid duplicates.
- Disable or plan around flows and validation rules for loads.

## Gotchas
- Import wizard can match and prevent duplicates; Data Loader does not by default.

## Self-check
Success and error files reconcile with source counts.
