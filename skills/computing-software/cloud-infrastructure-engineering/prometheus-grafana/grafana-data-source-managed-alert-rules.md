---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-data-source-managed-alert-rules
name: grafana-data-source-managed-alert-rules
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [data-source-managed-rules, ruler-managed-rules, grafana-alerting, mimir-ruler, loki-alert-rules]
level: practitioner
status: docs-checked
description: "Create and edit Mimir and Loki ruler rules from the Grafana alerting UI (data source-managed) and decide between them and Grafana-managed rules."
sources: ["https://grafana.com/docs/grafana/latest/alerting/alerting-rules/create-data-source-managed-rule/", "https://grafana.com/docs/grafana/latest/alerting/fundamentals/alert-rules/", "https://grafana.com/docs/mimir/latest/references/http-api/#ruler"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data source-managed alert rules

Data source-managed rules are stored in the data source (Mimir, Loki) rather than in Grafana. In Grafana Alerting you can
create and edit them for Mimir and Loki data sources, view rules from Prometheus data sources when "Manage alerts via
Alerting UI" is enabled (read-only), and import data source-managed rules from Loki, Mimir and Prometheus into
Grafana-managed rules. Grafana recommends Grafana-managed rules whenever possible; data source-managed rules support
horizontal scalability but add operational complexity.

In Grafana Cloud, the pre-provisioned Loki and Prometheus data source-managed alerts cannot be created in new stacks; your own
Mimir, Loki or Alertmanager data sources can still use them.

## Before you begin
- Write permission to the Mimir or Loki data source is required; users with Editor or Admin roles can edit or delete the rules.
- The Ruler API must be enabled. For Mimir use the `/prometheus` prefix: Grafana expects the Query API and Ruler API under the
  same URL and you cannot give the Ruler API a separate URL. For Loki, the default `local` rule storage supports only viewing;
  configure another rule storage type to edit.
- To stop managing a data source's rules, clear its "Manage alerts via Alerting UI" checkbox.

## Choosing
| | Grafana-managed | Data source-managed |
|---|---|---|
| Data sources | all backend data sources enabling alerting | only Mimir and Loki |
| Mix data sources, expressions | yes | no |
| No data and error states, stale instances, images | yes | no |
| Access control, state history, version history, Terraform | yes | no |
| Recording rules | yes | yes |
| Organisation | folders | namespaces |
| Evaluated and stored | in Grafana (stored in the Grafana database) | in the data source, allowing horizontal scaling |

## Create one
Alerts & IRM -> Alert rules -> New alert rule; name it (the name is also the `alertname` label); select a Prometheus-based
data source; enter a PromQL or LogQL query including the condition; set Rule type to Data source-managed; Preview alerts.
New rules default to Grafana-managed. Then choose a namespace and evaluation group (rules in a group are evaluated
sequentially over the same interval), set a pending period, labels (which select the notification policy; every rule matches the
default policy) and annotations (summary, description, runbook URL), then Save rule.

## Mimir ruler API
Endpoints include `GET <prometheus-http-prefix>/config/v1/rules`, `GET .../config/v1/rules/{namespace}`,
`POST .../config/v1/rules/{namespace}` (set rule group) and `DELETE .../config/v1/rules/{namespace}/{groupName}`.
Authenticated requests need the `X-Scope-OrgID` tenant header unless multi-tenancy is disabled.

## Verify
- [ ] A rule created in the UI can be read back from the ruler's `config/v1/rules` endpoint under its namespace.

## Checked
Checked 2026-11-07. Read in full: the Configure data source-managed alert rules page and the Alert rules fundamentals page. From the Mimir HTTP API page (58k characters)
I read the endpoint table lines for the ruler routes and the X-Scope-OrgID paragraph only. Removed as not on those pages: Cortex and
Thanos Ruler, the `jsonData.manageAlerts` key, the `/loki/api/v1/rules` path, all `mimirtool rules sync|diff|list` commands and
GitOps advice (mimirtool docs were not read), the claim that notifications go through the Mimir Alertmanager, the statement that UI
edits are overwritten by synced rules, and the two Gotchas about recording rule write-back and renaming namespaces. The import tool
for Cloud was not opened.
Method: documentation only; no commands were run.
