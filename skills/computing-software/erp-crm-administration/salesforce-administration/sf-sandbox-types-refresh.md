---
id: computing-software.erp-crm-administration.salesforce-administration.sf-sandbox-types-refresh
name: sf-sandbox-types-refresh
category: computing-software
field: erp-crm-administration
product: salesforce-administration
tags: [salesforce-administration, sf-sandboxes-deploy, sf-sandbox-types-refresh]
level: practitioner
status: draft
description: "Match sandbox type to use and plan refreshes."
sources: ['https://help.salesforce.com/', 'https://trailhead.salesforce.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choose sandbox types and manage refreshes
**Goal:** Match sandbox type to use and plan refreshes.

- Developer and Developer Pro hold configuration only (different storage), Partial Copy holds a sample of data via a sandbox template, Full copies production data.
- Refresh intervals differ by type (confirm current intervals in Salesforce Help); refresh resets metadata and data.
- Run Apex for post-refresh cleanup (mask emails, update integrations).

## Gotchas
- Sandbox users' emails are modified; integrations pointing at production must be repointed.

## Self-check
After refresh the sandbox has the expected data and settings.
