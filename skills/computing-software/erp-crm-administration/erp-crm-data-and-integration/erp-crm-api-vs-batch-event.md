---
id: computing-software.erp-crm-administration.erp-crm-data-and-integration.erp-crm-api-vs-batch-event
name: erp-crm-api-vs-batch-event
category: computing-software
field: erp-crm-administration
product: erp-crm-data-and-integration
tags: [erp-crm-data-and-integration, erp-crm-integration-patterns, erp-crm-api-vs-batch-event]
level: advanced
status: draft
description: "Choose the pattern from timing and volume needs."
sources: ['https://help.salesforce.com/', 'https://help.sap.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pick request/reply, batch or event integration
**Goal:** Choose the pattern from timing and volume needs.

- Request/reply APIs for real-time lookups; batch/ETL for bulk sync; events (platform events, change data capture, OData eventing) for loose coupling.
- Plan limits: API call quotas and throttling on both sides.
- Define the system of record per entity.

## Gotchas
- Two-way sync without a conflict rule creates loops.

## Self-check
Integration run with failure injection recovers cleanly.
