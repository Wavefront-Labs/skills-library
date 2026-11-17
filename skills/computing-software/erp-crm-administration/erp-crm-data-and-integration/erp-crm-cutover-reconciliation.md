---
id: computing-software.erp-crm-administration.erp-crm-data-and-integration.erp-crm-cutover-reconciliation
name: erp-crm-cutover-reconciliation
category: computing-software
field: erp-crm-administration
product: erp-crm-data-and-integration
tags: [erp-crm-data-and-integration, erp-crm-cutover-reconciliation]
level: advanced
status: draft
description: "Rehearse and prove the final load."
sources: ['https://help.salesforce.com/', 'https://help.sap.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Plan dry runs, cutover and reconciliation
**Goal:** Rehearse and prove the final load.

- Run at least two full dry runs timed end to end; define go/no-go criteria and rollback.
- Freeze source changes, load in dependency order, reconcile balances, counts and samples against the source.
- Keep the legacy system read-only for a period.

## Gotchas
- Skipping the rehearsal of load order causes cutover failures.

## Self-check
Reconciliation sign-off by business owners.
