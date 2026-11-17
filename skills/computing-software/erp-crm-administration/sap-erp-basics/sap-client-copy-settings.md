---
id: computing-software.erp-crm-administration.sap-erp-basics.sap-client-copy-settings
name: sap-client-copy-settings
category: computing-software
field: erp-crm-administration
product: sap-erp-basics
tags: [sap-erp-basics, sap-client-copy-settings]
level: advanced
status: draft
description: "Create and copy clients safely."
sources: ['https://help.sap.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Manage clients with SCC4 and SCC1
**Goal:** Create and copy clients safely.

- SCC4 defines client role (production, test, customizing), changes and cross-client object protection.
- SCC1 copies transport requests between clients; SCCL performs local client copy (profiles such as SAP_CUST, SAP_ALL).
- Plan time and disk for copies.

## Gotchas
- Client copy overwrites target client data; confirm target.

## Self-check
New client appears in SCC4 and logon works.
