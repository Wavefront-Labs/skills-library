---
id: computing-software.erp-crm-administration.salesforce-administration.sf-business-hours-holidays
name: sf-business-hours-holidays
category: computing-software
field: erp-crm-administration
product: salesforce-administration
tags: [salesforce-administration, sf-org-setup, sf-business-hours-holidays]
level: practitioner
status: draft
description: "Define business hours and holidays that drive escalation, entitlements and milestones."
sources: ['https://help.salesforce.com/', 'https://trailhead.salesforce.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Configure business hours and holidays
**Goal:** Define business hours and holidays that drive escalation, entitlements and milestones.

- Setup > Company Settings > Business Hours: create hours per time zone, mark one default; add Holidays and link them to the hours.
- Business hours are referenced by escalation rules, entitlement processes and flows.
- Test a case timestamp against hours, since SLA clocks read these values.

## Gotchas
- Holidays must be attached to the business-hours record or they have no effect.

## Self-check
A case opened outside hours escalates only when hours restart.
