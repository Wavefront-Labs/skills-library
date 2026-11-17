---
id: computing-software.systems-network-administration.patch-management.change-impact-analysis-with-cmdb
name: change-impact-analysis-with-cmdb
category: computing-software
field: systems-network-administration
product: patch-management
tags: [change-impact-analysis, cmdb, service-mapping, change-enablement, patch-management]
level: practitioner
status: draft
description: "Analyse change impact with the CMDB before patching: walk CI relationships to business services, find affected users and windows, flag conflicts and set risk accurately."
sources:
  - https://www.servicenow.com/docs/bundle/xanadu-it-service-management/page/product/change-management/concept/c_ChangeManagement.html
  - https://www.axelos.com/certifications/itil-service-management/itil-4-foundation
  - https://www.servicenow.com/docs/bundle/xanadu-servicenow-platform/page/product/configuration-management/concept/c_ITILConfigurationManagement.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Change impact analysis with the CMDB

A patch change on "SQL07" is low-risk until you learn SQL07 hosts payroll on payday.

## Steps
1. **Identify CIs** in scope (servers, clusters, appliances) from the patch group, and attach them as affected CIs on the change.
2. **Walk relationships upstream**: host -> application instance -> business application -> business service. In ServiceNow, use the "Refresh Impacted Services" related list (or Unified Map / dependency views); it populates Impacted Services/CIs from the CI relationships.
3. **Capture service details**: service owner, criticality, user base, SLA, business calendars (month-end, trading hours).
4. **Check conflicts**: Conflict Detection against blackout windows, maintenance schedules and other changes on the same CIs/services.
5. **Assess outage**: redundant (no user impact) vs single instance (outage for the window). Document expected user impact explicitly.
6. **Set risk/impact** from the above (risk assessment questionnaire or calculated risk).

## Without a good CMDB
Use observed dependencies: NetFlow/firewall logs, APM service maps (Dynatrace, AppDynamics), VMware/vRealize network insight, and confirm with app owners. Feed results back into the CMDB.

## Output in the change record
| Field | Example |
|---|---|
| Affected CIs | 12 servers listed |
| Impacted services | Payroll (critical), HR portal (medium) |
| User impact | none expected (rolling); payroll batch paused 02:00-03:00 |
| Conflicts | none; avoids month-end freeze |

## Gotchas
- Stale relationships (decommissioned apps still linked, new apps not linked) make analysis wrong in both directions; data quality reviews matter.
- Shared infrastructure (hypervisor clusters, storage, DNS) maps to almost every service; summarise by tier rather than listing hundreds.

## Verify
Post-change: incidents during the window were all on CIs listed in the impact analysis; any surprise dependency gets added to the CMDB.
