---
id: computing-software.cloud-infrastructure-engineering.azure.resource-graph-policy-health-advisor-and-security-tables
name: resource-graph-policy-health-advisor-and-security-tables
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, resource-graph, policyresources, healthresources, advisorresources, securityresources, governance-queries]
level: practitioner
status: draft
description: "Query Azure Resource Graph governance tables: policy states, resource health, Advisor recommendations, Defender assessments and patch data across all subscriptions."
sources: ["https://learn.microsoft.com/azure/governance/resource-graph/reference/supported-tables-resources", "https://learn.microsoft.com/azure/governance/resource-graph/samples/samples-by-table", "https://learn.microsoft.com/azure/governance/policy/samples/resource-graph-samples"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Resource Graph governance tables

**Goal:** answer estate-wide governance questions in seconds, beyond the `resources` table.

## Tables worth knowing
| Table | Contains |
|---|---|
| `policyresources` | Policy states, exemptions, remediations, attestations |
| `healthresources` | Resource Health availability statuses |
| `advisorresources` | Advisor recommendations (cost, security, reliability, performance, opex) |
| `securityresources` | Defender for Cloud assessments, sub-assessments, secure scores, alerts |
| `patchassessmentresources` / `patchinstallationresources` | Update Manager results |
| `resourcechanges` | Change history (14 days) |
| `servicehealthresources` | Service Health events affecting your subscriptions |
| `recoveryservicesresources` | Backup items and jobs |

## Examples
```kusto
// Non-compliant resources per assignment
policyresources
| where type == "microsoft.policyinsights/policystates" and properties.complianceState == "NonCompliant"
| summarize count() by tostring(properties.policyAssignmentName)

// Unhealthy resources now
healthresources
| where type == "microsoft.resourcehealth/availabilitystatuses"
| where properties.availabilityState != "Available"
| project id, state = properties.availabilityState, reason = properties.reasonType

// Advisor cost savings by subscription
advisorresources
| where type == "microsoft.advisor/recommendations" and properties.category == "Cost"
| extend savings = todouble(properties.extendedProperties.annualSavingsAmount)
| summarize annualSavings = sum(savings) by subscriptionId

// Unhealthy Defender recommendations, high severity
securityresources
| where type == "microsoft.security/assessments"
| where properties.status.code == "Unhealthy" and properties.metadata.severity == "High"
| summarize count() by tostring(properties.displayName)
```
```bash
az graph query -q "<query>" --management-groups mg-contoso --first 1000
```

## Joining with resources
```kusto
advisorresources
| where type == "microsoft.advisor/recommendations"
| extend rid = tolower(tostring(properties.resourceMetadata.resourceId))
| join kind=leftouter (resources | project rid = tolower(id), tags) on rid
```
Lower-case IDs before joining - casing differs across tables.

## Gotchas
- Not all properties are documented; inspect a row with `| take 1` and explore `properties`.
- Some tables need specific RBAC (security data needs Security Reader).
- Results reflect latest snapshot, not history (except `resourcechanges`).

## Verify
- [ ] Counts match the respective blades (Policy compliance, Advisor, Defender) for a sample subscription.
