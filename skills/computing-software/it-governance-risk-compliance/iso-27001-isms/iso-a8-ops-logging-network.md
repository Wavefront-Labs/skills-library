---
id: computing-software.it-governance-risk-compliance.iso-27001-isms.iso-a8-ops-logging-network
name: iso-a8-ops-logging-network
category: computing-software
field: it-governance-risk-compliance
product: iso-27001-isms
tags:
- iso-27001-isms
- iso-a8-ops-logging-network
level: practitioner
status: draft
description: 'Implement Annex A 8.9-8.23: configuration management, deletion, masking, DLP, backup, redundancy, logging, monitoring, clocks, network security, web filtering.'
sources:
- https://www.iso.org/standard/27001
- https://www.iso.org/standard/75652.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# A.8 configuration, backup, logging, network, data protection
**Goal:** operational technical controls including 2022 additions.
- New in 2022: 8.9 configuration management; 8.10 information deletion; 8.11 data masking; 8.12 data leakage prevention; 8.16 monitoring activities; 8.23 web filtering.
- Also 8.13 backup; 8.14 redundancy; 8.15 logging; 8.17 clock synchronisation; 8.18 privileged utility programs; 8.19 software installation; 8.20 network security; 8.21 security of network services; 8.22 segregation of networks.
- Evidence: hardened baselines, restore test results, log review records, network diagrams.

## Gotchas
- Backups never test-restored; logs collected but never reviewed.

## Self-check
Perform a restore test and record time and success.
