---
id: computing-software.systems-network-administration.patch-management.cmdb-reconciliation-for-patching
name: cmdb-reconciliation-for-patching
category: computing-software
field: systems-network-administration
product: patch-management
tags: [cmdb-reconciliation, cmdb, configuration-items, software-inventory, identification-rules, patch-coverage]
level: practitioner
status: draft
description: "Reconcile the CMDB with discovery and patch-tool data: identification keys, source precedence, duplicate and stale CI handling, and coverage gap reports."
sources:
  - https://www.axelos.com/certifications/itil-service-management/itil-4-practitioner-service-configuration-management
  - https://www.servicenow.com/docs/bundle/xanadu-servicenow-platform/page/product/configuration-management/concept/c_ReconciliationRules.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CMDB reconciliation

**Goal:** a CMDB that patch scoping, maintenance groups and SLA reporting can trust.

## Identification
Pick strong keys per CI class: serial number plus manufacturer for physical, BIOS UUID / instance ID for VMs and cloud, never hostname alone (renames and reuse). Configure identification rules so each discovery source matches existing CIs instead of creating duplicates (e.g. ServiceNow Identification and Reconciliation Engine).

## Source precedence
Decide which source owns each attribute:
| Attribute | Authoritative source |
|---|---|
| OS version, installed software | Endpoint/patch agent |
| IP, MAC | Network discovery |
| Owner, business service, criticality | Manual/ITSM |
| Cloud tags, size | Cloud API |
Set reconciliation rules so lower-priority sources cannot overwrite higher ones.

## Regular reconciliation jobs
1. **Duplicates**: group CIs by serial/UUID; merge keeping the oldest record ID.
2. **Stale**: CIs not seen by any discovery source in 30-60 days: verify, then retire.
3. **Coverage**: CIs in an operational status with no patch-agent check-in: feed the unmanaged-assets process.
4. **Orphans**: agents reporting hosts that have no CI: create the CI.

## Report
Coverage = CIs with patch agent reporting in last 7 days / operational CIs in scope. Track by business service and asset tier.

## Gotchas
- Retiring CIs too aggressively hides offline-but-real systems (DR, seasonal); use a "not discovered" state before retirement.
- Hand-edited attributes get overwritten unless precedence is configured.

## Verify
Sample 20 random operational CIs monthly: each exists, has correct owner, and appears in patch reporting.
