---
id: computing-software.erp-crm-administration.sap-erp-basics.sap-sm59-rfc-destinations
name: sap-sm59-rfc-destinations
category: computing-software
field: erp-crm-administration
product: sap-erp-basics
tags: [sap-erp-basics, sap-rfc-connections, sap-sm59-rfc-destinations]
level: advanced
status: draft
description: "Create and test RFC connections."
sources: ['https://help.sap.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Configure RFC destinations with SM59
**Goal:** Create and test RFC connections.

- SM59 holds types: 3 (ABAP), H (HTTP to ABAP), G (HTTP external), T (TCP/IP).
- Test Connection and Authorization Test buttons; use secure SNC where possible.
- Do not store passwords for powerful users; use trusted RFC with care.

## Gotchas
- Stored credentials with SAP_ALL on an RFC are a serious risk.

## Self-check
Connection test succeeds with correct authorization.
