---
id: computing-software.cloud-infrastructure-engineering.kubernetes.istio-mesh-troubleshooting-analyze-and-proxy-config
name: istio-mesh-troubleshooting-analyze-and-proxy-config
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, istio, service-mesh, istioctl-analyze, proxy-config, proxy-status, envoy, mesh-troubleshooting]
level: advanced
status: docs-checked
description: "Debug Istio traffic issues: istioctl analyze for config errors, proxy-status for xDS sync, proxy-config listeners/routes/clusters/endpoints, Envoy access log response flags."
sources: ["https://istio.io/latest/docs/ops/diagnostic-tools/istioctl-analyze/", "https://istio.io/latest/docs/ops/diagnostic-tools/proxy-cmd/", "https://istio.io/latest/docs/reference/commands/istioctl/", "https://istio.io/latest/docs/reference/config/analysis/", "https://www.envoyproxy.io/docs/envoy/latest/configuration/advanced/substitution_formatter"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Istio troubleshooting: analyze and proxy-config

## 1. Static config problems
```bash
istioctl analyze -A                       # whole mesh
istioctl analyze -n shop                  # namespace
istioctl analyze manifests/ --use-kube=false   # in CI, before apply
```
Typical findings: `IST0101 ReferencedResourceNotFound` (VirtualService → missing Gateway/host),
`IST0106 SchemaValidationError`, `IST0118 PortNameIsNotUnderNamingConvention`
(Service ports should be named `http-*`/`grpc-*` or set `appProtocol`), conflicting
VirtualServices for one host, DestinationRule subsets with no matching pods.

## 2. Is the proxy in sync?
```bash
istioctl proxy-status                      # SYNCED / STALE / NOT SENT per proxy and xDS type
```
STALE → istiod has not pushed the latest configuration to that proxy; check istiod logs and connectivity to istiod. No row → the pod has no sidecar (check the namespace injection label and the pod's containers).

## 3. What does Envoy actually have?
```bash
P="deploy/frontend -n shop"
istioctl proxy-config listeners $P --port 8080
istioctl proxy-config routes $P --name 8080 -o json
istioctl proxy-config clusters $P --fqdn orders.orders.svc.cluster.local
istioctl proxy-config endpoints $P --cluster "outbound|8080||orders.orders.svc.cluster.local"   # HEALTHY/UNHEALTHY
istioctl proxy-config secret $P            # certs: validity, root CA
istioctl x describe pod <pod> -n shop      # which VS/DR/policies apply
```
Endpoints empty → check the Service selector and whether `exportTo` hides the service; UNHEALTHY → the proxy considers the endpoint unhealthy (for example ejected by outlier detection).

## 4. Read access logs (response flags)
```bash
kubectl logs <pod> -c istio-proxy | tail
```
| Flag | Meaning |
|---|---|
| `UH` | no healthy upstream |
| `UF` | upstream connection failure (mTLS mismatch, port wrong) |
| `NR` | no route configured (host/port not matching any VirtualService/route) |
| `URX` | retry limit exceeded |
| `UO` | circuit breaker overflow |
| `DC` / `UC` | downstream/upstream connection closed |
`UF` and `UH` come with a 503, and `NR` with a 404 (per Envoy). Compare the flag with the route and cluster config from section 3 to find which resource is mismatched.

## 5. Raise Envoy log level temporarily
`istioctl proxy-config log <pod> --level connection:debug,router:debug`; the istioctl reference shows `--level none` as an example for turning loggers off again.

## Verify
- [ ] `istioctl analyze -A` clean in CI; all proxies SYNCED; issue reproduced and fixed with a matching access-log flag change.

## Checked
2026-10-26. Checked against the istio.io docs source (repository istio/istio.io, last commit 2026-10-23) and the Envoy docs source (substitution_formatter). Confirmed: `istioctl analyze` flags `--all-namespaces`/`-A` and `--use-kube=false`; analysis messages IST0101 ReferencedResourceNotFound, IST0106 SchemaValidationError and IST0118 PortNameIsNotUnderNamingConvention; `istioctl proxy-config` listeners, routes, clusters, endpoints, secret and log subcommands; `istioctl experimental describe`; Envoy response flags UH, UF, NR, URX, UO, DC, UC with their meanings. Removed as unconfirmed: the cause lists for STALE rows, the 503/UF root-cause hints and the jq pipeline.
Method: documentation only; no commands were run.
