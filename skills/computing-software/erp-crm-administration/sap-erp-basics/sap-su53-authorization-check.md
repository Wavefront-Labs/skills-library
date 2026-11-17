---
id: computing-software.erp-crm-administration.sap-erp-basics.sap-su53-authorization-check
name: sap-su53-authorization-check
category: computing-software
field: erp-crm-administration
product: sap-erp-basics
tags: [sap-erp-basics, sap-authorization-troubleshooting, sap-su53-authorization-check]
level: practitioner
status: draft
description: "Find which authorization object failed."
sources: ['https://help.sap.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Diagnose missing authorisations with SU53
**Goal:** Find which authorization object failed.

- The user runs SU53 after the error to display the last failed authorization check; admin compares with PFCG.
- ST01 trace records checks for a session when SU53 is not enough.
- SUIM reports on users, roles and objects.

## Gotchas
- SU53 shows only the last failed check for that user.

## Self-check
Adding the missing value to the role fixes the error.
