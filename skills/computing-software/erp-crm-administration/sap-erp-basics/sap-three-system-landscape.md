---
id: computing-software.erp-crm-administration.sap-erp-basics.sap-three-system-landscape
name: sap-three-system-landscape
category: computing-software
field: erp-crm-administration
product: sap-erp-basics
tags: [sap-erp-basics, sap-landscape-clients, sap-three-system-landscape]
level: practitioner
status: draft
description: "Recognise SAP system roles and transport routes."
sources: ['https://help.sap.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Understand the DEV, QAS and PRD landscape
**Goal:** Recognise SAP system roles and transport routes.

- A typical landscape has development (DEV), quality assurance (QAS) and production (PRD); changes flow by transport requests along routes defined in STMS.
- Each system has one or more clients (SCC4 lists them), with client-specific and cross-client customizing.
- Sandbox systems exist for experiments.

## Gotchas
- Customizing changes in production clients can be locked (client settings in SCC4) by design.

## Self-check
You can name which client and system a configuration item lives in.
