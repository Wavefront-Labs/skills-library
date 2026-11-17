---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-metrics-setup
name: tetragon-metrics-setup
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [metrics-setup]
level: practitioner
status: docs-checked
description: "Enable, verify and scrape Tetragon Prometheus metrics, limit label cardinality, and turn on ServiceMonitors in Kubernetes."
sources:
  - "https://tetragon.io/docs/installation/metrics/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enable and scrape Tetragon metrics

Metrics serve two purposes: monitoring Tetragon's own health and monitoring the activity of processes it observes. When the metrics server starts, both health and event metrics are exposed; pass `--enable-event-metrics=false` to disable event metrics but keep health metrics.

## Enable or disable

Kubernetes: metrics are on by default at `/metrics`. The `tetragon` service exposes agent metrics on port `2112`; `tetragon-operator-metrics` exposes operator metrics on `2113`.

```yaml
tetragon:
  prometheus:
    port: 2222 # default is 2112
    enabled: true # default is true
tetragonOperator:
  prometheus:
    port: 3333 # default is 2113
    enabled: true # default is true
```

Set `enabled: false` to turn a metrics server off. Non-Kubernetes: metrics are disabled by default. Set the agent metrics server address, for example `:2112`, with the `--metrics-server` flag; under systemd set the `metrics-address` entry in a file under `/etc/tetragon/tetragon.conf.d/`.

## Verify

```shell
kubectl -n <tetragon-namespace> logs ds/tetragon
kubectl -n <tetragon-namespace> port-forward svc/tetragon 2112:2112
```

The log has a line like `msg="Starting metrics server" addr="localhost:2112"`. Then fetch `localhost:2112/metrics` with a browser or `curl`.

## Limit label cardinality

Event metrics can have very high cardinality, since each pod creates a separate timeseries. Set a comma-separated list of enabled labels with Helm or `--metrics-label-filter`:

```yaml
tetragon:
  prometheus:
    metricsLabelFilter: "namespace,workload,binary" # "pod" label is disabled
```

## ServiceMonitors

Install Kube-Prometheus-Stack with `--set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false`, so Prometheus also picks up Tetragon's ServiceMonitors. Then enable them:

```yaml
tetragon:
  prometheus:
    serviceMonitor:
      enabled: true
tetragonOperator:
  prometheus:
    serviceMonitor:
      enabled: true
```

In the Prometheus UI open Status, Targets and confirm the Tetragon endpoints are `UP`.

## Checked

Date: 2026-11-07

Metrics installation page read in full; every claim matched, no change.

Method: documentation only; no commands were run.
