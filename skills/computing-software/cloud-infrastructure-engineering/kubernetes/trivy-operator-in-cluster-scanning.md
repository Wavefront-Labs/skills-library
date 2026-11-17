---
id: computing-software.cloud-infrastructure-engineering.kubernetes.trivy-operator-in-cluster-scanning
name: trivy-operator-in-cluster-scanning
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, image-security, trivy-operator, vulnerabilityreport, configauditreport, in-cluster-scanning, cks]
level: practitioner
status: docs-checked
description: "Continuously scan running workloads with Trivy Operator: VulnerabilityReports, ConfigAudit, exposed secrets and RBAC reports as CRDs, plus tuning, air-gapped DBs and alerting."
sources: ["https://aquasecurity.github.io/trivy-operator/latest/", "https://aquasecurity.github.io/trivy-operator/latest/getting-started/installation/helm/", "https://aquasecurity.github.io/trivy-operator/latest/tutorials/grafana-dashboard/", "https://aquasecurity.github.io/trivy-operator/latest/docs/vulnerability-scanning/private-registries/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Trivy Operator: in-cluster scanning

CI scanning misses images already running when a new CVE is published. Trivy Operator watches
workloads and rescans images, writing results as namespaced CRDs next to the workload.

## Install
```bash
helm repo add aqua https://aquasecurity.github.io/helm-charts/
helm install trivy-operator aqua/trivy-operator -n trivy-system --create-namespace \
  --set trivy.ignoreUnfixed=true \
  --set operator.scanJobsConcurrentLimit=5 \
  --set trivy.mode=ClientServer --set trivy.serverURL=http://trivy-server.trivy-system:4975 \
  --set serviceMonitor.enabled=true
```
The chart default is `trivy.mode: Standalone`; `ClientServer` mode needs `trivy.serverURL` (the chart can also run
a built-in Trivy server with `operator.builtInTrivyServer`). Air-gapped: mirror the Trivy DB and Java DB
artifacts to your registry and set `trivy.dbRegistry`/`dbRepository` and `javaDbRegistry`/`javaDbRepository`
(chart defaults `mirror.gcr.io` with `aquasec/trivy-db` and `aquasec/trivy-java-db`).

## Reports
```bash
kubectl get vulnerabilityreports -A -o wide        # CRITICAL/HIGH/MEDIUM/LOW counts per container image
kubectl get configauditreports -A -o wide          # misconfigurations (privileged, no limits...)
kubectl get exposedsecretreports -A
kubectl get rbacassessmentreports -A; kubectl get clusterrbacassessmentreports
```
Reports follow the workload lifecycle, and are deleted after `operator.scannerReportTTL` (env
`OPERATOR_SCANNER_REPORT_TTL`; chart default `24h`, empty disables it) so the operator rescans.

## Alerting and dashboards
The operator exposes metrics such as `trivy_image_vulnerabilities`, `trivy_resource_configaudits` and
`trivy_image_exposedsecrets` (used in the Grafana dashboard tutorial); enable the ServiceMonitor with
`serviceMonitor.enabled` in the chart. Check the exact label names on your metrics endpoint before writing alerts.
```promql
sum(trivy_image_vulnerabilities)
```

## Tuning
- Limit scope with `targetNamespaces` / `excludeNamespaces` (chart values).
- Scan Jobs pull images using the workload's image pull secrets, including those referenced through its
  service account; the operator creates a temporary secret per scan job.
- Large clusters: tune `operator.scanJobsConcurrentLimit` (default 10) and `operator.scanJobTimeout` (default 5m).

## Verify
- [ ] Every running workload has a VulnerabilityReport younger than the TTL; critical-CVE alert fires for a known-vulnerable test image.

## Checked

Checked on 2026-10-26 against `aquasecurity/trivy-operator` main (chart `deploy/helm/values.yaml`, docs `getting-started/installation/helm.md`, `docs/vulnerability-scanning/private-registries.md`, `docs/design/ttl_scans.md`, `docs/tutorials/grafana-dashboard.md`; latest release v0.35.0, pushed 2026-10-25).
Confirmed: Helm repo `https://aquasecurity.github.io/helm-charts/`; values `trivy.mode` (default `Standalone`), `trivy.serverURL`, `trivy.ignoreUnfixed` (default false), `operator.scanJobsConcurrentLimit` (10), `scanJobTimeout` (5m), `scannerReportTTL` (24h), DB registry and repository defaults, `targetNamespaces`, `excludeNamespaces`; image pull secret handling; metric names `trivy_image_vulnerabilities`, `trivy_resource_configaudits`, `trivy_image_exposedsecrets`.
Wrong in the draft: server port is 4975 in the chart docs (not 4954); the TTL env var is `OPERATOR_SCANNER_REPORT_TTL`; the DB artifacts default to `mirror.gcr.io/aquasec/...`. Removed as unconfirmed: the metric label names in the PromQL, the "much less bandwidth" claim and the node credential provider remark.

Method: documentation only; no commands were run.
