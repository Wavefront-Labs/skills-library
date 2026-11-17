---
id: computing-software.ai-ml-engineering.seldon-core-2.hpa-prometheus-adapter-setup
name: hpa-prometheus-adapter-setup
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, hpa, prometheus-adapter, custom-metrics, infer-rps, seldon-model-infer-total, metrics-relist-interval]
level: advanced
status: docs-checked
description: "Expose Seldon Core 2 request rate to Kubernetes HPA: install prometheus-adapter, replace its ConfigMap rule producing infer_rps, and test it through the custom metrics API."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/scaling/hpa-setup.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Exposing metrics for HPA with prometheus-adapter

Requirements: Core 2 publishing metrics to Prometheus (default, assumed here in namespace `seldon-monitoring`), Prometheus Adapter, and HPA manifests. A cluster supports only one active custom metrics provider.

## Install
```sh
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install --set prometheus.url=http://seldon-monitoring-prometheus hpa-metrics prometheus-community/prometheus-adapter -n seldon-monitoring
```
Set `prometheus.port` if it is not 9090. Make `metricsRelistInterval` (default 1m) larger than or equal to your Prometheus scrape interval.

## Configure
Overwrite the ConfigMap `hpa-metrics-prometheus-adapter` (name follows the helm release) with a rule:
- `seriesQuery`: `{__name__="seldon_model_infer_total",namespace!=""}`
- `resources.overrides`: map labels `model` and `server` to groups of `mlops.seldon.io`, plus `pod` and `namespace`.
- `name`: match `seldon_model_infer_total`, expose as `infer_rps`.
- `metricsQuery`: sum by GroupBy of the rate of Series with LabelMatchers over a window of `[2m]`.

The rule has four parts: discovery, association, naming, querying. Keep the rate window at least twice the scrape interval or the query may return nothing. Then apply and restart:

```sh
kubectl replace -f prometheus-adapter.config.yaml
kubectl rollout restart deployment hpa-metrics-prometheus-adapter -n seldon-monitoring
```

## Test
Send requests to a model first, then:
```sh
kubectl get --raw /apis/custom.metrics.k8s.io/v1beta1/namespaces/seldon-mesh/models.mlops.seldon.io/irisa0/infer_rps
```
Servers use `servers.mlops.seldon.io/mlserver` and pods use `pods/mlserver-0`.

## Checked

2026-11-04. Confirmed against scaling/hpa-setup.md (Seldon Core 2 docs, v2 branch): adapter install, ConfigMap rule, 2m window and twice-scrape guidance, restart, custom metrics API tests. Removed or corrected: nothing.

Method: documentation only; no commands were run.
