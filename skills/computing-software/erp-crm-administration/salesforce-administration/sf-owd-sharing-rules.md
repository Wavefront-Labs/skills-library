---
id: computing-software.erp-crm-administration.salesforce-administration.sf-owd-sharing-rules
name: sf-owd-sharing-rules
category: computing-software
field: erp-crm-administration
product: salesforce-administration
tags: [salesforce-administration, sf-role-hierarchy-sharing, sf-owd-sharing-rules]
level: practitioner
status: draft
description: "Start restrictive with OWD, then open access up with sharing rules."
sources: ['https://help.salesforce.com/', 'https://trailhead.salesforce.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Set org-wide defaults and sharing rules
**Goal:** Start restrictive with OWD, then open access up with sharing rules.

- Setup > Sharing Settings: per object choose Private, Public Read Only, Public Read/Write or Controlled by Parent.
- Sharing rules (owner-based or criteria-based) grant access to roles, groups or territories; they can only open access up, never restrict.
- Recalculate sharing after large changes and watch deferred recalculation.

## Gotchas
- "Grant Access Using Hierarchies" is on by default for standard objects; custom objects can switch it off.

## Self-check
A user in a different branch sees only the records the OWD and rules allow.
