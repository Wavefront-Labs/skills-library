---
id: computing-software.cloud-infrastructure-engineering.azure.kql-saved-functions-and-make-series-time-series
name: kql-saved-functions-and-make-series-time-series
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, log-analytics, kql, kql-functions, make-series, series-decompose-anomalies, time-series]
level: advanced
status: docs-checked
description: "Write reusable KQL saved and let-functions, and analyse time series with make-series, series_decompose_anomalies, series_fit_line."
sources: ["https://learn.microsoft.com/kusto/query/make-series-operator", "https://learn.microsoft.com/azure/azure-monitor/logs/functions", "https://learn.microsoft.com/kusto/query/series-decompose-anomalies-function", "https://learn.microsoft.com/kusto/query/functions/user-defined-functions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KQL functions and make-series

**Goal:** reuse query logic across alerts and workbooks, and do trend and anomaly analysis in Log Analytics.

## Functions
Inline (query-scoped):
```kusto
let ErrRate = (t:timespan) { AppRequests | where TimeGenerated > ago(t) | summarize err=countif(Success == false), all=count() by AppRoleName | extend rate = 1.0*err/all };
ErrRate(1h)
```
Saved workspace function: in the query editor *Save → Save as function*, name `fn_ErrRate` with a parameter for each variable; or deploy a `savedSearches` resource with `displayName`, `functionAlias` and `functionParameters` (the functions page shows an ARM template):
```bicep
resource fn 'Microsoft.OperationalInsights/workspaces/savedSearches@2025-07-01' = {
  parent: law, name: 'fn-errrate'
  properties: { category: 'Functions', displayName: 'fn_ErrRate', functionAlias: 'fn_ErrRate',
    functionParameters: 't:timespan = 1h', query: 'AppRequests | where TimeGenerated > ago(t) | summarize ...' }
}
```
Saving and running saved functions needs `Microsoft.OperationalInsights/workspaces/savedSearches/write` and query permissions on the workspace. Keep function definitions in IaC.

## make-series
`make-series` assigns a default value (0 unless you set `default=`) to absent bins, producing arrays the series functions take. For interpolation functions use `default=double(null)`.
```kusto
AppRequests
| where TimeGenerated > ago(14d)
| make-series reqs = count() default=0 on TimeGenerated from ago(14d) to now() step 1h by AppRoleName
| extend (anomalies, score, baseline) = series_decompose_anomalies(reqs, 1.5, -1, 'linefit')
| render anomalychart with (anomalycolumns=anomalies)
```
Other useful functions:
- `series_decompose_anomalies(series, threshold, seasonality, trend)`: threshold default 1.5, seasonality default -1 (autodetect), trend `avg` (default), `linefit` or `none`.
- `series_fit_line(reqs)` finds the best-fit straight line.
- `mv-expand` the arrays back to rows.

## Gotchas
- With trend `avg` (the default) the baseline has no trend and trending series produce more variance; pass `'linefit'` when you expect a trend.

## Verify
- [ ] Function appears under Functions in the workspace and returns the same result as the inline version.

## Checked
2026-10-31. Confirmed against the make-series, series_decompose_anomalies and Azure Monitor functions pages: make-series
`default` behaviour, `series_decompose_anomalies` threshold/seasonality/trend defaults and the `'linefit'` example,
`series_fit_line`, Save as function, savedSearches properties and the ARM apiVersion shown (2025-07-01), the savedSearches/write
permission. Removed as unconfirmed: `series_decompose_forecast` and `series_stats_dynamic` usage, cardinality and alert-breakage
claims, the CommonSecurityLog parser suggestion and the `render` claim.
Method: documentation only; no commands were run.
