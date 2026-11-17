---
id: computing-software.erp-crm-administration.salesforce-administration.sf-record-types-picklists
name: sf-record-types-picklists
category: computing-software
field: erp-crm-administration
product: salesforce-administration
tags: [salesforce-administration, sf-record-types-layouts, sf-record-types-picklists]
level: practitioner
status: draft
description: "Offer different picklist values and layouts by business process."
sources: ['https://help.salesforce.com/', 'https://trailhead.salesforce.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Use record types to segment processes
**Goal:** Offer different picklist values and layouts by business process.

- Create the record type, select available picklist values, and assign it via profiles or permission sets with a default.
- Sales processes and support processes (for opportunities and cases) tie stage sets to record types.
- Plan integrations: set RecordTypeId on loads.

## Gotchas
- Deleting a record type requires a replacement for existing records.

## Self-check
Users of different record types see different picklist values.
