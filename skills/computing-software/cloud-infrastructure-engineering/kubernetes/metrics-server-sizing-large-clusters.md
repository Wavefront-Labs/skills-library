---
id: computing-software.cloud-infrastructure-engineering.kubernetes.metrics-server-sizing-large-clusters
name: metrics-server-sizing-large-clusters
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, metrics-pipeline, metrics-server-scaling, metrics-server, high-availability, addon-resizer]
level: practitioner
status: docs-checked
description: "Size and run metrics-server for large clusters with per-node resource scaling, HA replicas, scrape tuning and alerts on stale resource metrics."
sources: ["https://github.com/kubernetes-sigs/metrics-server#scaling", "https://github.com/kubernetes-sigs/metrics-server#high-availability", "https://github.com/kubernetes-sigs/metrics-server/tree/master/manifests/components/autoscale", "https://github.com/kubernetes-sigs/metrics-server/blob/master/pkg/scraper/scraper.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sizing metrics-server for large clusters

metrics-server scrapes every kubelet each resolution interval and serves the latest values from
memory. The README lists 1 millicore of CPU and 2 MB of memory per node and support for clusters
up to 5,000 nodes. Since v0.5.0 the default requests (100m CPU, 200Mi) are meant for clusters up to
100 nodes (and up to 70 pods per node and 100 Deployments with HPAs); for more than 100 nodes add
1m CPU and 2MiB memory per node.

## Resources
- Static: set requests from node count, for example 1,000 nodes gives 100m + 900 x 1m = 1 CPU and
  200Mi + 900 x 2Mi, about 2 GiB.
- Dynamic: the repository's `autoscale` kustomize component runs addon-resizer (pod nanny) as a
  sidecar that adjusts the metrics-server requests with node count, using:
  ```
  /pod_nanny --cpu=0m --extra-cpu=1m --memory=0Mi --extra-memory=2Mi --threshold=5 --deployment=metrics-server --container=metrics-server --minClusterSize=100
  ```

## High availability
```yaml
replicas: 2
podDisruptionBudget: {enabled: true, minAvailable: 1}
affinity: {podAntiAffinity: {requiredDuringSchedulingIgnoredDuringExecution: [{labelSelector: {matchLabels: {app.kubernetes.io/name: metrics-server}}, topologyKey: kubernetes.io/hostname}]}}
```
(Helm chart values; the project's HA manifest uses `k8s-app: metrics-server` as the label.) The
README recommends also setting `--enable-aggregator-routing=true` on kube-apiserver so requests
are load balanced between the replicas.

## Scrape tuning
- The shipped manifests set `--metric-resolution=15s`; a longer interval means fewer kubelet
  requests but older data for HPA.
- `--kubelet-preferred-address-types` sets the node address order; the shipped manifests use
  `InternalIP,ExternalIP,Hostname`.
- The shipped deployment and chart use `priorityClassName: system-cluster-critical`.

## Watch it
```promql
histogram_quantile(0.99, sum by (le) (rate(metrics_server_kubelet_request_duration_seconds_bucket[5m])))
rate(metrics_server_kubelet_request_total{success="false"}[5m])
```
plus `container_memory_working_set_bytes` of metrics-server itself near its limit (OOM kills cause
HPA `FailedGetResourceMetric`).

## Verify
`kubectl top nodes` lists every node.

## Checked

Checked 2026-10-24 against the metrics-server README ("Scaling", "High availability"), `manifests/components/autoscale/patch.yaml`, `manifests/components/high-availability/`, base deployment, chart values and `pkg/scraper/scraper.go` on GitHub.
- 1m CPU and 2MiB per node beyond 100 nodes, default 100m and 200Mi since v0.5.0, scalability thresholds (100 nodes, 70 pods per node, 100 Deployments with HPAs), 5,000-node support, 1 millicore and 2 MB per node: README.
- addon-resizer arguments: the autoscale component patch (`--extra-cpu=1m --extra-memory=2Mi --threshold=5 --minClusterSize=100`).
- Metric names `metrics_server_kubelet_request_duration_seconds` (label `node`) and `metrics_server_kubelet_request_total` (label `success`): scraper source.
- `system-cluster-critical`, HA replicas, PDB `minAvailable: 1` and required anti-affinity on `kubernetes.io/hostname`: manifests; chart `podDisruptionBudget.enabled` and `replicas` values.

Method: documentation only; no commands were run.
