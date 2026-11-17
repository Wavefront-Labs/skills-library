---
id: computing-software.cloud-infrastructure-engineering.azure.policy-compliance-states-reasons-and-export
name: policy-compliance-states-reasons-and-export
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-policy, compliance-states, compliance-reasons, policy-states, policyresources, trigger-scan]
level: practitioner
status: docs-checked
description: "Read and report Azure Policy compliance: states and their maths, per-resource reasons, on-demand scans, CLI and Resource Graph queries, and Event Grid state events."
sources: ["https://learn.microsoft.com/azure/governance/policy/how-to/get-compliance-data", "https://learn.microsoft.com/azure/governance/policy/concepts/compliance-states", "https://learn.microsoft.com/azure/governance/policy/samples/resource-graph-samples"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Policy compliance states, reasons and export

**Goal:** trustworthy compliance numbers and a per-resource explanation for every non-compliant item.

## States
Compliant, Non-compliant, Exempt (resource is in the scope of an exemption), Conflicting (two or more assignments in the
same scope with contradicting rules, such as appending the same tag with different values), Not started (evaluation
cycle not started), Not registered (check that `Microsoft.PolicyInsights` is registered and the user has the RBAC
permissions), Error, Unknown (default for manual effect, an attestation is warranted), Protected (covered by a
`denyAction` assignment). Not started and Not registered are left out of rollups.
Compliance % = (compliant + exempt + unknown + protected) / (compliant + exempt + unknown + non-compliant +
conflicting + error + protected). An exempt resource has a compliance substate showing what its state would be without
the exemption (`properties.stateDetails.complianceSubState` in Resource Graph).

## Evaluation timing
- New assignment: about five minutes to apply to the scope, then the evaluation cycle begins.
- Resource deployed or updated through ARM, REST or an SDK: that resource is evaluated; exemption changes re-evaluate the assignment.
- Standard cycle: assignments are re-evaluated every 24 hours (no predefined completion time). On demand:
```bash
az policy state trigger-scan --resource-group rg-app            # or omit for subscription
az policy state trigger-scan --no-wait
```

## Query
```bash
az policy state summarize --subscription <sub> --query "results.{nonCompliantResources:nonCompliantResources,nonCompliantPolicies:nonCompliantPolicies}"
az policy state list --filter "complianceState eq 'NonCompliant' and policyAssignmentName eq '<assignment>'" \
  --query "[].{res:resourceId,policy:policyDefinitionName}" -o table
```
Resource Graph (across subscriptions, faster):
```kusto
policyresources
| where type == "microsoft.policyinsights/policystates"
| where properties.complianceState == "NonCompliant"
| summarize count() by assignment = tostring(properties.policyAssignmentName), subscriptionId
```

## Reasons
Portal: Policy > Compliance > assignment > resource; the compliance details pane lists the policies assigned to the
resource and its change history (for Resource Provider mode resources it opens component compliance).

## Export
Results are exposed by the `Microsoft.PolicyInsights` resource provider (PolicyStates and PolicyEvents) through the REST
API, `az policy state`, PowerShell and Resource Graph (`policyresources`). Summaries can be taken per container,
definition or assignment.

## Verify
- [ ] Dashboard numbers match `az policy state summarize`; each non-compliant resource has an owner or exemption.

## Checked
2026-10-28. Confirmed in Learn compliance-states and get-compliance-data: state definitions, rollup exclusions, compliance
percentage formula, substate property, five minute assignment delay, 24 hour cycle, PolicyInsights provider and the
summarize and trigger-scan commands. Removed: 15 minute and 5-30 minute timings, the Event Grid topic and event names,
Defender for Cloud and Power BI export, the 90 day history gotcha, the Not started cause and ARG lag gotchas, and the
Compliance details field example.
Method: documentation only; no commands were run.
