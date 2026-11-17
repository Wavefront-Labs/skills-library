---
id: computing-software.erp-crm-administration.salesforce-administration.sf-change-sets-vs-cli
name: sf-change-sets-vs-cli
category: computing-software
field: erp-crm-administration
product: salesforce-administration
tags: [salesforce-administration, sf-change-sets-vs-cli]
level: advanced
status: draft
description: "Move metadata between orgs and keep it in version control."
sources: ['https://help.salesforce.com/', 'https://trailhead.salesforce.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Deploy with change sets or Salesforce CLI
**Goal:** Move metadata between orgs and keep it in version control.

- Change sets: outbound set in source, inbound in target after a deployment connection; no deletions.
- Salesforce CLI: `sf project retrieve start`, `sf project deploy start -x manifest/package.xml`, run tests in production with test levels; keep metadata in Git.
- Validate before deploy; order dependent components.

## Gotchas
- Change sets cannot delete components; CLI destructive changes can.

## Self-check
Deployment succeeds with required test coverage.
