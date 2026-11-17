---
id: computing-software.erp-crm-administration.salesforce-administration.sf-upsert-external-id
name: sf-upsert-external-id
category: computing-software
field: erp-crm-administration
product: salesforce-administration
tags: [salesforce-administration, sf-data-loader-bulk, sf-upsert-external-id]
level: practitioner
status: draft
description: "Load and re-load data idempotently."
sources: ['https://help.salesforce.com/', 'https://trailhead.salesforce.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Upsert with External IDs
**Goal:** Load and re-load data idempotently.

- Mark the field External ID and Unique; map in Data Loader for Upsert.
- Use relationship notation (`Account.ExternalId__c`) to link parents without IDs.
- Keep an ID map for rollbacks.

## Gotchas
- Case-insensitivity matters for unique external IDs.

## Self-check
Re-running a load updates rather than duplicates.
