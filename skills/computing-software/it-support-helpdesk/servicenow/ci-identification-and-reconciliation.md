---
id: computing-software.it-support-helpdesk.servicenow.ci-identification-and-reconciliation
name: ci-identification-and-reconciliation
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, cmdb, configuration-item, ci-reconciliation, duplicate-ci, identification-engine, ire, itil-4, data-source-precedence]
level: practitioner
status: gated
description: "Stop and fix duplicate CIs: ServiceNow IRE identification rules, reconciliation and data-source precedence, the de-duplication task workflow, and merging without losing history."
sources:
  - "https://www.servicenow.com/docs/"
  - "https://www.axelos.com/certifications/itil-service-management"
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# ci-identification-and-reconciliation
Goal: one real device = one CI, whichever tool reported it, and the most
trustworthy source wins each field.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Why duplicates appear
- Different sources identify differently (Intune by serial, Discovery by
  hostname + MAC, manual entry by name with typo).
- Reimaged laptop gets a new name; renamed CI created instead of matched.
- Virtual machines cloned with the same serial (VMware UUID quirks).
- Imports bypassing IRE (transform maps writing straight to the table).

## Identification (IRE)
- **Identification rules** per class, in priority order: e.g. computer →
  1. serial number + serial type, 2. name, 3. MAC address. CI Class
  Manager > Identification Rule.
- All integrations should write via IRE (`IdentificationEngine` API /
  Service Graph Connectors / Discovery). Fix custom imports that do not.
- Exclude junk serials ("To be filled by O.E.M.", "0", "System Serial
  Number") using the serial number exclusion list.

## Reconciliation
- **Reconciliation rules** say which data source may update which
  attributes, with priority (e.g. Intune wins assigned_to and OS; SCCM
  wins installed software; Discovery wins IP).
- **Data refresh rules** stop a stale high-priority source blocking a
  fresher lower one.

## Cleaning existing duplicates
1. CMDB Health > Correctness > Duplicates (or the de-duplication
   dashboard) creates **De-duplication tasks** grouping suspects.
2. In the task, pick the main CI (oldest with most relationships and
   tickets), merge relationships and related records, retire the rest.
3. Use the **CMDB 360 / Multisource** view to see which source reported
   what before deciding.

## Gotchas
- Deleting a duplicate that has incidents, assets or contracts linked
  orphans that history; merge or retire instead.
- Name-only identification merges different devices called "LAPTOP01".
- Fixing duplicates without fixing the feeding integration means they
  come back next import.

## Verify
De-duplication task count trends down, a reimaged test laptop updates its
existing CI rather than creating a new one, and junk serials are excluded.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (axelos.com, servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
