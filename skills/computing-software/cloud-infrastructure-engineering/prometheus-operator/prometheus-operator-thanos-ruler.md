---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-thanos-ruler
name: prometheus-operator-thanos-ruler
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [thanos-ruler, queryendpoints, queryconfig, alertmanagersconfig, dnssrv]
level: advanced
status: docs-checked
description: "Deploy a ThanosRuler that evaluates PrometheusRule objects against Thanos query endpoints and sends alerts to Alertmanager."
sources: ["https://prometheus-operator.dev/docs/platform/thanos/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A `ThanosRuler` evaluates recording and alerting rules against a chosen Query API, so rules can span many Prometheus instances or shards.

## Requirements
At least one query API server, defined by `.spec.queryEndpoints` (a list, for example `dnssrv+_http._tcp.my-thanos-querier.monitoring.svc.cluster.local`) or by `.spec.queryConfig`. Alert delivery uses `.spec.alertmanagersConfig`, a reference to a Secret key.

## Example
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ThanosRuler
metadata:
  name: thanos-ruler-demo
  namespace: monitoring
spec:
  image: quay.io/thanos/thanos:v0.28.1
  ruleSelector:
    matchLabels:
      role: my-thanos-rules
  queryEndpoints:
    - dnssrv+_http._tcp.my-thanos-querier.monitoring.svc.cluster.local
  alertmanagersConfig:
    key: alertmanager-configs.yaml
    name: thanosruler-alertmanager-config
```
The Secret holds Thanos-format Alertmanager configuration, for instance `alertmanagers: [{static_configs: ["dnssrv+_web._tcp.alertmanager-operated.monitoring.svc.cluster.local"], api_version: v2}]`, created with `kubectl create secret generic ... --from-file=alertmanager-configs.yaml=...`.

The image tag is the docs example; use a current Thanos release.

## Rules
It consumes the same `PrometheusRule` objects as Prometheus. Any rule whose labels match `ruleSelector` (`role=my-thanos-rules` here) is loaded into the Thanos Ruler pods.

## Checked

2026-11-08. Read the Thanos page in full. Noted the image tag is the docs example; other claims match.

Method: documentation only; no commands were run.
