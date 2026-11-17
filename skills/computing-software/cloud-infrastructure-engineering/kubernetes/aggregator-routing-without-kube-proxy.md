---
id: computing-software.cloud-infrastructure-engineering.kubernetes.aggregator-routing-without-kube-proxy
name: aggregator-routing-without-kube-proxy
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, aggregation-layer, enable-aggregator-routing, kube-apiserver, apiservice, metrics-server]
level: practitioner
status: docs-checked
description: "Use kube-apiserver --enable-aggregator-routing so aggregated APIs work when control-plane nodes cannot reach Service ClusterIPs (no kube-proxy or external control planes)."
sources: ["https://kubernetes.io/docs/tasks/extend-kubernetes/configure-aggregation-layer/", "https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# --enable-aggregator-routing

By default the apiserver proxies requests for an aggregated API (for example
`/apis/metrics.k8s.io`) to the APIService's Service **ClusterIP**. The Kubernetes docs say that if
you are not running kube-proxy on a host running the API server, you must enable
`--enable-aggregator-routing=true`. Where control-plane nodes cannot reach Service ClusterIPs,
aggregated API calls fail (typically a connection timeout to the ClusterIP).

## Fix
```
--enable-aggregator-routing=true
```
The flag routes aggregator requests to endpoint IPs rather than the cluster IP (kube-apiserver
reference). The metrics-server README says it also load-balances requests between multiple
Metrics Server replicas. Pod IPs must be routable from the control-plane nodes (CNI running there,
or routes).

## When you need it
- Control-plane hosts that do not run kube-proxy (or an equivalent that handles Service ClusterIPs).
- Control planes hosted outside the cluster network.
- Debugging an APIService that is `Available=False` with timeouts while the backing pods are healthy.
- Running several Metrics Server replicas: the metrics-server README recommends the flag so requests
  are load balanced between instances.

## Gotchas
- If pod IPs are not reachable either, fix routing; the metrics-server README notes the control plane
  must reach the Metrics Server pod IP and port 10250 (or node IP and custom port if `hostNetwork`
  is enabled).
- The apiserver also needs the front-proxy client cert configured (`--proxy-client-cert-file`),
  independent of this flag.

## Verify
```bash
kubectl get apiservice v1beta1.metrics.k8s.io -o jsonpath='{.status.conditions[0].status}'
kubectl top nodes
```
`True` and data returned.

## Checked
Checked 2026-10-24 against the kubernetes/website "Configure the Aggregation Layer" page, the
kube-apiserver flag reference (`--enable-aggregator-routing`: "Turns on aggregator routing requests
to endpoints IP rather than cluster IP") and the metrics-server README (network requirements and
the load-balancing recommendation).
Method: documentation only; no commands were run.
