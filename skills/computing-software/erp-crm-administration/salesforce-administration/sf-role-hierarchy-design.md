---
id: computing-software.erp-crm-administration.salesforce-administration.sf-role-hierarchy-design
name: sf-role-hierarchy-design
category: computing-software
field: erp-crm-administration
product: salesforce-administration
tags: [salesforce-administration, sf-role-hierarchy-design]
level: practitioner
status: draft
description: "Model data visibility, not the org chart."
sources: ['https://help.salesforce.com/', 'https://trailhead.salesforce.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Design the role hierarchy
**Goal:** Model data visibility, not the org chart.

- Roles determine who sees records owned by subordinates; users can have one role.
- Keep the hierarchy shallow; deep hierarchies and many users per owner slow sharing recalculation.
- Use public groups and queues for lateral sharing rather than extra role levels.

## Gotchas
- Role hierarchy does not give edit access beyond what the OWD and sharing permit.

## Self-check
A manager can see reports' records and not peers' records in a test.
