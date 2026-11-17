---
id: computing-software.erp-crm-administration.salesforce-administration.sf-duplicate-matching-rules
name: sf-duplicate-matching-rules
category: computing-software
field: erp-crm-administration
product: salesforce-administration
tags: [salesforce-administration, sf-duplicate-matching-rules]
level: practitioner
status: draft
description: "Prevent and report duplicates."
sources: ['https://help.salesforce.com/', 'https://trailhead.salesforce.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Use matching and duplicate rules
**Goal:** Prevent and report duplicates.

- Setup > Duplicate Management: create Matching Rules (fuzzy or exact) and Duplicate Rules (block, alert, report) for leads, contacts and accounts.
- Run Duplicate Jobs to find existing duplicates.
- Merge duplicates with limits on merge counts.

## Gotchas
- Rules apply to API creates unless bypass options are set on the load.

## Self-check
Creating a known duplicate shows an alert or block.
