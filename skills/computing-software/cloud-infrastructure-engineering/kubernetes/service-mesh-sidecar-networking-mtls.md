---
id: computing-software.cloud-infrastructure-engineering.kubernetes.service-mesh-sidecar-networking-mtls
name: service-mesh-sidecar-networking-mtls
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, istio, linkerd, service-mesh, sidecar, envoy, mtls, traffic-shifting, iptables-redirect, ambient-mesh, sidecar-injection]
level: advanced
status: docs-checked
description: "How sidecar injection redirects traffic with iptables, what breaks it (startup ordering, PSA, CNI), and what mTLS and traffic shifting a mesh adds over NetworkPolicy."
sources: ["https://istio.io/latest/docs/ops/deployment/application-requirements/", "https://istio.io/latest/docs/setup/additional-setup/pod-security-admission/", "https://istio.io/latest/docs/ops/diagnostic-tools/proxy-cmd/", "https://linkerd.io/2/features/proxy-injection/", "https://linkerd.io/2/features/native-sidecars/", "https://istio.io/latest/docs/ambient/overview/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service mesh sidecar networking: how traffic capture actually works, and what it buys you

**Goal:** understand the plumbing that makes sidecar injection transparent (or breaks it),
and know precisely what a mesh adds over NetworkPolicy/CNI policy (mTLS with workload
identity, retries, traffic shifting) versus what it does not (coarse allow/deny, which
NetworkPolicy already does).

## 1. How traffic actually gets into the sidecar
- Istio injection adds an Envoy proxy container (`istio-proxy`) **plus an init container**,
  `istio-init`, that programs iptables rules in the pod's own network namespace so
  inbound traffic goes to Envoy's inbound port (15006) and outbound traffic to its outbound
  port (15001). The interception mode is `REDIRECT` or `TPROXY`
  (annotation `sidecar.istio.io/interceptionMode`). User ID 1337 is reserved for the proxy,
  so applications must not run as UID 1337.
- Linkerd does the same with a `linkerd-init` init container that configures iptables to
  forward incoming and outgoing TCP traffic through `linkerd-proxy`; that init container is
  not injected when the Linkerd CNI plugin is used. From Linkerd 2.20 the proxy is injected
  as a Kubernetes native sidecar (an init container with `restartPolicy: Always`), which
  Linkerd says fixes startup races with init containers and lets meshed Jobs terminate.
- `istio-init` needs the `NET_ADMIN` and `NET_RAW` capabilities, so whoever deploys pods
  needs RBAC and admission permission for them. Pod Security `baseline` does not allow
  those capabilities. Istio's PSA guide's answer is the Istio CNI plugin (`istio-cni-node`
  DaemonSet, whose namespace must allow the `privileged` level because it uses `hostPath`
  volumes), after which mesh namespaces can enforce `baseline` or `restricted` (with a
  `seccompProfile` configured for your apps).
- **Startup ordering** matters: if the application container starts sending traffic
  before the proxy is ready, requests can fail or bypass the mesh. Istio's
  `holdApplicationUntilProxyStarts` proxy setting exists to hold application containers
  until the proxy is ready; native sidecars (Istio's `ENABLE_NATIVE_SIDECARS`, defaulting
  to true from Istio 1.27 where supported) are the other mechanism. A pod that
  intermittently "isn't in the mesh" right after rollout is usually this ordering problem.

## 2. What a mesh adds that NetworkPolicy/CNI policy does not
- **mTLS with workload identity**: Istio issues each workload a certificate over Envoy's
  secret discovery service, identity-bound to the Kubernetes service account
  (SPIFFE-style), and rotates it periodically. Policy can be written as "this service
  account may call that service", which is cryptographically verified rather than based on
  IP or labels. Istio configures sidecars to use mTLS automatically ("auto mTLS") when
  calling workloads that have sidecars.
- **L7 traffic management**: weighted traffic splitting, retries, timeouts, circuit
  breaking and fault injection, configured with `VirtualService`/`DestinationRule` in Istio
  or `HTTPRoute`/policy resources in Linkerd; no app code changes. Core NetworkPolicy has none of this; Cilium's L7
  policy (see
  `computing-software.cloud-infrastructure-engineering.kubernetes.networkpolicy-advanced-fqdn-l7-tiers`)
  covers allow-listing at L7 but not retries or traffic splitting.
- **A mesh does not replace NetworkPolicy for coarse allow/deny**: the Kubernetes docs list
  gaps NetworkPolicy has (TLS, node identity, naming Services); a default-deny
  NetworkPolicy remains the right tool for "namespace X can never reach namespace Y",
  and the mesh's identity-based authorization is complementary. Running both is normal.

## 3. Sidecar overhead and the ambient alternative
- Every injected pod gets an extra proxy container, and every call crosses two proxies
  (client sidecar, then server sidecar). Istio publishes measured numbers; see
  `computing-software.cloud-infrastructure-engineering.kubernetes.sidecar-resource-overhead-and-ambient-tradeoffs`.
- **Ambient mode** removes per-pod sidecars: a per-node `ztunnel` handles L4 and mTLS, and
  optional L7 **waypoint** proxies handle HTTP-level features. Istio's feature-stage page
  tracks its status per release; check it for the version you run before relying on specific
  L7 features.

## 4. Debugging a pod that "isn't in the mesh" or has broken traffic
```bash
kubectl get pod <pod> -o jsonpath='{.spec.containers[*].name}'   # sidecar present?
kubectl exec -it <pod> -c istio-proxy -- pilot-agent request GET server_info
istioctl proxy-status                 # SYNCED / NOT SENT / STALE per proxy
istioctl analyze -n <ns>              # configuration analysis
istioctl x describe pod <pod>         # includes the effective PeerAuthentication / mTLS mode
# or Linkerd
linkerd diagnostics proxy-metrics -n <ns> po/<pod>
```
With native sidecars the proxy may be listed under init containers rather than containers.

## Verify
- [ ] The sidecar container is present and the pod's `READY` count includes it (e.g. `2/2`).
- [ ] `istioctl proxy-status` shows the proxy `SYNCED`: Istio documents `STALE` as an update
  sent to Envoy without an acknowledgement, which usually indicates a problem.
- [ ] mTLS is confirmed active with the mesh's own tools (`istioctl x describe pod`) and a
  capture, not assumed from config alone.
- [ ] A canary/traffic-split change is verified by measuring actual traffic distribution,
  not just by the percentage written in the config.

## Checked
2026-10-27. Documentation releases: istio.io docs (main) with istio/api annotations and 1.27/1.31 release notes and istioctl 1.31.3 source; Linkerd website docs (2-edge, 2.20 behaviour); Istio ambient overview.
Confirmed: ports 15001/15006, UID 1337, interception modes, `NET_ADMIN`/`NET_RAW` and the PSA/CNI guidance, `holdApplicationUntilProxyStarts`, native sidecar default from 1.27, auto mTLS, ambient ztunnel/waypoint roles, `istioctl x describe`/`proxy-status` semantics, Linkerd init container and native sidecar behaviour, `linkerd diagnostics proxy-metrics`.
Method: documentation only; no commands were run.
