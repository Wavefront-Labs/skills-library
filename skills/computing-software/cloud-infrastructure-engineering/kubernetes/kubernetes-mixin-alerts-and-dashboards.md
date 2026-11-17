---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubernetes-mixin-alerts-and-dashboards
name: kubernetes-mixin-alerts-and-dashboards
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubernetes-mixin, mixins, ksm-alerts, kubedeploymentreplicasmismatch, saturation-alerts, cputhrottlinghigh, prometheus, kube-prometheus-stack]
level: practitioner
status: docs-checked
description: "Adopt and tune the kubernetes-mixin alerts and dashboards (kube-prometheus-stack): key workload, saturation and capacity alerts and how to cut noise."
sources: ["https://github.com/kubernetes-sigs/kubernetes-mixin", "https://runbooks.prometheus-operator.dev/", "https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack", "https://raw.githubusercontent.com/prometheus-community/helm-charts/main/charts/kube-prometheus-stack/values.yaml", "https://raw.githubusercontent.com/kubernetes-monitoring/kubernetes-mixin/master/alerts/apps_alerts.libsonnet", "https://raw.githubusercontent.com/kubernetes-monitoring/kubernetes-mixin/master/alerts/resource_alerts.libsonnet", "https://raw.githubusercontent.com/kubernetes-monitoring/kubernetes-mixin/master/alerts/storage_alerts.libsonnet"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kubernetes-mixin alerts and dashboards

The mixin (jsonnet) is the community set of recording rules, alerts and Grafana dashboards.
kube-prometheus-stack ships rules and dashboards that originate from upstream projects; runbooks live at
`runbooks.prometheus-operator.dev/runbooks/kubernetes/<lowercase alertname>` (for example `kubepodcrashlooping`).
The `for` durations and severities below are the mixin defaults in the alert files; the chart's values can
override them.

## Key alerts and what to do
| Alert | Fires when | First check |
|---|---|---|
| `KubePodCrashLooping` | pod crash looping, 15m | `kubectl logs --previous` |
| `KubePodNotReady` | pod not ready 15m | describe pod, probes, scheduling |
| `KubeDeploymentReplicasMismatch` | spec replicas ≠ available 15m | quota, FailedCreate on RS, Pending pods |
| `KubeDeploymentRolloutStuck` | Progressing condition false 15m | `kubectl rollout status`, bad image/probes |
| `KubeStatefulSetReplicasMismatch` / `KubeDaemonSetRolloutStuck` | same for STS/DS | ordinal blocked, taints |
| `KubeJobFailed` / `KubeJobNotCompleted` | job failed / running too long | job pod logs |
| `KubeHpaMaxedOut` | HPA at maxReplicas 15m | capacity, raise max |
| `CPUThrottlingHigh` | more than `cpuThrottlingPercent` (25) of CFS periods throttled, 15m, severity info | CPU limits too low |
| `KubeCPUOvercommit` / `KubeMemoryOvercommit` | pod requests too high for the cluster to tolerate a node failure, 10m | add capacity or cut requests |
| `KubeQuotaAlmostFull` (info) / `KubeQuotaExceeded` (warning) | namespace quota, 15m | quota troubleshooting |
| `KubePersistentVolumeFillingUp` | critical: under 3% free; warning: under 15% free and predicted to fill within 4 days | expand PVC |
| `KubeNodeNotReady` / `KubeletTooManyPods` | node not ready 15m / pod count near capacity | node triage |
| `KubeClientCertificateExpiration` | apiserver client certificates near expiry | cert rotation |

Node filesystem alerts such as `NodeFilesystemAlmostOutOfSpace` come from node-exporter's rules, not this mixin.

## Tuning without forking
In kube-prometheus-stack values:
```yaml
defaultRules:
  disabled: {CPUThrottlingHigh: true}          # disable individual alerts
  additionalRuleLabels: {team: platform}
customRules:
  KubePodCrashLooping: {for: 30m, severity: critical}   # overrides `for` and `severity` per alert
```
Route by namespace/team label in Alertmanager; send `severity=info` to a ticket queue, not
pagers. Use **inhibit_rules** (for example a critical alert suppressing warnings with the same labels).
For deep customisation, vendor the mixin with jsonnet-bundler and set `_config` (selectors,
thresholds), then render with `jsonnet -J vendor` as in the mixin README.

## Dashboards
The mixin defines dashboards titled "Compute Resources / Namespace (Pods)", "Compute Resources / Workload",
"Compute Resources / Node (Pods)" and "Persistent Volumes" (among others), with a configurable
`dashboardNamePrefix`. They rely on the mixin's recording rules (for example
`namespace_cpu:kube_pod_container_resource_requests:sum`), so do not delete the rules.

## Verify
- [ ] `amtool alert` during a test crashloop shows `KubePodCrashLooping`, and it reaches the owning team's receiver.
- [ ] No alert stays firing for weeks without an owner (noise review).

## Checked
2026-10-28. Confirmed against the kubernetes-mixin alert sources (`apps_alerts`, `resource_alerts`,
`storage_alerts`, `kubelet`, `kube_apiserver`): alert names, `for` durations (15m for pod, deployment,
HPA, job and node alerts; 10m for overcommit), severities (info for `CPUThrottlingHigh` and
`KubeQuotaAlmostFull`), `cpuThrottlingPercent: 25`, the PV 3% / 15% / 4-day thresholds, the "cannot tolerate
node failure" overcommit text, dashboard titles and `dashboardNamePrefix`, the README `jsonnet -J vendor`
steps; `defaultRules.disabled`, `additionalRuleLabels`, `customRules` and the runbook base URL against the
kube-prometheus-stack `values.yaml`; the runbook URL pattern against the runbooks site; `amtool alert` and
`inhibit_rules` against the Alertmanager README and configuration page. Removed: `NodeFilesystemAlmostOutOfSpace`
(node-exporter's rules, not this mixin), the `node_namespace_pod_container:*` recording-rule name and the
"pre-rendered" wording (not on the pages read), `amtool alert query`, and the 7-day figure.
Method: documentation only; no commands were run.
