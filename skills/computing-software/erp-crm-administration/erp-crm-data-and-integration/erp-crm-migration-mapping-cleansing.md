---
id: computing-software.erp-crm-administration.erp-crm-data-and-integration.erp-crm-migration-mapping-cleansing
name: erp-crm-migration-mapping-cleansing
category: computing-software
field: erp-crm-administration
product: erp-crm-data-and-integration
tags: [erp-crm-data-and-integration, erp-crm-data-migration, erp-crm-migration-mapping-cleansing]
level: practitioner
status: draft
description: "Build a mapping and cleansing plan before loading."
sources: ['https://help.salesforce.com/', 'https://help.sap.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Map and cleanse source data
**Goal:** Build a mapping and cleansing plan before loading.

- Profile source data for duplicates, nulls, invalid codes and orphans; define field-level mapping and transformation rules.
- Agree owners for each decision; keep the mapping as a controlled document.
- Create load templates in the target platform (for example the S/4HANA migration cockpit or Salesforce external ID loads).

## Gotchas
- Cleansing in the source is cheaper than fixing in the target.

## Self-check
Row counts and key totals reconcile between source and staging.
