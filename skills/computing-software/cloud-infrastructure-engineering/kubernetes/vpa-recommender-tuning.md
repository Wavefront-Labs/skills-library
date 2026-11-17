---
id: computing-software.cloud-infrastructure-engineering.kubernetes.vpa-recommender-tuning
name: vpa-recommender-tuning
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, vpa, vpa-recommender-tuning, vpa-recommender, prometheus, rightsizing]
level: practitioner
status: docs-checked
description: "Tune the VPA recommender's percentiles, histogram decay, margins and minimums, and seed it from Prometheus history so recommendations are sane from day one."
sources: ["https://github.com/kubernetes/autoscaler/blob/master/vertical-pod-autoscaler/docs/flags.md", "https://github.com/kubernetes/autoscaler/blob/master/vertical-pod-autoscaler/docs/examples.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VPA recommender tuning

## Key flags
| Flag | Default | Effect |
|---|---|---|
| `--target-cpu-percentile` | 0.9 | CPU target from the usage histogram |
| `--target-memory-percentile` | 0.9 | memory usage percentile used as the base for the memory target |
| `--recommendation-margin-fraction` | 0.15 | safety margin added |
| `--cpu-histogram-decay-half-life` | 24h | how fast old CPU samples lose weight |
| `--memory-histogram-decay-half-life` | 24h | same for memory |
| `--pod-recommendation-min-cpu-millicores` | 25 | floor |
| `--pod-recommendation-min-memory-mb` | 250 | floor |
| `--oom-bump-up-ratio` | 1.2 | memory bump ratio after an OOM kill (see also `--oom-min-bump-up-bytes`, default 100Mi) |
| `--recommender-interval` | 1m | how often metrics are fetched |

Raise the decay half-life for weekly cycles; raise the memory percentile for memory-sensitive
JVMs; lower minimums for many tiny sidecars.

## Seed from Prometheus history
```
--storage=prometheus
--prometheus-address=http://prometheus-operated.monitoring:9090
--history-length=8d
--history-resolution=1h
--prometheus-cadvisor-job-name=kubelet
--metric-for-pod-labels=kube_pod_labels{job="kube-state-metrics"}[8d]
```
The default storage mode is `checkpoint`; Prometheus defaults for `--prometheus-address`
(`http://prometheus.monitoring.svc`), `--prometheus-cadvisor-job-name` (`kubernetes-cadvisor`),
`--history-length` (8d) and `--history-resolution` (1h) are in flags.md.

## Several recommenders
Run a second recommender with `--recommender-name=batch` and different percentiles, and select it
per VPA (never run two recommenders with the same name in a cluster):
```yaml
spec:
  recommenders: [{name: batch}]
```

## Per-VPA bounds
`resourcePolicy.containerPolicies[].minAllowed/maxAllowed` and `controlledValues:
RequestsOnly` keep recommendations inside what nodes can host.

## Verify
`kubectl describe vpa <name>` shows target, lowerBound and upperBound; compare the target with
the usage percentile you configured over the same window.

## Checked

Checked 2026-10-24 against flags.md in kubernetes/autoscaler vertical-pod-autoscaler (master, VPA 1.8.1).
- Defaults confirmed in the recommender flag table: `target-cpu-percentile` 0.9, `target-memory-percentile` 0.9, `recommendation-margin-fraction` 0.15, both decay half-lives 24h, `pod-recommendation-min-cpu-millicores` 25, `pod-recommendation-min-memory-mb` 250, `oom-bump-up-ratio` 1.2, `oom-min-bump-up-bytes` 100Mi, `recommender-interval` 1m, `storage` (prometheus or checkpoint), `history-length` 8d, `history-resolution` 1h, `recommender-name`.
- `spec.recommenders[].name` selection per VPA and the "same name" warning: flags.md and api.md.

Method: documentation only; no commands were run.
