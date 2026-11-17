---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kube-state-metrics-install-and-rbac
name: kube-state-metrics-install-and-rbac
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kube-state-metrics, ksm-install, prometheus, rbac, servicemonitor]
level: practitioner
status: docs-checked
description: "Install kube-state-metrics with Helm or manifests, give it the RBAC it needs, scope resources and namespaces, shard it and scrape it with honorLabels."
sources: ["https://github.com/kubernetes/kube-state-metrics/blob/main/README.md", "https://github.com/kubernetes/kube-state-metrics/blob/main/docs/developer/cli-arguments.md", "https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-state-metrics", "https://prometheus.io/docs/prometheus/latest/configuration/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Installing kube-state-metrics

kube-state-metrics (KSM) watches the API and exposes object state (replicas, phases, conditions,
requests) as metrics. It is separate from metrics-server, which provides usage.

## Helm
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install ksm prometheus-community/kube-state-metrics -n monitoring --create-namespace \
  --set prometheus.monitor.enabled=true \
  --set prometheus.monitor.http.honorLabels=true
```

## Manifests
```bash
git clone https://github.com/kubernetes/kube-state-metrics && cd kube-state-metrics
git checkout <release tag>
kubectl apply -f examples/standard
```
The README documents applying `examples/standard`. Use the latest release unless the README's compatibility matrix says
otherwise (v2.20.0 is listed for Kubernetes 1.36). Adjust apiVersions of some resources if your cluster is old.
Image: `registry.k8s.io/kube-state-metrics/kube-state-metrics:<tag>`.

## RBAC
The ClusterRole needs `list` and `watch` on every resource it exports (the default `--resources` list includes
certificatesigningrequests, configmaps, cronjobs, daemonsets, deployments and more). To restrict access, give the
service account only what it needs and narrow KSM to match:
```
--resources=pods,deployments,nodes,persistentvolumeclaims
--namespaces=shop,payments          # RoleBindings per namespace instead of a ClusterRoleBinding
```

## Ports
`--port` 8080 (object metrics) and `--telemetry-port` 8081 (KSM's own metrics, including list and watch success and
error counts). Scrape with `honorLabels: true`: with `honor_labels` false, Prometheus renames conflicting scraped labels
to `exported_<label>`.

## Large clusters
Shard horizontally: `--shard=N` (zero indexed) with `--total-shards=M` per instance, or run a StatefulSet and pass
`--pod` and `--pod-namespace` (from the downward API) for automated sharding. Objects are assigned by an md5 sum of the
object UID modulo the shard count; every instance still receives and unmarshals all objects, so sharding spreads
metric generation, not API load. StatefulSet rollouts replace one pod at a time and cause short gaps per shard.
The Helm chart exposes this as `autosharding.enabled` (marked experimental there).

## Verify
```bash
kubectl -n monitoring port-forward svc/ksm-kube-state-metrics 8080 &
curl -s localhost:8080/metrics | grep -c '^kube_pod_info'
```
equals the number of pods you expect (after any sharding change, confirm every shard is scraped).

## Checked

2026-10-26: kube-state-metrics README and cli-arguments (kubernetes/kube-state-metrics main, latest release v2.20.0, repo updated 2026-10-19), the prometheus-community Helm chart 8.7.1 values, and the Prometheus configuration reference (honor_labels). Confirmed: examples/standard install, compatibility matrix entry, ports and flags, sharding flags and algorithm, automated sharding via --pod and --pod-namespace, namespace and resource restriction, chart key prometheus.monitor.http.honorLabels and autosharding.enabled, exported_ renaming. Corrected the Helm key (prometheus.monitor.honorLabels does not exist). Removed the pinned v2.13.0 remote kustomize ref and the unconfirmed replica-per-pods and kube-prometheus-stack remarks.

Method: documentation only; no commands were run.
