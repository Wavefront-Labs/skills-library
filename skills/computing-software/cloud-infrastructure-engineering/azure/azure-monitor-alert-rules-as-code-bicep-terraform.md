---
id: computing-software.cloud-infrastructure-engineering.azure.azure-monitor-alert-rules-as-code-bicep-terraform
name: azure-monitor-alert-rules-as-code-bicep-terraform
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-monitor, alert-rules-bicep, alerts-as-code, terraform, action-groups, azure-monitor-baseline-alerts]
level: advanced
status: docs-checked
description: "Define metric, log search, activity log alerts and action groups in Bicep or Terraform, parameterise per environment, and use Azure Monitor Baseline Alerts."
sources: ["https://learn.microsoft.com/azure/azure-monitor/alerts/resource-manager-alerts-metric", "https://learn.microsoft.com/azure/azure-monitor/alerts/resource-manager-alerts-log", "https://azure.github.io/azure-monitor-baseline-alerts/welcome/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure Monitor alert rules as code

**Goal:** stop click-ops alerts; version, review and deploy alert rules with the workload.

## Bicep: metric alert
```bicep
resource cpu 'Microsoft.Insights/metricAlerts@<api-version>' = {
  name: 'vm-cpu-high', location: 'global'
  properties: {
    severity: 2, enabled: true, scopes: [ vm.id ], evaluationFrequency: 'PT5M', windowSize: 'PT15M'
    criteria: { 'odata.type': 'Microsoft.Azure.Monitor.SingleResourceMultipleMetricCriteria', allOf: [ {
      name: 'cpu', criterionType: 'StaticThresholdCriterion', metricName: 'Percentage CPU'
      operator: 'GreaterThan', threshold: 90, timeAggregation: 'Average' } ] }
    actions: [ { actionGroupId: ag.id } ]
  }
}
```
Metric alert `windowSize` and `evaluationFrequency` take ISO 8601 durations such as `PT1M`, `PT5M`, `PT15M` and `PT30M`; use the current API version from the Learn template page.

## Bicep: log search alert
```bicep
resource la 'Microsoft.Insights/scheduledQueryRules@2021-08-01' = {
  name: 'app-5xx', location: location
  properties: {
    severity: 1, enabled: true, scopes: [ workspace.id ], evaluationFrequency: 'PT5M', windowSize: 'PT5M', autoMitigate: true
    criteria: { allOf: [ { query: '<KQL query>', timeAggregation: 'Count',
      operator: 'GreaterThan', threshold: 10, failingPeriods: { numberOfEvaluationPeriods: 1, minFailingPeriodsToAlert: 1 } } ] }
    actions: { actionGroups: [ ag.id ] }
  }
}
```

## Practices
- One module per resource type with thresholds as parameters; environment files decide severity and action group (prod pages, dev emails).
- Start from **Azure Monitor Baseline Alerts (AMBA)**, which offers Azure Policy definitions and initiatives for deploying alerts at scale.
- Put action groups in a shared resource group; reference by ID.
- Validate with `az deployment group what-if` in CI.

## Gotchas
- Metric alerts on `location: 'global'`; log alerts need a real region.
- Log alerts using a measure other than a row count set `metricMeasureColumn` in the criteria.

## Verify
- [ ] `az monitor metrics alert list -g rg -o table` and `az monitor scheduled-query list -g rg -o table` match the repo.

## Checked
2026-10-28. Confirmed in Learn resource-manager-alerts-metric and resource-manager-alerts-log templates: metricAlerts location global, SingleResourceMultipleMetricCriteria,
StaticThresholdCriterion, PT durations, scheduledQueryRules with `failingPeriods`, `autoMitigate`, `metricMeasureColumn`, `actions.actionGroups`, and the
AMBA policy-based deployment. check_commands found the verification commands valid. Removed: the 2018-03-01 and 2023-03-15-preview API versions (docs show
`<ApiVersion>` and 2021-08-01), the ResultCode query, the Terraform resource name list and registry source (not fetched), multi-resource alert properties,
and the numeric-column and orphaned-alert gotchas. Terraform guidance was not verified.
Method: documentation only; no commands were run.
