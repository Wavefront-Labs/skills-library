---
id: computing-software.erp-crm-administration.salesforce-administration.sf-lookup-vs-master-detail
name: sf-lookup-vs-master-detail
category: computing-software
field: erp-crm-administration
product: salesforce-administration
tags: [salesforce-administration, sf-lookup-vs-master-detail]
level: practitioner
status: draft
description: "Decide ownership and cascade behaviour."
sources: ['https://help.salesforce.com/', 'https://trailhead.salesforce.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choose lookup or master-detail relationships
**Goal:** Decide ownership and cascade behaviour.

- Master-detail: detail inherits sharing and owner from master, cascades delete, supports roll-ups; the child record needs the parent.
- Lookup: independent records, optional parent, supports clearing; can be hierarchical for the same object.
- An object can have at most two master-detail relationships; a standard object cannot be the detail side.

## Gotchas
- Converting a lookup to master-detail requires every child to have a parent first.

## Self-check
Deleting a master removes its detail records in a sandbox test.
