---
id: computing-software.cloud-infrastructure-engineering.kubernetes.egress-gateway-and-static-egress-ip
name: egress-gateway-and-static-egress-ip
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, egress, egress-gateway, static-ip, nat-gateway, cilium, calico, snat, ip-allowlisting, cloud-firewall, compliance, ciliumegressgatewaypolicy]
level: advanced
status: docs-checked
description: "Give workloads a stable, allow-listable source IP for external calls: Cilium egress gateway vs cloud NAT gateways, and why pod IPs are the wrong thing to allow-list."
sources: ["https://docs.cilium.io/en/stable/network/egress-gateway/egress-gateway/", "https://github.com/tigera/docs/blob/main/calico-enterprise/networking/egress/index.mdx", "https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-troubleshooting.html"]
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Egress gateways and static egress IPs: making a pod's traffic allow-listable

**Goal:** give an external partner (bank, SaaS API, customer firewall) a small, stable set of
source IPs to allow-list, instead of trying to allow-list an entire, constantly-changing pod
CIDR or node pool.

## 1. Why this is a recurring requirement
Partners that gate access by source-IP allow-list are common (financial APIs, enterprise
SaaS, customer-hosted webhooks). Pod IPs are ephemeral and numerous: never usable as the
allow-listed identity. Node IPs are more stable but still numerous and tied to autoscaling
events. The fix is to force a specific category of egress traffic through a small, fixed set
of IPs.

## 2. Cloud-level NAT gateway (simplest, works with any CNI)
- Route the node pool's egress through a cloud NAT gateway (AWS NAT Gateway, GCP Cloud NAT,
  equivalent) bound to one or a few static IPs. All outbound traffic from every pod
  on those nodes shares that IP.
- Pro: no CNI-specific config, works regardless of CNI choice. Con: **coarse**: every
  workload on that node pool shares the same egress identity; you cannot give team A a
  different allow-listed IP than team B without separate node pools or subnets per team.
- Cloud NAT gateways have a per-IP connection limit. AWS documents up to 55,000 concurrent
  connections per IP address on a NAT gateway and suggests adding IP addresses or more NAT
  gateways when you hit it (see
  `computing-software.cloud-infrastructure-engineering.kubernetes.conntrack-and-connection-scaling`).

## 3. Cilium Egress Gateway: per-workload granularity
```yaml
apiVersion: cilium.io/v2
kind: CiliumEgressGatewayPolicy
metadata: {name: billing-to-stripe}
spec:
  selectors:
  - podSelector: {matchLabels: {app: billing-worker}}
  destinationCIDRs: ["0.0.0.0/0"]
  egressGateway:
    nodeSelector: {matchLabels: {egress-gateway: "true"}}
    egressIP: "203.0.113.10"   # must already be an IP on a network interface of the gateway node
```
- Enable with Helm `egressGateway.enabled=true`, `bpf.masquerade=true` and
  `kubeProxyReplacement=true`: the docs require BPF masquerading and the kube-proxy
  replacement. It is not compatible with Cluster Mesh, with the `kvstore` identity
  allocation mode or with CiliumEndpointSlice (Cilium v1.20 docs).
- Matched pod traffic is SNAT'd to the gateway node's egress IP **regardless of which node
  the pod runs on**, giving per-workload (via `podSelector`) egress identity instead of
  per-node-pool. `nodeSelector` inside `selectors` can narrow the policy to pods on certain
  nodes but cannot be used without a `podSelector`.
- Select the egress interface with `egressGateway.interface` (first IPv4 and IPv6 address of
  that interface) or an explicit `egressIP`; the two cannot be combined (such a policy is
  ignored). With neither, the interface holding the default route is used. If no egress IP
  can be selected the gateway drops matching traffic with reason `No Egress IP configured`.
- Cilium does not allocate cloud IPs: the operator must provision and attach the
  interface or address (for example an ENI with extra IPs on AWS).
- Gateway node(s) become a traffic concentration point. With several gateways in
  `egressGateways: [...]`, **each source endpoint still uses a single gateway** (assigned by
  its CiliumEndpoint UID); it is a spread, not a failover pair. Changing the gateway node
  list reassigns endpoints and breaks existing egress connections (Cilium tracks this in
  issue 39245), so allow-list every gateway's egress IP with the partner.
- There is a delay before the policy applies to new pods: their first packets can leave with
  the pod or node IP.

## 4. Calico egress gateway
Calico's egress gateway documentation is part of the **Calico Enterprise** and Calico Cloud
docs (pod-based gateways with per-namespace or per-pod source IPs). The open-source Calico
3.33 documentation has no egress gateway guide and its networking index links to the
Calico Cloud page, so treat it as a commercial feature and check licensing before designing
around it.

## 5. Decision guide
| Need | Approach |
|---|---|
| "Allow-list our whole cluster's egress" | Cloud NAT gateway, done |
| "Give team X's workload a different allow-listed IP than everyone else" | Cilium egress gateway (or Calico Enterprise) |
| High-fanout egress (many short-lived connections) | Check the per-IP connection budget regardless of approach |

## Debug routine
```bash
# From inside the workload pod, confirm the observed source IP matches expectation
kubectl exec -it billing-worker-xyz -- curl -s https://ifconfig.me
# Cilium (the egress map is a debug command inside the agent pod)
kubectl -n kube-system exec ds/cilium -- cilium-dbg bpf egress list
kubectl get ciliumegressgatewaypolicy -o yaml
```

## Verify
- [ ] External call from the targeted workload shows the expected static IP at the partner's
  end (ask them to log/confirm, don't just trust client-side `ifconfig.me`).
- [ ] A workload NOT matched by the egress policy still egresses via its normal path (the
  policy didn't accidentally become cluster-wide).
- [ ] The partner's allow-list includes every gateway egress IP in the policy.
- [ ] Connection headroom at the egress IP is checked under realistic peak fanout,
  not just steady-state traffic.

## Checked
2026-10-27. Documentation releases: Cilium v1.20.4 (egress gateway docs and cmdref), Calico 3.33 docs (tigera/docs: egress gateway only under calico-enterprise and calico-cloud), AWS NAT gateway troubleshooting page.
Confirmed: policy fields (`selectors`, `podSelector`, `nodeSelector`, `destinationCIDRs`, `egressGateway.nodeSelector|interface|egressIP`, `egressGateways`), Helm prerequisites, incompatibilities, single-gateway-per-endpoint behaviour, 55,000 connections per AWS NAT IP. Calico egress gateway docs exist only in the Enterprise and Cloud trees.
Method: documentation only; no commands were run.
