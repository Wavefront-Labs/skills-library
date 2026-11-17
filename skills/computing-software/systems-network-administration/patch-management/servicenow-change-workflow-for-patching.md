---
id: computing-software.systems-network-administration.patch-management.servicenow-change-workflow-for-patching
name: servicenow-change-workflow-for-patching
category: computing-software
field: systems-network-administration
product: patch-management
tags: [servicenow-change, servicenow, change-model, standard-change, change-enablement, patch-management]
level: practitioner
status: draft
description: "Run patching through ServiceNow change: standard change templates for routine patches, normal change states and approvals, emergency path, and automating records via API."
sources:
  - https://www.servicenow.com/docs/bundle/xanadu-it-service-management/page/product/change-management/concept/c_ChangeManagement.html
  - https://www.servicenow.com/docs/bundle/xanadu-api-reference/page/integrate/inbound-rest/concept/change-management-api.html
  - https://www.servicenow.com/docs/bundle/xanadu-it-service-management/page/product/change-management/concept/c_StandardChangeCatalogPlugin.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ServiceNow change workflow for patching

## Choose the change type
- **Standard change** (pre-approved template) for the routine monthly cycle once it has a track record: template "Monthly Windows server patching - tier 2/3". Raised from the Standard Change Catalog; no CAB.
- **Normal change** for tier-1 systems, new patch types, or first-time procedures; follows assess -> authorize -> scheduled -> implement -> review.
- **Emergency change** for zero-days; expedited approval (ECAB), retrospective review.

## Normal change states (default model)
New -> Assess (technical approval by assignment group) -> Authorize (CAB/change manager) -> Scheduled -> Implement -> Review -> Closed. Planned start/end, implementation plan, backout plan, test plan and risk assessment are required before Assess.

## Automate creation
```sh
curl -s -u "$SN_USER:$SN_PASS" -H 'Content-Type: application/json' \
  -X POST "https://<instance>.service-now.com/api/sn_chg_rest/change/standard/<template_sys_id>" \
  -d '{"short_description":"Oct 2026 patching wave 2","start_date":"2026-10-21 22:00:00","end_date":"2026-10-22 02:00:00","cmdb_ci":"<ci_sys_id>"}'
```
Normal: `POST /api/sn_chg_rest/change/normal`; add affected CIs via `task_ci` table; update state via `PATCH /api/sn_chg_rest/change/{sys_id}` when the window starts/ends. Patch tools (Ansible AAP, ConfigMgr orchestrations) can check `GET .../change/{sys_id}` for state `Implement` before running.

## Closing
Close code (Successful / Successful with issues / Unsuccessful), close notes with patch success numbers, link incidents raised during the window. Feeds change success rate metrics.

## Gotchas
- Standard change templates need periodic review; failures should demote a template back to normal.
- Large waves: one change per wave with affected CIs listed, not one change per server (noise) or one per month (no traceability).
- Conflict detection only works if affected CIs and planned dates are set.

## Verify
Each patch window maps to a change in Implement state at execution time; post-window closure within 1 business day with accurate close code.
