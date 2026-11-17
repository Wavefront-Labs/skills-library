---
id: computing-software.cloud-infrastructure-engineering.kubernetes.grafana-dashboards-as-code-provisioning
name: grafana-dashboards-as-code-provisioning
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, dashboard-provisioning, grafana-operator, dashboard-configmap, grafana, gitops, observability]
level: practitioner
status: docs-checked
description: "Ship Grafana dashboards from Git on Kubernetes: sidecar-loaded ConfigMaps, Grafana Operator GrafanaDashboard CRs, datasource mapping, ConfigMap size limit, and UI edits."
sources: ["https://github.com/grafana-community/helm-charts/blob/main/charts/grafana/values.yaml", "https://github.com/grafana/grafana-operator/blob/master/docs/docs/api.md", "https://grafana.com/docs/grafana/latest/administration/provisioning/#dashboards"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grafana dashboards as code

## Option A: ConfigMap + sidecar
The Grafana Helm chart's dashboards sidecar (image `kiwigrid/k8s-sidecar`) watches ConfigMaps (and Secrets, by default both) with a label and writes them into the
provisioning folder. The chart has moved to the grafana-community/helm-charts repository.
```yaml
# values
grafana:
  sidecar:
    dashboards:
      enabled: true
      label: grafana_dashboard
      labelValue: "1"
      searchNamespace: ALL
      folderAnnotation: grafana_folder
      provider: {foldersFromFilesStructure: true, allowUiUpdates: false}
```
Create a ConfigMap holding the dashboard JSON, give it the label `grafana_dashboard` (matching the
value in the values above) and, for folders, the annotation `grafana_folder: Payments`. Commit the
YAML; GitOps applies it. The chart defaults are `label: grafana_dashboard`, an empty `labelValue`,
`allowUiUpdates: false` and `foldersFromFilesStructure: false`.

## Option B: Grafana Operator
```yaml
apiVersion: grafana.integreatly.org/v1beta1
kind: GrafanaDashboard
metadata: {name: api, namespace: monitoring}
spec:
  instanceSelector: {matchLabels: {dashboards: grafana}}
  folder: Payments
  resyncPeriod: 10m
  configMapRef: {name: api-dashboard-json, key: api.json}   # or json:, url:, grafanaCom: {id: 15760}
  datasources:
  - {inputName: DS_PROMETHEUS, datasourceName: Prometheus}
```
The operator also has CRs for datasources, folders and alert rule groups, and a Grafana CR can
point at an external Grafana instance that it does not manage (`spec.external`). Dashboard
content can also come from `gzipJson`, `jsonnet`, `jsonnetLib` or an `oci` artifact; the default
`resyncPeriod` is 10m0s, and `allowCrossNamespaceImport` defaults to false.

## Making dashboards portable
- For the operator, `datasources` maps each templated datasource input name (`inputName`) in the
  dashboard JSON to an existing datasource (`datasourceName`).
- Set a fixed `uid` (the operator's `spec.uid` is immutable and overrides any uid in the JSON, up
  to 40 characters of alphanumerics, `-` and `_`). Grafana's provisioning guide warns against
  reusing the same `uid` or the same `title` within a folder in one instance.

## Gotchas
- **Size**: a ConfigMap cannot exceed 1 MiB.
- **UI edits**: with `allowUiUpdates: false` you cannot save changes to a provisioned dashboard.
  Workflow: edit in a dev Grafana, export JSON, PR it.
- Duplicate `uid` values in one Grafana instance cause inconsistent behaviour.

## Verify
```bash
kubectl get grafanadashboards -A     # operator: inspect each resource's status
```
For the sidecar, check the logs of the sidecar container in the Grafana pod.
Dashboard appears in the right folder, and editing the source in Git updates it within one sync.

## Checked

Checked 2026-11-09 against the Grafana provisioning page (dashboard providers, allowUiUpdates, foldersFromFilesStructure, uid and title warning), the Grafana Helm chart values file (sidecar.dashboards settings and defaults), the Grafana Operator CRD reference (GrafanaDashboard spec, datasources, grafanaCom, resyncPeriod, uid, Grafana spec.external) and the Kubernetes ConfigMap page (1 MiB limit). Removed: the kube-prometheus-stack default claim, the kubectl label/annotate pipeline, the 256 KiB client-side apply claim, Export for sharing externally, Grafonnet, the sidecar container name and the silent uid winner claim; none were found in those pages. The Operator dashboards docs URL in sources returned 404 and was replaced by the CRD reference.

Method: docs-checked 2026-11-09 against the pages listed above; no commands were run.
