---
id: computing-software.erp-crm-administration.sap-erp-basics.sap-st22-abap-dumps
name: sap-st22-abap-dumps
category: computing-software
field: erp-crm-administration
product: sap-erp-basics
tags: [sap-erp-basics, sap-st22-abap-dumps]
level: practitioner
status: draft
description: "Diagnose ABAP runtime errors."
sources: ['https://help.sap.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Analyse short dumps in ST22
**Goal:** Diagnose ABAP runtime errors.

- ST22 lists dumps by date and user; open the dump to see the error type, source line and variables.
- Use SM13 for update errors and SM12 for lock entries.
- Escalate with the dump text to the developer or SAP.

## Gotchas
- Dumps expire; save them if needed.

## Self-check
Dump shows program and line, enabling a fix.
