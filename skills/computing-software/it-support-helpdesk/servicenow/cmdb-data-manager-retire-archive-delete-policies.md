---
id: computing-software.it-support-helpdesk.servicenow.cmdb-data-manager-retire-archive-delete-policies
name: cmdb-data-manager-retire-archive-delete-policies
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, cmdb-data-manager, cmdb, ci-lifecycle, retire-policy, archive-policy]
level: advanced
status: gated
description: "Use ServiceNow CMDB Data Manager to retire, archive and delete stale CIs with policies, filters, approvals and dry runs, without breaking relationships or audit history."
sources:
  - https://www.servicenow.com/docs/bundle/washingtondc-servicenow-platform/page/product/configuration-management/concept/cmdb-data-manager.html
  - https://www.servicenow.com/docs/bundle/washingtondc-servicenow-platform/page/product/configuration-management/concept/ci-lifecycle-management.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CMDB Data Manager: retire, archive and delete policies

**Problem:** discovery keeps adding CIs; nothing removes them. Stale CIs make impact analysis, licensing and incident routing wrong.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Lifecycle first
CMDB Data Manager acts on CIs by their CSDM lifecycle fields (`life_cycle_stage` / `life_cycle_stage_status`, older `install_status`/`operational_status`). Standardise these before automating.

## Policy types (CMDB Workspace > Data Manager)
| Policy | Effect | Typical rule |
|---|---|---|
| **Retire** | Sets lifecycle to Retired/End of Life; CI stays queryable | Not seen by discovery for 60 days (`last_discovered` older than X) |
| **Archive** | Moves CI records to archive tables, out of the live CMDB | Retired more than 180 days |
| **Delete** | Removes the CI (and optionally relationships) | Archived/retired more than N years and no legal need |

## Building a policy
1. Pick class (e.g. `cmdb_ci_computer`, `cmdb_ci_vmware_instance`) and conditions: `last_discovered` relative date, discovery source, lifecycle status, no open tasks.
2. Exclude CIs referenced by open incidents/changes or with active contracts (Asset).
3. Approvals: require a CI class owner group approval for delete policies.
4. **Preview** the matching set; run on a schedule with a cap per run.
5. Enable the policy; review the generated tasks and their results.

## Gotchas
- Retiring a CI does not retire its hardware asset; align Asset lifecycle (or use the CI-asset sync).
- Deleting CIs loses history used by reports; prefer archive for anything with incident history.
- Discovery that misses a host temporarily (firewall change) will retire live CIs; use thresholds longer than a discovery outage.
- Domain separation and ACLs affect which CIs the policy sees.

## Verify
CMDB Health dashboard staleness score improves; a sample of retired CIs is confirmed decommissioned by owners; no open task references a deleted CI.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
