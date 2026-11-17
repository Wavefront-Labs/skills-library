---
id: computing-software.erp-crm-administration.salesforce-administration.sf-freeze-deactivate-users
name: sf-freeze-deactivate-users
category: computing-software
field: erp-crm-administration
product: salesforce-administration
tags: [salesforce-administration, sf-users-licenses, sf-freeze-deactivate-users]
level: practitioner
status: draft
description: "Remove access safely: freeze first, then reassign work and deactivate."
sources: ['https://help.salesforce.com/', 'https://trailhead.salesforce.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Freeze, deactivate and offboard users
**Goal:** Remove access safely: freeze first, then reassign work and deactivate.

- Setup > Users: Freeze blocks login immediately without releasing the licence; Deactivate releases the licence.
- Users with assignments (workflow approvers, owner in assignment rules, default case owner) cannot be deactivated until reassigned; users cannot be deleted.
- Transfer record ownership, reassign approvals, then deactivate; remove from public groups and queues.

## Gotchas
- Freeze and deactivate do not revoke existing session tokens by themselves; terminate sessions via Setup > Session Management.

## Self-check
The user cannot log in and the licence count has dropped after deactivation.
