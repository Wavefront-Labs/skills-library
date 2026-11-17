---
id: computing-software.cloud-infrastructure-engineering.azure.aks-container-insights-managed-prometheus-and-grafana
name: aks-container-insights-managed-prometheus-and-grafana
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, aks, aks-monitoring, container-insights, managed-prometheus, managed-grafana, azure-monitor-workspace, container-logs]
level: practitioner
status: docs-checked
description: "Monitor AKS with managed Prometheus (Azure Monitor workspace), Managed Grafana dashboards and Container Insights logs, tuning DCR cost and scraping custom targets."
sources: ["https://learn.microsoft.com/azure/azure-monitor/containers/kubernetes-monitoring-enable", "https://learn.microsoft.com/azure/azure-monitor/containers/prometheus-metrics-scrape-configuration", "https://learn.microsoft.com/azure/azure-monitor/containers/prometheus-metrics-scrape-crd", "https://learn.microsoft.com/azure/azure-monitor/containers/prometheus-metrics-scrape-default", "https://learn.microsoft.com/azure/azure-monitor/containers/container-insights-cost", "https://learn.microsoft.com/azure/azure-monitor/containers/kubernetes-metric-alerts", "https://learn.microsoft.com/azure/managed-grafana/overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Container Insights and managed Prometheus/Grafana for AKS

**Goal:** metrics in Prometheus, logs in Log Analytics, dashboards in Grafana — enabled in one
pass and costed deliberately.

## Enable all three
```bash
az aks update -g rg -n aks1 --enable-azure-monitor-metrics \
  --azure-monitor-workspace-resource-id <amw-id> --grafana-resource-id <grafana-id>
az aks enable-addons -g rg -n aks1 -a monitoring --workspace-resource-id <law-id> \
  --data-collection-settings dcr-settings.json
```
Deploys the `ama-metrics` (Prometheus) and `ama-logs` agents and a logs DCR named `MSCI-<region>-<cluster name>`, and links Grafana to the Azure Monitor workspace. Linking an existing Managed Grafana workspace during onboarding needs Owner, or Contributor plus User Access Administrator; viewing data afterwards needs Monitoring Reader or Monitoring Contributor.

## Control log cost (Container Insights)
`dcr-settings.json`:
```json
{ "interval": "1m", "namespaceFilteringMode": "Exclude", "namespaces": ["kube-system","gatekeeper-system"],
  "enableContainerLogV2": true, "streams": ["Microsoft-ContainerLogV2"] }
```
`interval` accepts 1m to 30m; `namespaceFilteringMode` is Off, Include or Exclude. Namespace filtering does not apply to the `ama-logs` agent's own records, and it only filters inventory and performance data.
- Cost presets: *Logs and Events* (the default: ContainerLogV2, KubeEvents, KubePodInventory at 1m, no syslog), *Syslog*, *Standard* (all standard tables), *Cost-optimized* (5m, excludes kube-system, gatekeeper-system and azure-arc).
- Rather than changing a whole table's plan, use DCR transformations to send low-value records to a separate table on a cheaper plan (basic logs).
- ConfigMap `container-azm-ms-agentconfig` controls stdout/stderr collection per namespace, pod and container.

## Scrape custom targets (managed Prometheus)
Use pod and service monitor CRDs (note the API group `azmonitoring.coreos.com/v1`, not `monitoring.coreos.com/v1`), the `ama-metrics-prometheus-config` ConfigMap (recommended for scrape jobs), or opt in to annotation-based scraping with the `pod-annotation-based-scraping` setting (`podannotationnamespaceregex`) in `ama-metrics-settings-configmap`; `prometheus.io/scrape: "true"` is then required on the pod. These ConfigMaps do not exist by default. Example CRD:
```yaml
apiVersion: azmonitoring.coreos.com/v1
kind: PodMonitor
metadata: { name: orders, namespace: orders }
spec:
  selector: { matchLabels: { app: orders } }
  podMetricsEndpoints: [{ port: metrics, interval: 30s }]
```
`ama-metrics-settings-configmap` also toggles the default targets, sets the cluster alias, defines per-target metric keep lists, and controls the **minimal ingestion profile** (enabled by default; limits ingestion to the metrics the default dashboards and alerts use). The ama-metrics pods restart in 2-3 minutes to pick up changes.

## Alerts
Enable the recommended alert rules for the cluster (Prometheus rule groups in the Azure Monitor workspace) as described in the recommended alert rules article.

## Gotchas
- Minimal ingestion drops metrics outside the default list, so custom dashboards can show gaps until you add keep-list entries for those targets or turn the profile off.
- Windows targets (`windows-exporter`, `kube-proxy-windows`) are disabled by default and need Windows metrics collection (preview) enabled.
- Clusters connecting through Azure Monitor private link need the private link scope settings (`useAzureMonitorPrivateLinkScope` in the templates) configured.

## Verify
- [ ] `kubectl get pods -n kube-system | grep ama-` all Running.
- [ ] The built-in Kubernetes dashboards in Grafana show data and a PromQL `up` query for the custom job returns 1.
- [ ] The Container Insights Usage workbook (Workbooks page of the cluster) shows ingestion within budget.

## Checked
Date: 2026-10-24. Checked against MicrosoftDocs/azure-monitor-docs `articles/azure-monitor/containers` (kubernetes-monitoring-enable, kubernetes-data-collection-configure, kubernetes-data-collection-configmap, prometheus-metrics-scrape-configuration, -crd, -default, container-insights-cost, kubernetes-metric-alerts; main branch, repo pushed 2026-10-22).
- Confirmed: `az aks create/update --enable-azure-monitor-metrics --azure-monitor-workspace-resource-id --grafana-resource-id`; `az aks enable-addons --addon monitoring --workspace-resource-id --data-collection-settings`; DCR settings keys and ranges; cost preset contents; CRD API group `azmonitoring.coreos.com/v1`; ConfigMap names and the opt-in annotation scraping; minimal ingestion profile on by default; Windows targets disabled by default; required roles for onboarding and viewing.
- Corrected: pod annotation scraping is available through a ConfigMap setting (not unsupported); Grafana linking roles replace the unconfirmed Monitoring Data Reader claim.
- Removed as unconfirmed: DCE and recording-rule claims, KubeEvents and KubePodInventory stream names, Basic/Auxiliary table-plan advice, double-scrape cost claim, specific alert names, dashboard name and the Usage query.
Method: documentation only; no commands were run.
