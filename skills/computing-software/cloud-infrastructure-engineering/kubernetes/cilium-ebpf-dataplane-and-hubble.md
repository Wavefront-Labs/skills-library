---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cilium-ebpf-dataplane-and-hubble
name: cilium-ebpf-dataplane-and-hubble
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cilium, ebpf, hubble, kube-proxy-replacement, xdp, tc, observability, service-mesh, l7-visibility, flow-logs, networking]
level: advanced
status: gated
description: "Run Cilium as a full kube-proxy replacement and read cluster traffic with Hubble: eBPF hook points, identity caching, and the flows that actually tell you what broke."
sources: ["https://docs.cilium.io/en/stable/network/kubernetes/kubeproxy-free/", "https://docs.cilium.io/en/stable/security/network/identity/", "https://docs.cilium.io/en/stable/observability/hubble/hubble-cli/", "https://docs.cilium.io/en/stable/observability/hubble/setup/", "https://docs.cilium.io/en/stable/operations/troubleshooting/", "https://github.com/cilium/cilium/blob/main/api/v1/flow/flow.proto"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cilium's eBPF dataplane and Hubble — operating it, not just enabling it

**Goal:** understand where Cilium intercepts packets, why that makes it faster and more
observable than iptables, and how to use Hubble to answer "why can't A reach B" in seconds.

## 1. Where eBPF hooks in
- **Traffic-control (TC) hook placement**: which exact hook points Cilium attaches programs to
  (gated: unconfirmed, source is paywalled or blocked; the fetched pages do not describe it).
  Check the Cilium datapath reference for your release.
- **XDP** (eXpress Data Path): optional acceleration for LoadBalancer and NodePort traffic
  (`loadBalancer.acceleration`; see the kube-proxy-free guide's XDP section, which lists the
  driver and mode requirements).
- **Socket-level load balancing**: Cilium's kube-proxy replacement depends on socket LB. On
  `connect` (TCP, connected UDP), `sendmsg` and `recvmsg` (UDP) the service address is
  translated so the kernel socket is connected directly to the backend address. It can be
  bypassed in pod namespaces with `socketLB.hostNamespaceOnly=true`, which is needed for
  KubeVirt, Kata Containers and Istio sidecar setups.

## 2. kube-proxy replacement
```
helm upgrade cilium cilium/cilium --namespace kube-system --reuse-values \
  --set kubeProxyReplacement=true \
  --set k8sServiceHost=<API_SERVER_IP> --set k8sServicePort=6443
```
- `k8sServiceHost` and `k8sServicePort` must point at the API server directly: the guide
  runs `kubeadm init --skip-phases=addon/kube-proxy`, so nothing provisions the kube-apiserver
  ClusterIP and the agent needs the real address (kubeadm defaults to port 6443). Helm sets
  `kubeProxyReplacement=false` by default; `true` makes the agent bail out if kernel support
  is missing.
- Verify with `cilium-dbg status` (run in the agent pod) — look for `KubeProxyReplacement: True`
  and check `cilium-dbg service list` shows every Service with backends.
- With the replacement active, `iptables-save | grep KUBE-SVC` on the host shows no rules for
  Services — that is the documented check, not a fault.

## 3. Identity and policy caching
- Every pod's security identity is derived from its labels and can be shared between pods:
  starting another `role=frontend` pod only requires resolving the existing identity through a
  key-value store, with no per-node action (Cilium identity docs).
- `cilium-dbg endpoint list` (run in the agent pod) shows endpoints with their identities —
  the first place to look when policy seems to apply to the wrong pods. Details of the ipcache
  and policy maps are not in the fetched pages (gated: unconfirmed, source is paywalled or blocked).
- A stuck identity sync would show up as policy that works on one node and not another; the
  identity docs describe the key-value store as the propagation path.

## 4. Hubble — the observability payoff
- `hubble observe` streams flow events with a verdict (`FORWARDED`, `DROPPED`, `AUDIT` and
  others; there is no `DENIED` verdict) and, for drops, a drop reason — the fastest way to
  answer "is my NetworkPolicy blocking this" without guessing. L7 flows need an L7 policy or
  visibility setting that redirects traffic to the proxy (gated: unconfirmed, source is paywalled or blocked; exact setting names vary by release).
```bash
hubble observe --namespace shop --to-pod api-xyz --verdict DROPPED
hubble observe --protocol http --namespace shop   # L7 flows, only for traffic redirected to the L7 proxy
```
- `DROPPED` flows carry a drop reason such as `Policy denied`, `Invalid source ip` or
  `CT: Map insertion failed` (a connection-tracking map insertion failure, not a policy decision).
- Hubble UI / Relay aggregates flows cluster-wide into a service map — useful for onboarding
  someone to an unfamiliar cluster's actual traffic graph, not just its declared topology.
- Hubble is a live flow view; for postmortem retention use Hubble's export or metrics features
  (gated: unconfirmed, source is paywalled or blocked; check the Hubble configuration docs for your release).

## 5. Common gotchas
- Replacing a running kube-proxy breaks existing connections, because the two NAT tables are
  not aware of each other (kube-proxy-free guide). The guide's removal steps are
  `kubectl -n kube-system delete ds kube-proxy`, deleting the `kube-proxy` ConfigMap so
  kubeadm does not reinstall it, and `iptables-save | grep -v KUBE | iptables-restore` on each node —
  plan a maintenance window.
- MTU: tunnelling adds encapsulation headers that reduce the effective payload MTU (Cilium
  routing docs; see `computing-software.cloud-infrastructure-engineering.kubernetes.mtu-overlay-fragmentation-troubleshooting`).
- Inside the agent pod the binary is `cilium-dbg`; the separate `cilium` command is the CLI
  used for install, status and connectivity tests.

## Verify
- [ ] `cilium-dbg status` shows `KubeProxyReplacement: True` with no errors.
- [ ] `iptables-save | grep KUBE-SVC` is empty when replacement is enabled — no leftover
  kube-proxy rules.
- [ ] A deliberately-blocked connection shows up in `hubble observe --verdict DROPPED` with a
  specific reason, not just a timeout in the app.
- [ ] L7 HTTP visibility (if enabled) shows method/path/status in `hubble observe --protocol http`.

Drop reason strings and Helm value names vary by release; confirm them against the installed version's docs before scripting around them.

## Checked
2026-10-26. Checked against the Cilium documentation source (repository cilium/cilium, last commit 2026-10-25). Confirmed: Helm default is `kubeProxyReplacement=false` and `true` makes the agent bail out if kernel support is missing; `k8sServiceHost` and `k8sServicePort` are needed because kubeadm is run without kube-proxy so nothing provisions the kube-apiserver ClusterIP; `cilium-dbg status`, `cilium-dbg service list` and `cilium-dbg endpoint list`; socket-level load balancing at connect, sendmsg and recvmsg with `socketLB.hostNamespaceOnly` as the bypass; XDP acceleration applies to LoadBalancer and NodePort; identity is derived from labels and shared between pods; Hubble verdicts include FORWARDED, DROPPED and AUDIT (there is no DENIED verdict); drop reasons `Policy denied`, `Invalid source ip` and `CT: Map insertion failed`. The migration steps follow the kube-proxy removal commands in the guide. Marked gated: eBPF hook placement (TC), ipcache details, the Hubble retention claim and the L7 visibility switch name, which the fetched pages do not state.
Method: documentation only; no commands were run.
