---
id: computing-software.erp-crm-administration.dynamics-365-administration.dyn-pac-cli-solution-pipelines
name: dyn-pac-cli-solution-pipelines
category: computing-software
field: erp-crm-administration
product: dynamics-365-administration
tags: [dynamics-365-administration, dyn-pac-cli-solution-pipelines]
level: advanced
status: draft
description: "Script solution export/import."
sources: ['https://learn.microsoft.com/en-us/dynamics365/', 'https://learn.microsoft.com/en-us/power-platform/admin/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Automate with pac CLI and pipelines
**Goal:** Script solution export/import.

- `pac auth create --environment <URL>`, `pac solution export --name <name> --path <file> --managed`, `pac solution import --path <file>`.
- Power Platform Pipelines offers in-product deployments between environments; Azure DevOps and GitHub Actions use Power Platform Build Tools.
- Store solutions unpacked in Git (`pac solution unpack`).

## Gotchas
- Use service principals, not personal accounts, for automation.

## Self-check
Import in the target succeeds without missing dependencies.
