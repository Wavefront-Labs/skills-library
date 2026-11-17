---
id: computing-software.data-science-and-analytics.bi-tools.pbi-deployment-pipelines
name: pbi-deployment-pipelines
category: computing-software
field: data-science-and-analytics
product: bi-tools
tags: [deployment-pipelines, workspace-roles, power-bi-app]
level: advanced
status: docs-checked
description: "Separate development, test and production, promote content with Fabric deployment pipelines and understand item pairing."
sources:
  - https://learn.microsoft.com/power-bi/create-reports/deployment-pipelines-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deployment
- A pipeline has two to 10 stages (default three: Development, Test, Production). Deployment clones content from a source stage to the next; at least one item must be selected.
- Pairing links an item to the same item in the adjacent stage. Paired items are overwritten on deploy and keep their pairing if renamed; unpaired items with identical names are not overwritten and a duplicate is created. Items added after a workspace is assigned are not automatically paired.
- Items that exist only in the target stage remain as they are.
- Use Test for sharing with reviewers, running tests with larger data volumes and checking how the app looks to end users; Production shares the final version with business users.
- Deployment rules are created in the pipeline (see Get started with deployment pipelines); an optional deployment plan (preview) adds order and actions.
- Automate with the Power BI or Fabric deployment pipelines REST APIs.
## Gotchas
- Since 12 February 2026 Fabric deployment pipelines no longer support semantic models that are not upgraded to Enhanced Metadata. Only listed item types deploy, and several are preview; check the supported items list.
- Pipelines deploy to the service; for version control use Git integration (the page points to its own documentation).
## Verify
- [ ] Test stage numbers reconcile before promoting.

## Checked
Confirmed on the deployment pipelines introduction: stage count and defaults, stage purposes, pairing rules, overwrite behaviour, deployment plan (preview), REST API automation, Enhanced Metadata retirement date, Git integration pointer. Removed: Premium/Fabric capacity licensing statement, apps with audiences, endorsement/certification advice and "keep .pbix in source control" (not stated on the page); deployment rule details were not read beyond the link text.
Method: docs-checked 2026-11-09 against the Microsoft Learn deployment pipelines introduction page (Fabric), read in full.
