---
id: computing-software.erp-crm-administration.sap-erp-basics.sap-su01-user-maintenance
name: sap-su01-user-maintenance
category: computing-software
field: erp-crm-administration
product: sap-erp-basics
tags: [sap-erp-basics, sap-users-authorizations, sap-su01-user-maintenance]
level: practitioner
status: draft
description: "Create, lock and change users."
sources: ['https://help.sap.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Maintain users with SU01
**Goal:** Create, lock and change users.

- SU01 maintains users: address, logon data (user type Dialog/System/Service/Communication/Reference), roles tab, profiles and validity.
- SU10 for mass changes; lock with the lock button or via `SU01` lock status; initial passwords force change.
- Avoid shared dialog users.

## Gotchas
- User types matter: system and service users bypass password expiry rules.

## Self-check
New user can log on and sees assigned roles.
