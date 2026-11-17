---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cilium-service-mesh-sidecar-free
name: cilium-service-mesh-sidecar-free
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cilium, ebpf, service-mesh, cni, sidecar-free, wireguard, ipsec, envoy, mtls, spire, l7-policy, cluster-mesh, hubble]
level: advanced
status: gated
description: "Cilium's sidecar-free service mesh: eBPF-enforced L3/L4 policy plus optional per-node Envoy for L7, transparent WireGuard/IPsec encryption instead of per-connection mTLS handshakes."
sources: ["https://docs.cilium.io/en/stable/network/servicemesh/", "https://docs.cilium.io/en/stable/security/network/proxy/envoy/", "https://docs.cilium.io/en/stable/security/network/encryption/", "https://docs.cilium.io/en/stable/security/network/encryption-wireguard/", "https://docs.cilium.io/en/stable/security/network/encryption-ztunnel/", "https://docs.cilium.io/en/stable/security/policy/layer7/", "https://docs.cilium.io/en/stable/network/servicemesh/istio/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cilium as service mesh — sidecar-free by construction

**Goal:** know how Cilium gets mesh-like properties (L7 policy, encryption, observability)
without a per-pod proxy, because it's architecturally different from Istio/Linkerd, not
just a lighter version of them. If your cluster already runs Cilium as CNI, this is often
the lowest-overhead path to "mesh-lite" — see `when-not-to-use-a-service-mesh` for when
even this is more than you need.

## 1. The core idea: policy enforcement moves into the kernel
Cilium's CNI already attaches eBPF programs at the pod's veth/socket layer for networking.
Service-mesh features reuse that same attachment point instead of adding a new user-space
proxy per pod:
- **L3/L4 identity-based policy** (`CiliumNetworkPolicy`, allow/deny by pod identity/label,
  not just IP) is enforced directly in the eBPF datapath — no proxy hop at all for traffic
  that doesn't need L7 inspection.
- **L7 policy** (HTTP and DNS rules in the current layer 7 policy docs) still needs a proxy, because
  Cilium parses application protocols such as HTTP and DNS with Envoy (per the service mesh
  overview). By default the agent starts Envoy as a separate process inside the per-node
  Cilium agent pod; alternatively it runs as an independently managed `cilium-envoy`
  DaemonSet (Helm `envoy.enabled=true`). Either way it is per node, not per pod, and traffic
  needing L7 rules goes through the node-local Envoy.

## 2. Encryption: transparent, not per-connection mTLS
Cilium's transparent encryption docs list three modes: IPsec, WireGuard and ztunnel.
- **WireGuard**: needs the WireGuard kernel module; enabled with
  `--set encryption.enabled=true --set encryption.type=wireguard`. Packets destined to the same
  node are not encrypted. Node-to-node encryption (`encryption.nodeEncryption=true`) is a beta option.
- **IPsec**: `encryption.type=ipsec`, with keys supplied through a Kubernetes secret.
- **ztunnel (Beta)**: a per-node proxy that gives transparent layer 4 mTLS encryption and
  authentication; pods are enrolled per namespace and redirected using iptables rules in
  their network namespace.
- Don't conflate "traffic is encrypted" (WireGuard/IPsec) with "the peer's identity is
  verified" (mTLS): of the three modes, only ztunnel is described as providing mutual TLS
  authentication. An older SPIFFE/SPIRE mutual-authentication feature is not in the current docs
  (gated: unconfirmed, source is paywalled or blocked).

## 3. Observability: Hubble
Hubble (Cilium's observability layer) taps the same eBPF datapath for flow-level
visibility — `hubble observe` shows connections with identity, verdict (`FORWARDED`,
`DROPPED`, `AUDIT` and others) and L7 metadata where a proxy was in the path, without needing
a sidecar to emit the access log. The Hubble UI (`cilium hubble enable --ui`) gives a service
map. See `service-mesh-observability-integration` for the cross-mesh comparison.

## 4. What this does and doesn't replace
- Covers: transparent encryption and identity-based L3/L4 plus L7 policy for teams already
  running Cilium as CNI, with no sidecar process per pod. The size of the resource saving is
  not documented (gated: unconfirmed, source is paywalled or blocked); measure it.
- Cilium also has Envoy-based traffic management pages (circuit breaker, traffic shifting,
  load balancing) in its service mesh docs; compare them with Istio's feature set before
  choosing.
- Combining with Istio: the Cilium Istio guide supports running Cilium with or without
  kube-proxy. With `kubeProxyReplacement: true` set `socketLB.hostNamespaceOnly: true` and
  `cni.exclusive: false` so socket load balancing does not interfere with Istio's proxying.

## Verify
- [ ] `cilium status` encryption section matches what Helm values declare.
- [ ] `hubble observe --verdict DROPPED` during a policy change shows exactly the traffic
  you intended to block, nothing more.
- [ ] L7 flows (`hubble observe --protocol http`) appear for traffic covered by an L7 rule,
  confirming it is reaching the Envoy proxy.
- [ ] Before claiming "mTLS," confirmed whether ztunnel mode is enabled, versus relying on
  WireGuard/IPsec transport encryption alone.

## Checked
2026-10-26. Checked against the Cilium documentation source (repository cilium/cilium, last commit 2026-10-25). Confirmed: Cilium uses eBPF for IP, TCP and UDP and a proxy such as Envoy for HTTP, gRPC and DNS; Envoy runs inside the agent pod by default or as a separate `cilium-envoy` DaemonSet (`envoy.enabled=true`); transparent encryption options are IPsec, WireGuard and ztunnel (Beta); WireGuard is enabled with `encryption.enabled=true` and `encryption.type=wireguard`, does not encrypt traffic that stays on the same node, and has beta node-to-node encryption via `encryption.nodeEncryption=true`; the layer 7 policy page documents HTTP and DNS rules; Hubble verdicts have no DENIED value; Istio on Cilium needs `socketLB.hostNamespaceOnly: true` and `cni.exclusive: false` when kube-proxy replacement is on. Corrected: Envoy is not always embedded in the agent, Kafka and gRPC rule types are not listed, and the SPIFFE mutual-authentication page no longer exists in the docs. Marked gated: the sidecar-overhead comparison and the ambient pairing details.
Method: documentation only; no commands were run.
