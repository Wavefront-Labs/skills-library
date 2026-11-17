---
id: computing-software.erp-crm-administration.salesforce-administration.sf-legacy-automation-migration
name: sf-legacy-automation-migration
category: computing-software
field: erp-crm-administration
product: salesforce-administration
tags: [salesforce-administration, sf-legacy-automation-migration]
level: advanced
status: draft
description: "Replace retired automation with flows."
sources: ['https://help.salesforce.com/', 'https://trailhead.salesforce.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Migrate Workflow Rules and Process Builder to Flow
**Goal:** Replace retired automation with flows.

- Salesforce announced end of support for Workflow Rules and Process Builder (confirm current dates in Salesforce release notes); use the Migrate to Flow tool where supported.
- Inventory automations, rebuild as record-triggered flows, then deactivate originals.
- Test in sandbox with data loads.

## Gotchas
- Order of execution differs; re-test cross-object updates.

## Self-check
Same test data gives the same results as before migration.
