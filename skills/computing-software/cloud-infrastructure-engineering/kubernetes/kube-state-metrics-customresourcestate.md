---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kube-state-metrics-customresourcestate
name: kube-state-metrics-customresourcestate
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, customresourcestate, custom-resource-metrics, kube-state-metrics, crd, prometheus, observability]
level: advanced
status: docs-checked
description: "Expose CRD status as Prometheus metrics with kube-state-metrics CustomResourceState config: Gauge, StateSet and Info metrics, labelsFromPath, RBAC, and cardinality limits."
sources: ["https://github.com/kubernetes/kube-state-metrics/blob/main/docs/metrics/extend/customresourcestate-metrics.md", "https://github.com/kubernetes/kube-state-metrics/blob/main/docs/developer/cli-arguments.md", "https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-state-metrics"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kube-state-metrics CustomResourceState

## Status
The project notes that `custom-resource-state` is feature-frozen in favour of
`kubernetes-sigs/resource-state-metrics` and will be deprecated once that is stable; the related flags are
marked experimental. Use it for existing setups, and check the replacement for new ones.

## Why
Operators often expose no per-object metrics. KSM can read any CR and turn fields into
metrics: "Certificate not ready", "Flux Kustomization failing", "CNPG cluster replicas".

## Config
```yaml
kind: CustomResourceStateMetrics
spec:
  resources:
  - groupVersionKind: {group: cert-manager.io, version: v1, kind: Certificate}
    metricNamePrefix: certmanager
    labelsFromPath:
      name: [metadata, name]
      namespace: [metadata, namespace]
    metrics:
    - name: certificate_ready
      help: "Ready condition of the certificate"
      each:
        type: Gauge
        gauge:
          path: [status, conditions]
          labelsFromPath: {type: [type]}
          valueFrom: [status]           # "True" -> 1; "false", "no", "unknown" -> 0 (case-insensitive)
    - name: certificate_not_after
      each:
        type: Gauge
        gauge:
          path: [status, notAfter]      # RFC3339 timestamps become unix timestamps
    - name: certificate_info
      each:
        type: Info
        info:
          labelsFromPath: {issuer: [spec, issuerRef, name]}
```
`StateSet` emits one series per value in `list` with 1 on the one that matches; use it for phase fields:
```yaml
      each:
        type: StateSet
        stateSet:
          labelName: phase
          path: [status, phase]
          list: [Pending, Bound, Failed]
```
If the path does not resolve yet, no series is produced and no error is logged.

## Wiring (Helm chart)
```yaml
customResourceState:
  enabled: true
  config: {}            # the spec above, or point at a ConfigMap
rbac:
  extraRules:
  - apiGroups: [cert-manager.io]
    resources: [certificates]
    verbs: [list, watch]
```
CLI flags behind it: `--custom-resource-state-config` (inline YAML) or `--custom-resource-state-config-file`, and
`--custom-resource-state-only=true` to run an instance that serves only the configured custom resources.
kube-state-metrics needs `list` and `watch` on `customresourcedefinitions.apiextensions.k8s.io` as well as on
the resources you configure. The chart's `customResourceState.config` is written to a ConfigMap
(`customResourceState.create`, default key `config.yaml`).

## Resulting series
```
certmanager_certificate_ready{name="api-tls",namespace="shop",type="Ready",customresource_group="cert-manager.io",customresource_kind="Certificate",customresource_version="v1"} 1
```
`metricNamePrefix` replaces the default prefix. Without it the examples in the project docs produce names
such as `kube_customresource_uptime`. The labels `customresource_group`, `customresource_version` and
`customresource_kind` are added automatically and are reserved.

## Alert example
```yaml
- alert: CertificateNotReady
  expr: certmanager_certificate_ready{type="Ready"} == 0
  for: 15m
```

## Gotchas
- Every `labelsFromPath` entry multiplies cardinality; never use UIDs, timestamps or
  free-text messages as labels.
- The flags are marked experimental and the feature is frozen; test the config after every KSM upgrade.
- CRD version must be served; when the operator drops `v1beta1`, update the GVK.

## Verify
```bash
kubectl port-forward -n monitoring svc/kube-state-metrics 8080 &
curl -s localhost:8080/metrics | grep certmanager_
```

## Checked

2026-10-26: kube-state-metrics docs (kubernetes/kube-state-metrics main, latest release v2.20.0, repo updated 2026-10-19) and the prometheus-community kube-state-metrics Helm chart 8.7.1 values. Confirmed: feature-freeze notice, flags and their experimental label, value conversion rules (true/yes to 1, RFC3339 to timestamp), StateSet fields, metricNamePrefix naming, reserved customresource_* labels, CRD list/watch RBAC, chart keys customResourceState.enabled/config and rbac.extraRules. Corrected: the old skill showed the series as kube_customresource_certmanager_certificate_ready, but a metricNamePrefix replaces the default prefix, so it is certmanager_certificate_ready.

Method: documentation only; no commands were run.
