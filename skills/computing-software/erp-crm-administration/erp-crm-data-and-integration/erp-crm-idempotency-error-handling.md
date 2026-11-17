---
id: computing-software.erp-crm-administration.erp-crm-data-and-integration.erp-crm-idempotency-error-handling
name: erp-crm-idempotency-error-handling
category: computing-software
field: erp-crm-administration
product: erp-crm-data-and-integration
tags: [erp-crm-data-and-integration, erp-crm-idempotency-error-handling]
level: advanced
status: draft
description: "Survive retries and failures."
sources: ['https://help.salesforce.com/', 'https://help.sap.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Make integrations idempotent and observable
**Goal:** Survive retries and failures.

- Use external IDs/upserts and message keys so a retry does not duplicate; add dead-letter handling and alerting.
- Log correlation IDs across systems.
- Store credentials in a secret store, not in config.

## Gotchas
- Retrying non-idempotent calls creates duplicates.

## Self-check
Replaying the same message twice yields one record.
