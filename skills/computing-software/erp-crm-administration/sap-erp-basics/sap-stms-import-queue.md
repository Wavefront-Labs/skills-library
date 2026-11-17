---
id: computing-software.erp-crm-administration.sap-erp-basics.sap-stms-import-queue
name: sap-stms-import-queue
category: computing-software
field: erp-crm-administration
product: sap-erp-basics
tags: [sap-erp-basics, sap-stms-import-queue]
level: advanced
status: draft
description: "Import to the next system."
sources: ['https://help.sap.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Import transports with STMS
**Goal:** Import to the next system.

- STMS import queue per system: add requests, import individually or all, check return codes (0 or 4 = success or warning; 8 or higher is an error).
- Use transport routes and consolidation.
- Respect import order for dependent objects.

## Gotchas
- Importing out of order can overwrite newer versions.

## Self-check
Return code 0 or 4 and the change visible in the target.
