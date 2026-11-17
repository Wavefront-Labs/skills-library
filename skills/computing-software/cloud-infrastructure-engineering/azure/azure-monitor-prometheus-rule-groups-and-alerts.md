---
id: computing-software.cloud-infrastructure-engineering.azure.azure-monitor-prometheus-rule-groups-and-alerts
name: azure-monitor-prometheus-rule-groups-and-alerts
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-monitor, prometheus-alerts, prometheus-rule-groups, managed-prometheus, azure-monitor-workspace, promql, recording-rules, alert-rules, aks, kube-prometheus-rules, action-groups]
level: practitioner
status: docs-checked
description: "Create Azure Monitor managed Prometheus rule groups: PromQL alert and recording rules scoped to an Azure Monitor workspace and AKS cluster, wired to action groups."
sources: ["https://learn.microsoft.com/azure/azure-monitor/metrics/prometheus-rule-groups", "https://learn.microsoft.com/azure/azure-monitor/alerts/prometheus-alerts", "https://learn.microsoft.com/azure/azure-monitor/containers/kubernetes-metric-alerts", "https://learn.microsoft.com/azure/azure-monitor/containers/prometheus-metrics-scrape-default"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prometheus rule groups in Azure Monitor

**Goal:** PromQL alerts and recording rules evaluated by Azure against managed Prometheus
data, using Azure action groups — no self-hosted Alertmanager or Prometheus server.

## 1. Model
- Data lives in an **Azure Monitor workspace** (AMW), populated by the AKS metrics add-on
  (`az aks update --enable-azure-monitor-metrics --azure-monitor-workspace-resource-id <amw-id>`).
- A **rule group** (`Microsoft.AlertsManagement/prometheusRuleGroups`) is an Azure resource scoped to an AMW (the AMW cannot be changed afterwards), optionally limited to one cluster (exact cluster name) or to clusters whose name contains given text, with an evaluation interval (default 1 minute) and a list of rules, each an `alert` or a `record`. You cannot apply individual rules to a cluster.
- Fired Prometheus alerts appear in Azure Monitor *Alerts* (filter Monitor service = Prometheus) with a severity and call **action groups**; rule labels and annotations are added to the alerts.

## 2. Create
```bash
az alerts-management prometheus-rule-group create -n rg-aks-prod-alerts -g rg-mon -l uksouth \
  --scopes <amw-id> --interval PT1M --enabled \
  --rules '[
    {"record":"namespace:container_cpu_usage:sum","expression":"sum by (namespace) (rate(container_cpu_usage_seconds_total{container!=\"\"}[5m]))"},
    {"alert":"KubePodCrashLooping","expression":"max_over_time(kube_pod_container_status_waiting_reason{reason=\"CrashLoopBackOff\"}[5m]) >= 1",
     "for":"PT15M","severity":3,"labels":{"team":"platform"},"annotations":{"description":"{{ $labels.namespace }}/{{ $labels.pod }} crash looping"},
     "actions":[{"actionGroupId":"<ag-id>"}],"resolveConfiguration":{"autoResolved":true,"timeToResolve":"PT10M"}}
  ]'
```
- Bicep/ARM (API version `2023-03-01`) is the normal home: one rule group per concern (node, pod, app SLOs). To limit a group to one cluster in a template, put the cluster's resource ID in `scopes` next to the AMW and set `clusterName` (the value of the `cluster` label).
- **Recommended alerts**: the cluster's *Alerts* menu → *Set up recommendations* offers the Prometheus community rules organised by pod, cluster and node level, plus platform alerts; start there and tune. Create the rule group in the same region as the cluster.

## 3. Writing rules that behave
- `for` is an ISO-8601 duration (`PT5M`), not `5m`; it is the time between the expression first becoming true and the alert firing.
- Recording rules precompute values into new metrics (the rule name is the metric name); record once, alert on the recorded series.
- Use `severity` consistently with your other Azure alerts so routing works.
- Test the expression against the AMW (for example in Managed Grafana) before deploying; an empty result never fires.

## Gotchas
- The default cluster name is the cluster's `cluster` label value; change it only if you changed the label with `cluster_alias`.
- Metrics outside the default minimal scrape profile need `ama-metrics-settings-configmap` changes before rules can use them.
- Enable the recommended alerts for the Azure Monitor workspace too, to watch ingestion limits and quotas.

## Verify
- [ ] `az alerts-management prometheus-rule-group show -n rg-aks-prod-alerts -g rg-mon` shows the group enabled.
- [ ] A deliberately crash-looping test pod raises `KubePodCrashLooping` in *Alerts* and the action group notifies.
- [ ] The recorded series `namespace:container_cpu_usage:sum` is queryable against the AMW.

## Checked
Date: 2026-10-24. Checked against MicrosoftDocs/azure-monitor-docs (metrics/prometheus-rule-groups, alerts/prometheus-alerts, containers/kubernetes-metric-alerts; main branch, repo pushed 2026-10-22).
- Confirmed: `az alerts-management prometheus-rule-group create` with `--scopes`, `--interval`, `--enabled` and the `--rules` JSON shape (record, alert, expression, severity, for, labels, annotations, resolveConfiguration, actions); 1-minute default interval; scope options (workspace, specific cluster, cluster name text); ARM API version 2023-03-01 with `clusterName`; recommended alerts through *Set up recommendations* grouped by pod, cluster and node; same-region recommendation; AMW immutable once created.
- Removed as unconfirmed: the `az-prom-rules-converter` tool, `--cluster-name` on the CLI command, the severity 0-4 range, the same-region-as-AMW rule, time-to-fire estimates, and the CrashLoopBackOff and CPU rule expressions are shown only as illustrative PromQL.
Method: documentation only; no commands were run.
