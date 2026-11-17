---
id: computing-software.cloud-infrastructure-engineering.azure.service-health-resource-health-and-advisor
name: service-health-resource-health-and-advisor
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, service-health, resource-health, azure-advisor, advisor, azure-status, service-issues, planned-maintenance, health-advisories, security-advisories, health-alerts, resource-health-alerts, advisor-score, advisor-recommendations, reliability-recommendations, cost-recommendations, advisor-alerts, impacted-resources, incident-communications, change-analysis, resource-health-kql]
level: practitioner
status: draft
description: "Subscribe to platform signals: Service Health alerts by region/service, Resource Health alerts and KQL, impacted-resource lists, and Advisor score/recommendations run as a backlog."
sources: ["Microsoft Learn - Azure Service Health overview, alerts and impacted resources", "Microsoft Learn - Resource Health overview and alerts", "Microsoft Learn - Azure Advisor overview, Advisor score and recommendation alerts", "Microsoft Learn - Azure status page vs Service Health", "Microsoft Learn - Change Analysis in Azure Monitor"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Service Health, Resource Health and Advisor — platform signals you must subscribe to

**Goal:** platform incidents, maintenance and deprecations reach on-call and owners
automatically; a VM going `Unavailable` pages before the user ticket; Advisor's
reliability/cost findings are tracked like any other backlog.

## 1. Three sources, three scopes
| Source | Scope | Tells you |
|---|---|---|
| **Azure status** (status.azure.com) | global, public | only large multi-region incidents — never your only source |
| **Service Health** | your subscriptions | incidents affecting *your* resources/regions, planned maintenance (with dates), health advisories (deprecations, required actions), security advisories, billing updates |
| **Resource Health** | one resource | `Available` / `Unavailable` / `Degraded` / `Unknown` with cause `PlatformInitiated` vs `UserInitiated`, and history (30 days) |

## 2. Service Health alerts (one per subscription, deployed by policy)
```bash
az monitor activity-log alert create -g rg-ops -n svc-health-uks --scope /subscriptions/<sub> \
  --condition "category=ServiceHealth" --action-group ag-platform-oncall --description "Service Health: incidents/maintenance/advisories"
# Bicep: properties.condition.allOf += {field: 'properties.impactedServices[*].ImpactedRegions[*].RegionName', containsAny: ['UK South','UK West','Global']}
#        and {field: 'properties.incidentType', equals: 'Incident'} for a paging rule; separate rule for Maintenance/ActionRequired to the info group
```
- Split rules: **Incident + Security** → paging group; **Maintenance + Informational + ActionRequired** → ticket/chat group (ActionRequired = "migrate off X by date" — someone must own it).
- Filter regions to those you use plus *Global*; filter services only if the list is short — new services you adopt won't be covered otherwise.
- Built-in Policy *Configure subscriptions to enable Service Health alerts* (ALZ deploys it) — assign at the management group with the action group parameter.
- Portal *Service Health > Impacted resources* lists exactly which of your resources an incident touched; the incident ID/tracking ID goes in the post-incident review. *Health history* keeps 90 days; export via the Activity log (`ServiceHealth` category) for longer.

## 3. Resource Health
```bash
az monitor activity-log alert create -g rg-ops -n rh-vm-unavailable --scope /subscriptions/<sub> \
  --condition "category=ResourceHealth and properties.currentHealthStatus=Unavailable and properties.cause=PlatformInitiated" --action-group ag-platform-oncall
az rest --method get --url "https://management.azure.com<vm-id>/providers/Microsoft.ResourceHealth/availabilityStatuses/current?api-version=2022-10-01"
```
- Resource types covered include VMs/VMSS, App Service, SQL DB/MI, Cosmos, Redis, AKS, Storage, Key Vault, Load Balancer, Firewall, VPN/ER gateways, Event Hubs, Service Bus and more; `Unknown` = no signal for 10+ min (often a deallocated/stopped resource — filter it).
- Alert on `PlatformInitiated` + `Unavailable` for paging; `UserInitiated` (someone stopped it) to info; `Degraded` for storage/SQL warnings.
- KQL (needs the Activity log exported): `AzureActivity | where CategoryValue == "ResourceHealth" | extend s = tostring(parse_json(Properties).currentHealthStatus), c = tostring(parse_json(Properties).cause) | project TimeGenerated, _ResourceId, s, c`.
- Resource Graph `healthresources` table: `healthresources | where type =~ "microsoft.resourcehealth/availabilitystatuses" | extend state = tostring(properties.availabilityState) | summarize count() by state` — fleet health snapshot now.

## 4. Advisor as a backlog
- Five pillars: **Reliability** (no AZ/no backup/expired certs/SLA risks), **Security** (from Defender for Cloud), **Performance** (SKU/limits), **Cost** (idle/under-used, reservations), **Operational excellence** (Service Health alerts missing, policy, quotas). **Advisor score** per subscription/pillar — trend it monthly.
```bash
az advisor recommendation list --category Cost --query "[].{res:resourceMetadata.resourceId,impact:impact,desc:shortDescription.problem,saving:extendedProperties.annualSavingsAmount}" -o table
az advisor recommendation disable --ids <rec-id> --days 90     # snooze with a reason in the ticket
az advisor configuration update --low-cpu-threshold 10 --exclude false   # tune the "underutilised VM" CPU threshold (5/10/15/20)
```
- Resource Graph `advisorresources` for fleet-wide queries and dashboards (`properties.category`, `properties.impact`, `properties.extendedProperties.savingsAmount`).
- **Advisor alerts** (`az monitor activity-log alert create --condition "category=Recommendation and properties.recommendationCategory=HighAvailability and properties.recommendationImpact=High"`) push new high-impact items to the owning team's queue; weekly digest email per subscription via *Advisor > Recommendation digests*.
- Treat each High-impact reliability item as a ticket with an owner; cost items feed the FinOps review; "postpone" only with an expiry. Exclude sandbox subscriptions via Advisor configuration to keep the score honest.

## 5. Change Analysis and correlation
Azure Monitor *Change Analysis* (`Microsoft.ChangeAnalysis` provider) shows ARM property and app-setting changes in a time window — pair with a Resource Health `Unavailable` event: "what changed in the 24 h before?" Resource Graph `resourcechanges` gives the same for 14 days (see resource-graph skill). In a Service Health incident, the answer is usually "nothing you did" — confirm quickly and stop the war room from chasing ghosts.

## Gotchas
- Service Health alerts only cover subscriptions in scope at creation; new subscriptions need the policy or they're blind — the common gap in vended subscriptions.
- Activity-log alerts can't filter by resource tag; route by subscription/region instead.
- Resource Health `Unknown` after a VM deallocate is normal; alerting on `Unknown` floods.
- Advisor cost savings are estimates on list price without your discounts; validate before committing a number to finance.
- Advisor "Enable Backup" and "Use AZ" recommendations ignore workloads deliberately exempt (stateless scale sets) — snooze with a reason rather than letting them erode the score.
- Status page shows nothing for most incidents that hit you; if the team's first instinct is status.azure.com, the alerting is wrong.

## Verify
- [ ] Every subscription has ≥ 1 Service Health alert rule (`az monitor activity-log alert list --query "[?contains(condition.allOf[].equals, 'ServiceHealth')]"`) and the action group's test notification arrives.
- [ ] Stop a test VM from the platform side (or use *Resource Health > Report incorrect health*/a simulated event): the Resource Health alert fires with `PlatformInitiated` when applicable; `UserInitiated` goes to info only.
- [ ] Advisor score reviewed monthly; High-impact reliability recommendations have tickets or snoozes with expiry.
- [ ] A recent Service Health incident's impacted-resources list matches what on-call saw in their alerts.
