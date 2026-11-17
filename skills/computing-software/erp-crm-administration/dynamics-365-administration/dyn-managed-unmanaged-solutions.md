---
id: computing-software.erp-crm-administration.dynamics-365-administration.dyn-managed-unmanaged-solutions
name: dyn-managed-unmanaged-solutions
category: computing-software
field: erp-crm-administration
product: dynamics-365-administration
tags: [dynamics-365-administration, dyn-solutions-alm, dyn-managed-unmanaged-solutions]
level: practitioner
status: draft
description: "Use solutions to move and version customisations."
sources: ['https://learn.microsoft.com/en-us/dynamics365/', 'https://learn.microsoft.com/en-us/power-platform/admin/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Package customisations with solutions
**Goal:** Use solutions to move and version customisations.

- Create a solution with a publisher (prefix); unmanaged for development, managed for deployment; managed layers stack in order.
- Add components via Add existing; use environment variables and connection references for environment-specific values.
- Do not customise outside solutions.

## Gotchas
- Deleting a managed solution removes its components.

## Self-check
Importing the managed solution in test reproduces the customisations.
