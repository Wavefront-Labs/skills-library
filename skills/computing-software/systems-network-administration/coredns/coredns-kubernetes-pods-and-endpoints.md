---
id: computing-software.systems-network-administration.coredns.coredns-kubernetes-pods-and-endpoints
name: coredns-kubernetes-pods-and-endpoints
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, kubernetes, pods, endpoints, headless]
level: advanced
status: docs-checked
description: "Control pod A records with pods disabled, insecure or verified, endpoint naming, noendpoints and TTL in the kubernetes plugin."
sources:
  - https://coredns.io/plugins/kubernetes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: choose which Kubernetes records are answered.

`pods POD-MODE` handles IP-based pod records like `1-2-3-4.ns.pod.cluster.local. in A 1.2.3.4`:
- `disabled` (default): always NXDOMAIN.
- `insecure`: always returns an A record from the name without checking Kubernetes. It is vulnerable to abuse with wildcard SSL certs and exists for kube-dns compatibility.
- `verified`: returns a record only if a pod with that IP exists in the same namespace. It needs substantially more memory, since it watches all pods.

`endpoint_pod_names`: name endpoints by pod name. Default is the endpoint hostname, else the dashed IP (1-2-3-4). With the option: hostname, else the pod name, falling back to the dashed IP if there is no pod or the name exceeds 63 characters.

`noendpoints` turns off the watch on endpoints. All endpoint and headless service queries then return NXDOMAIN.

`ttl TTL` sets the response TTL. Default 5 seconds, minimum 0, maximum 3600. A TTL of 0 prevents caching.

`ignore empty_service` returns NXDOMAIN for services with no ready endpoints, so the querying pod can continue down its search path, which might include another cluster.

`multicluster [ZONES...]` defines Multi-Cluster Services API zones; the plugin must be authoritative for them.

## Checked

2026-11-03. Page read: https://coredns.io/plugins/kubernetes/ (the CoreDNS plugin page).

Confirmed: the syntax, options, defaults, limits, metric names and examples stated in this skill.

Removed or corrected: nothing.

Method: documentation only; no commands were run.
