---
id: computing-software.erp-crm-administration.erp-crm-data-and-integration.erp-crm-sod-matrix
name: erp-crm-sod-matrix
category: computing-software
field: erp-crm-administration
product: erp-crm-data-and-integration
tags: [erp-crm-data-and-integration, erp-crm-access-sod, erp-crm-sod-matrix]
level: advanced
status: draft
description: "Identify conflicting duties."
sources: ['https://help.salesforce.com/', 'https://help.sap.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Build a segregation of duties matrix
**Goal:** Identify conflicting duties.

- List critical business functions (create vendor, approve payment, post journal) and mark pairs that one person must not hold.
- Map roles to functions and report conflicts; define mitigating controls where unavoidable.
- Review at joiner, mover and leaver events.

## Gotchas
- Role names hide conflicts; map at permission level.

## Self-check
Conflict report reviewed with business owners.
