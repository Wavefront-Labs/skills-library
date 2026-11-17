---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-data-source-configuration
name: grafana-data-source-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana, data-sources, prometheus-datasource-config, loki-datasource-config, cloudwatch-datasource, azure-monitor-datasource, postgres-datasource, mysql-datasource, sql-datasource]
level: practitioner
status: gated
description: "Configure the key Grafana data sources: Prometheus (scrape interval, POST, exemplars), Loki (derived fields, max lines), CloudWatch and Azure Monitor auth, and SQL sources safely."
sources: ["https://grafana.com/docs/grafana/latest/datasources/prometheus/configure/", "https://grafana.com/docs/grafana/latest/datasources/loki/configure-loki-data-source/", "https://grafana.com/docs/grafana/latest/datasources/aws-cloudwatch/", "https://grafana.com/docs/grafana/latest/datasources/azure-monitor/", "https://grafana.com/docs/grafana/latest/datasources/postgres/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data source configuration

## Prometheus / Mimir / Thanos
- **Scrape interval** = your real scrape interval (drives `$__rate_interval`); **Query timeout**; **HTTP method POST**
  (long queries); **Prometheus type/version** (enables features like native histograms, label APIs; the effect of the type/version was not tested). Provisioning keys that were stored and read back on 13.2.4: `jsonData.timeInterval`, `queryTimeout`, `httpMethod`, `prometheusType`, `prometheusVersion`. `$__rate_interval` check: with the default scrape interval a query `rate(x[$__rate_interval])` at a 15 s step executed as `[1m0s]`; with `timeInterval: 5s` it executed as `[20s]`.
- **Exemplars**: internal link to Tempo, label name `trace_id` (`jsonData.exemplarTraceIdDestinations: [{name: trace_id, datasourceUid: tempo}]` was stored; the click-through to Tempo was not run) (gated: unconfirmed, source is paywalled or blocked).
- **Incremental querying** (`incrementalQuerying`) / **query overlap window** (`incrementalQueryOverlapWindow`, e.g. `5m`) (cache-friendly dashboards on Mimir): keys stored; the caching effect was not measured (gated: unconfirmed, source is paywalled or blocked).
- Custom query parameters (`customQueryParameters: max_source_resolution=auto`, stored) for Thanos downsampled data (not run against Thanos) (gated: unconfirmed, source is paywalled or blocked).
- **Manage alerts via Alerting UI** is `jsonData.manageAlerts` (stored with `false`).

## Loki
No Loki ran here, so this section was not tested (gated: unconfirmed, source is paywalled or blocked).
- **Maximum lines** (default 1000) per log query.
- **Derived fields**: regex `traceID=(\w+)` or label-based -> internal link to Tempo `${__value.raw}`. In a provisioning file write `$${__value.raw}`: Grafana expands `${...}` from the environment when it reads data source YAML (a correlation query `{pod="${pod}"}` was stored as `{pod=""}`; `$${pod}` kept `${pod}`).
- Timeout and multi-tenancy header `X-Scope-OrgID` (custom header) if Loki has auth enabled.

## CloudWatch
No AWS account was used, so the CloudWatch, Azure Monitor and SQL sections below were not run (gated: unconfirmed, source is paywalled or blocked).
- Auth: **AWS SDK default** (IRSA/instance role, recommended on EKS/EC2), Credentials file, or Access/secret key;
  optional **Assume role ARN** + External ID for cross-account.
- IAM: `cloudwatch:GetMetricData`, `ListMetrics`, `logs:StartQuery`/`GetQueryResults`, `ec2:DescribeRegions`,
  `tag:GetResources`.
- Cost: GetMetricData is billed per metric; long ranges with many dimensions are expensive. Use Metric Insights
  SQL queries and longer min intervals.

## Azure Monitor
- App registration (client ID/secret, tenant) with **Monitoring Reader** on subscriptions, or Managed Identity /
  Workload Identity when Grafana runs in Azure (`managed_identity_enabled = true` in `[azure]`).
- Query types: Metrics, Logs (KQL against Log Analytics), Azure Resource Graph, Traces (App Insights).

## SQL (PostgreSQL, MySQL, MSSQL)
- Use a **read-only** DB user with access only to reporting views; Grafana doesn't sandbox SQL.
- Max open/idle connections, connection max lifetime; TLS mode.
- Macros: `$__timeFilter(ts)`, `$__timeGroupAlias(ts, $__interval)`, `$__unixEpochFilter(col)`.
```sql
SELECT $__timeGroupAlias(created_at, '5m'), count(*) AS orders
FROM orders WHERE $__timeFilter(created_at) GROUP BY 1 ORDER BY 1
```

## Verify
- [ ] "Save & test" passes for each data source with the production auth method (no static keys where roles exist).
- [ ] Exemplars and derived-field links jump to the right trace.

## Checked
Environment: Windows 11, Grafana OSS 13.2.4, Prometheus 3.15.1.
- Provisioned a Prometheus data source with the jsonData keys above and read them back from `/api/datasources/uid/<uid>`; ran `/api/ds/query` against a default and a `timeInterval: 5s` data source and read `executedQueryString`; provisioned a correlation with `${pod}` and saw it blanked, then fixed with `$${pod}`. Key names cross-checked with the Grafana Prometheus configure docs.
- Loki, CloudWatch, Azure and SQL could not run: gated markers, so the skill is `gated`.
