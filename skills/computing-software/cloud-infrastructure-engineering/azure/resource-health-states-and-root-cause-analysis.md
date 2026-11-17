---
id: computing-software.cloud-infrastructure-engineering.azure.resource-health-states-and-root-cause-analysis
name: resource-health-states-and-root-cause-analysis
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, service-health, resource-health-states, root-cause-analysis, resource-health-alerts]
level: practitioner
status: docs-checked
description: "Interpret Resource Health states (Available, Unavailable, Degraded, Unknown), platform vs user-initiated causes, alert on transitions and retrieve root cause analyses."
sources: ["https://learn.microsoft.com/azure/service-health/resource-health-overview", "https://learn.microsoft.com/azure/service-health/resource-health-alert-arm-template-guide", "https://learn.microsoft.com/azure/service-health/resource-health-checks-resource-types"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resource Health states and RCA

**Goal:** tell quickly whether a single resource problem is Azure's or yours, and get the evidence afterwards.

## States
| State | Meaning | Action |
|---|---|---|
| Available | No platform events detected | Look in your app/config |
| Unavailable | Platform or user-initiated event made it unavailable; reason shows **Platform initiated** (unplanned/planned) or **User initiated** (stop, restart, config) | Platform: wait/failover; user: check Activity log |
| Degraded | Reduced performance but available | Check metrics, consider failover |
| Unknown | Health information is missing | Not necessarily down; validate with your own probes |

Health history is available in the Resource Health blade and API.

## Query
```bash
az rest --method get --url "https://management.azure.com/<resourceId>/providers/Microsoft.ResourceHealth/availabilityStatuses/current?api-version=<api-version>"
```
Take the current `api-version` from the Resource Health REST reference. Resource Graph can query the same data (table and column names not verified here).

## Alerts
Create an Activity log alert on Resource Health events; see the Resource Health alert ARM template guide for the exact condition fields (status, previous status, reason type). Filter on the platform-initiated reason type so user-initiated restarts do not alert.

## Root cause analysis
- Root cause information for platform-initiated events appears in Resource Health history and Service Health; check there (timing and coverage not verified here).

## Verify
- [ ] Test the alert on a non-prod resource with the reason-type filter temporarily removed.
- [ ] The incident review process links RCA/PIR documents.

## Checked
2026-10-28. Confirmed on the Resource Health overview page: states Available, Unavailable, Unknown (health information is missing), Degraded, and the reason type (platform or user initiated). Removed as unconfirmed: the 10-minute and 30-day figures, the pinned api-version, Resource Graph query, alert JSON field names, RCA timing and PIR claims.
Method: documentation only; no commands were run.
