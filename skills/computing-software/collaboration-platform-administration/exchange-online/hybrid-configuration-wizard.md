---
id: computing-software.collaboration-platform-administration.exchange-online.hybrid-configuration-wizard
name: hybrid-configuration-wizard
category: computing-software
field: collaboration-platform-administration
product: exchange-online
tags: [hybrid-configuration-wizard, exo-hybrid]
level: advanced
status: draft
description: Run the HCW and verify hybrid mail flow and free/busy.
sources: ['https://learn.microsoft.com/en-us/exchange/exchange-online', 'https://learn.microsoft.com/en-us/powershell/exchange/exchange-online-powershell']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hybrid Configuration Wizard
**Goal:** Run the HCW and verify hybrid mail flow and free/busy.

- Prerequisites: supported on-premises Exchange CU, public certificate, autodiscover and EWS published.
- Download the HCW from the Exchange admin center; choose Minimal or Full hybrid.
- Review the Organization Relationship and connectors it creates.
- Test: `Test-OrganizationRelationship`, free/busy lookups, cross-premises mail.

## Gotchas
- Keep at least one hybrid server; Microsoft documents a path for removing last server (confirm current guidance).
- Certificate name mismatch breaks secure mail flow.

## Self-check
Mail flows both ways and free/busy works in both directions.
