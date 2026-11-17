---
id: computing-software.erp-crm-administration.salesforce-administration.sf-scheduled-flows
name: sf-scheduled-flows
category: computing-software
field: erp-crm-administration
product: salesforce-administration
tags: [salesforce-administration, sf-scheduled-flows]
level: advanced
status: draft
description: "Run batch-like automation on a schedule."
sources: ['https://help.salesforce.com/', 'https://trailhead.salesforce.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Run scheduled flows
**Goal:** Run batch-like automation on a schedule.

- New Scheduled-Triggered Flow: choose start date, frequency and object filter; actions run per record batch.
- Be aware of per-record limits and batch processing; keep conditions selective.
- Monitor with Scheduled Jobs and flow error emails.

## Gotchas
- Scheduled flows run as the Automated Process user context settings; check permissions.

## Self-check
Next run appears in Scheduled Jobs.
