---
id: computing-software.erp-crm-administration.sap-erp-basics.sap-sm50-sm21-system-log
name: sap-sm50-sm21-system-log
category: computing-software
field: erp-crm-administration
product: sap-erp-basics
tags: [sap-erp-basics, sap-system-monitoring, sap-sm50-sm21-system-log]
level: practitioner
status: draft
description: "See what the app server is doing."
sources: ['https://help.sap.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Read work processes and the system log
**Goal:** See what the app server is doing.

- SM50 shows work processes on a server and SM66 across the system; SM21 reads the system log.
- Look for long-running dialog processes and PRIV mode.
- AL11 shows application server directories and files.

## Gotchas
- Killing a work process can cause data inconsistencies if mid-update.

## Self-check
Stuck process identified and cause traced.
