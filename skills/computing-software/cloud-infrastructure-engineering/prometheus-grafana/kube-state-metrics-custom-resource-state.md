---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.kube-state-metrics-custom-resource-state
name: kube-state-metrics-custom-resource-state
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [kube-state-metrics, custom-resource-state, kube-state-metrics-crd-metrics, crd, argocd, cert-manager, rbac]
level: advanced
status: docs-checked
description: "Expose metrics from any CRD with kube-state-metrics CustomResourceStateMetrics: config shape, gauge/stateSet/info types, label paths, RBAC, and Helm wiring."
sources: ["https://github.com/kubernetes/kube-state-metrics/blob/main/docs/metrics/extend/customresourcestate-metrics.md", "https://github.com/kubernetes/kube-state-metrics/blob/main/docs/developer/cli-arguments.md", "https://github.com/prometheus-community/helm-charts/blob/main/charts/kube-state-metrics/values.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kube-state-metrics custom resource state

Turns fields of any custom resource into metrics without writing an exporter.

```yaml
# crs-config.yaml
kind: CustomResourceStateMetrics
spec:
  resources:
    - groupVersionKind: {group: cert-manager.io, version: v1, kind: Certificate}
      metricNamePrefix: certmanager
      labelsFromPath:
        name: [metadata, name]
        namespace: [metadata, namespace]
        issuer: [spec, issuerRef, name]
      metrics:
        - name: certificate_ready
          help: "Certificate Ready condition"
          each:
            type: StateSet
            stateSet:
              labelName: status
              path: [status, conditions, "[type=Ready]", status]
              list: ["True", "False", "Unknown"]
        - name: certificate_expiration_timestamp_seconds
          each:
            type: Gauge
            gauge:
              path: [status, notAfter]          # RFC3339 strings are parsed into unix seconds
```
Produces e.g. `certmanager_certificate_ready{status="True",...} 1`: `metricNamePrefix` replaces the default prefix
(the upstream examples show `kube_customresource_<name>` when it is unset; `metricNamePrefix: ""` omits the prefix).
Every series also carries the reserved `customresource_group`, `customresource_version` and `customresource_kind` labels.
The feature is flagged experimental and feature-frozen in favour of resource-state-metrics.

## Wiring
```bash
kube-state-metrics --custom-resource-state-config-file=/etc/ksm/crs-config.yaml \
  --custom-resource-state-only=false
```
`--custom-resource-state-config` takes the YAML inline instead (inline wins if both are given);
`--custom-resource-state-only=true` serves only the custom resource metrics.
Helm (`prometheus-community/kube-state-metrics`): `customResourceState.enabled: true`,
`customResourceState.config: {...}`, and add RBAC (list/watch is also needed on
`customresourcedefinitions.apiextensions.k8s.io`):
```yaml
rbac:
  extraRules:
    - apiGroups: [cert-manager.io]
      resources: [certificates]
      verbs: [list, watch]
```

## Types
- `Gauge` (numbers, booleans, RFC3339 timestamps, quantities such as `250m`; a nil value is mapped to 0 only when
  `nilIsZero` is true, otherwise it errors), `StateSet` (one series per entry in `list`, value 1 for the match),
  `Info` (labels only, value 1). `valueFrom` and `labelsFromPath` per metric for nested arrays; a path that targets an
  array or object yields one series per element.

## Gotchas
- ksm needs list and watch on each configured resource and on CRDs; grant them (Helm: `rbac.extraRules`).
- Select list elements with a `"[key=value]"` path segment. If a path is not found on a resource, an error is logged
  (tune with `errorLogV`); an unresolved StateSet path produces no series and no error.
- Every CR instance x label combination is a series; avoid labels like resourceVersion or timestamps.

## Verify
- [ ] `curl ksm:8080/metrics | grep certmanager_certificate` shows series per CR instance.
- [ ] Alert `certmanager_certificate_ready{status="False"} == 1` fires on a broken cert.

## Checked

2026-11-08. Confirmed against the kube-state-metrics customresourcestate-metrics and cli-arguments docs and the kube-state-metrics Helm chart values: config shape, flags, Gauge/StateSet/Info semantics, path syntax, RBAC, metricNamePrefix naming, error logging, Helm customResourceState and rbac.extraRules keys. Fixed the metric name produced by metricNamePrefix, the RBAC note (CRD list/watch), and the claim that a wrong path is silent. Removed the unconfirmed forbidden log hint.

Method: documentation only; no commands were run.
