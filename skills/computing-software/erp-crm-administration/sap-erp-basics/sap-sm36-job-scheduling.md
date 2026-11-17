---
id: computing-software.erp-crm-administration.sap-erp-basics.sap-sm36-job-scheduling
name: sap-sm36-job-scheduling
category: computing-software
field: erp-crm-administration
product: sap-erp-basics
tags: [sap-erp-basics, sap-background-jobs, sap-sm36-job-scheduling]
level: practitioner
status: draft
description: "Create background jobs."
sources: ['https://help.sap.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Schedule jobs with SM36
**Goal:** Create background jobs.

- SM36 defines the job name, class, steps (ABAP program with variant), start conditions (immediate, date/time, after event or periodic).
- Use variants to supply parameters; set the job user to a service user.
- Avoid overlapping periodic jobs.

## Gotchas
- A job runs under the authorisations of the step user.

## Self-check
Job appears in SM37 as scheduled and then finished.
