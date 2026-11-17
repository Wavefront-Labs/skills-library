---
id: computing-software.cloud-infrastructure-engineering.kubernetes.istio-ambient-mode-ztunnel-waypoint
name: istio-ambient-mode-ztunnel-waypoint
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, istio, ambient-mode, ztunnel, waypoint, hbone, sidecar-less, service-mesh, mtls, l4, l7, ambient-mesh]
level: advanced
status: docs-checked
description: "Istio ambient mode's split L4/L7 architecture — ztunnel per node, optional waypoint per namespace — and what migrating off sidecars actually changes operationally."
sources: ["https://istio.io/latest/docs/ambient/architecture/data-plane/", "https://istio.io/latest/docs/ambient/architecture/hbone/", "https://istio.io/latest/docs/ambient/usage/waypoint/", "https://istio.io/latest/docs/ambient/usage/add-workloads/", "https://istio.io/latest/docs/ambient/usage/l7-features/", "https://istio.io/latest/docs/ambient/migrate/enable-ambient-mode/", "https://istio.io/latest/docs/ambient/usage/troubleshoot-ztunnel/", "https://istio.io/latest/news/releases/1.24.x/announcing-1.24/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Istio ambient mode — ztunnel and waypoints

**Goal:** understand ambient as a genuinely different architecture, not "Istio without the
YAML change" — know which workloads need a waypoint and which don't, and what you lose.
Status note: ambient reached GA in Istio 1.24 but is younger in production than sidecar
mode; verify current behavior against your exact version before relying on specifics here.
Resource-overhead comparison against sidecars is in
`sidecar-resource-overhead-and-ambient-tradeoffs`.

## 1. The split: ztunnel (L4) and waypoint (L7)
- **ztunnel**: one per node, written in Rust (github.com/istio/ztunnel), handles every enrolled pod on that node.
  Does mTLS origination/termination, basic L4 authorization (`AuthorizationPolicy` with
  only L4 fields — source identity, ports), and the `HBONE` tunnel protocol
  (HTTP/2 CONNECT plus mTLS, TCP port 15008) between workloads. There is no per-pod proxy:
  the istio-cni node agent transparently redirects an enrolled pod's traffic to the node-local ztunnel.
- **waypoint**: an Envoy Deployment created from a Kubernetes Gateway API `Gateway` with
  `gatewayClassName: istio-waypoint` (`istioctl waypoint apply -n <ns>`). Traffic uses it
  only when the namespace, Service or pod carries `istio.io/use-waypoint=<waypoint-name>`
  (`--enroll-namespace` applies the namespace label). By default a waypoint handles traffic
  addressed to Services (`istio.io/waypoint-for: service`); use `--for workload` or `all`
  for traffic addressed to pod IPs. Only workloads that need L7 features — HTTP-aware
  routing, retries/timeouts, L7 authorization — need one. Plain L4 mTLS traffic never
  touches a waypoint.
- Traffic path for an L7-needing call: pod → local ztunnel → (HBONE over the network) →
  destination waypoint (does L7 policy/routing) → destination ztunnel → destination pod.
  That's more hops than a sidecar's single in-process detour — budget for it in latency
  budgets, don't assume ambient is strictly faster end to end just because it's "sidecar-
  less" (it removes per-pod proxy CPU, not inter-hop latency).

## 2. What you keep, what changes, what you lose
- **Keep**: automatic mTLS for every ambient pod (ztunnel-issued, same SPIFFE identity
  model as sidecar mode) and L4 `AuthorizationPolicy` enforced by ztunnel.
- **Changes**: L7 traffic management only applies to traffic that goes through a waypoint,
  and waypoints are configured with Gateway API objects such as `HTTPRoute` (Beta). Usage
  of `VirtualService` in ambient mode is documented as Alpha, and mixing it with Gateway API
  configuration is unsupported (`istio-traffic-management-virtualservice-destinationrule`
  covers the sidecar model). Always check `kubectl get gateway -n <ns>` for a waypoint and
  the `istio.io/use-waypoint` label before debugging "my L7 routing isn't working."
- **Lose (today)**: not every sidecar-mode feature has an ambient equivalent — check the
  current Istio release notes for gaps (this list drifts release to release). The ambient
  docs state that `EnvoyFilter` is not supported with waypoint proxies.

## 3. Migration path
Ambient and sidecar mode coexist in the same mesh — migrate namespace by namespace:
The documented order is: enrol, then remove injection, then restart pods last.
```bash
kubectl label namespace <ns> istio.io/dataplane-mode=ambient      # enrol; pods keep sidecars, which take precedence
istioctl ztunnel-config workloads -n istio-system | grep <ns>      # confirm HBONE workloads
kubectl label namespace <ns> istio-injection-                      # or istio.io/rev- if you use a revision label
kubectl rollout restart deployment -n <ns>                         # new pods come up without sidecars
```
Removing the injection label alone does not remove existing sidecars from running pods —
you need the rollout, and not before ambient is confirmed. Immediately after the restart,
delete old selector-based L7 `AuthorizationPolicy` objects: ztunnel only understands L4
attributes and drops L7 conditions, which can turn an ALLOW or DENY policy into deny-all.
Watch ztunnel logs (`kubectl -n istio-system logs -l app=ztunnel`) during the switch. Do not
label a namespace with both `istio-injection=enabled` and `istio.io/dataplane-mode=ambient`.

## Verify
- [ ] For every namespace relying on canary/mirror/circuit-breaking, a waypoint Gateway
  actually exists (`kubectl get gateway -A`, class `istio-waypoint`) and is selected by `istio.io/use-waypoint`.
- [ ] `istioctl ztunnel-config` (or equivalent for your version) shows the workload's
  identity and policy loaded on the correct node's ztunnel.
- [ ] A namespace migrated to ambient shows zero `istio-proxy` containers after rollout.
- [ ] Latency budgets account for the extra waypoint hop on any L7-policy path, measured,
  not assumed.

## Checked
2026-10-26. Checked against the istio.io documentation source (repository istio/istio.io, last commit 2026-10-23) and the 1.24 release announcement. Confirmed: ambient GA in Istio 1.24; HBONE on TCP port 15008 (HTTP/2 CONNECT plus mTLS); labels `istio.io/dataplane-mode` (ambient or none), `istio.io/use-waypoint` and `istio.io/waypoint-for` (default service); waypoint Gateway uses `gatewayClassName: istio-waypoint` and `istioctl waypoint apply [--enroll-namespace] [--for workload]`; documented migration order (label ambient, remove injection label, restart pods, delete old selector-based L7 policies); `istioctl ztunnel-config` and `kubectl -n istio-system logs -l app=ztunnel`; VirtualService in ambient is Alpha and EnvoyFilter is unsupported with waypoints. Corrected: how a waypoint is requested, the migration command order, and the per-ServiceAccount, per-node DaemonSet and iptables claims, which no doc covers.
Method: documentation only; no commands were run.
