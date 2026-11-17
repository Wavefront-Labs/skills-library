---
id: computing-software.erp-crm-administration.salesforce-administration.sf-permission-set-groups
name: sf-permission-set-groups
category: computing-software
field: erp-crm-administration
product: salesforce-administration
tags: [salesforce-administration, sf-profiles-permission-sets, sf-permission-set-groups]
level: practitioner
status: draft
description: "Bundle permission sets by job function and mute unwanted permissions."
sources: ['https://help.salesforce.com/', 'https://trailhead.salesforce.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Build permission set groups
**Goal:** Bundle permission sets by job function and mute unwanted permissions.

- Create permission sets for capabilities, then combine them in a Permission Set Group and assign the group.
- Muting permission sets inside a group remove specific permissions without editing the source sets.
- Check the group status (Updated) after changing member sets.

## Gotchas
- Group calculation is asynchronous; wait for Updated status before testing.

## Self-check
"View Summary" on the user shows the expected effective permissions.
