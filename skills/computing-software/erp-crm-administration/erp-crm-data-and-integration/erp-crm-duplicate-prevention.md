---
id: computing-software.erp-crm-administration.erp-crm-data-and-integration.erp-crm-duplicate-prevention
name: erp-crm-duplicate-prevention
category: computing-software
field: erp-crm-administration
product: erp-crm-data-and-integration
tags: [erp-crm-data-and-integration, erp-crm-duplicate-prevention]
level: practitioner
status: draft
description: "Stop duplicates at entry and clean existing ones."
sources: ['https://help.salesforce.com/', 'https://help.sap.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Prevent and merge duplicates
**Goal:** Stop duplicates at entry and clean existing ones.

- Use matching rules at entry (Salesforce duplicate rules, SAP BP duplicate checks) and scheduled duplicate jobs.
- Merge with survivorship rules and keep an audit trail of merges.
- Use external IDs from the system of record.

## Gotchas
- Merging child data across systems needs prior dependency review.

## Self-check
Duplicate rate drops after rules go live.
