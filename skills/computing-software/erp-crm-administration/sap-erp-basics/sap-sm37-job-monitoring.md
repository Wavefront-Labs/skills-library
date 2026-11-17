---
id: computing-software.erp-crm-administration.sap-erp-basics.sap-sm37-job-monitoring
name: sap-sm37-job-monitoring
category: computing-software
field: erp-crm-administration
product: sap-erp-basics
tags: [sap-erp-basics, sap-sm37-job-monitoring]
level: practitioner
status: draft
description: "Check, restart and troubleshoot jobs."
sources: ['https://help.sap.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Monitor jobs in SM37
**Goal:** Check, restart and troubleshoot jobs.

- SM37 filters by name, user, status (Scheduled, Released, Ready, Active, Finished, Cancelled).
- View the job log and spool for the cancel reason; copy or reschedule.
- Check ST22 for ABAP dumps behind a cancelled job.

## Gotchas
- Cancelled jobs often log a short dump in ST22.

## Self-check
Failed job cause is identified from log and dump.
