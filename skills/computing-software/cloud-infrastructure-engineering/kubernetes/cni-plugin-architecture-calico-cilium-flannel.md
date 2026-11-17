---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cni-plugin-architecture-calico-cilium-flannel
name: cni-plugin-architecture-calico-cilium-flannel
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cni, calico, cilium, flannel, vxlan, ipip, bgp, ebpf, overlay, underlay, ipam, networking, cluster-networking, datapath]
level: advanced
status: docs-checked
description: "Pick and operate a CNI plugin by understanding its actual datapath: Flannel VXLAN/host-gw, Calico BGP/IPIP/VXLAN, Cilium eBPF, not the marketing slide."
sources: ["https://github.com/flannel-io/flannel/blob/master/Documentation/backends.md", "https://docs.tigera.io/calico/latest/getting-started/kubernetes/requirements", "https://docs.tigera.io/calico/latest/networking/determine-best-networking", "https://docs.cilium.io/en/stable/operations/system_requirements/", "https://github.com/containernetworking/cni"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CNI plugin architecture: Flannel, Calico, Cilium, and how to actually choose

**Goal:** know what each CNI plugin puts on the wire so you can predict performance,
debug an unreachable pod, and justify a migration instead of cargo-culting a choice.

## 1. What a CNI plugin actually does
Three jobs, done differently by every plugin: (1) **IPAM**: assign a pod CIDR per node
and an IP per pod; (2) **datapath**: get packets from pod A to pod B, same node or not;
(3) **policy enforcement**: optional, not every plugin does it.
The plugin binary lives in the CNI binary directory (`/opt/cni/bin` by default) and its
config in `/etc/cni/net.d`; Calico's requirements page states it must use these default
Kubernetes CNI directories. A broken CNI config means pods stick in `ContainerCreating`
with a CNI error in the pod events.

## 2. Flannel: simplest, least capable
- Default backend **VXLAN**: in-kernel VXLAN encapsulation. On Linux the UDP port is the
  kernel default, currently **8472** (Windows must use 4789). VXLAN costs about 50 bytes
  per packet (see the MTU skill).
- **host-gw** backend: no encapsulation, adds routes to each peer's pod subnet via the
  peer's node IP. Flannel's docs say it needs direct layer-2 connectivity between hosts
  and typically cannot be used in cloud environments.
- Other backends: `wireguard` (encrypted, default UDP 51820), `ipip` and `ipsec`
  (listed as experimental), `udp` (debugging only). Flannel's docs say the backend
  should not be changed at runtime once set.
- NetworkPolicy: plain Flannel does not enforce it. From Flannel v0.25.5 you can deploy
  the optional kubernetes-sigs `kube-network-policies` controller (Helm value
  `netpol.enabled=true`), or pair Flannel with Calico ("Canal"). No BGP.

## 3. Calico: routing-first, policy-rich
- Networking modes: non-overlay routing with **BGP**, **IP-in-IP** or **VXLAN**
  overlays, each with cross-subnet variants (encapsulate only between subnets). Calico's
  docs say most public clouds support IPIP, with Azure the notable exception (use VXLAN).
- BGP: by default Calico builds a full node-to-node iBGP mesh; the docs call this fine
  for about 100 nodes or fewer and recommend route reflectors at larger scale.
- `calico/node` runs **Felix** (programs routes and ACLs on the host) and **BIRD** (the BGP
  client). **Typha** is a separate daemon between the datastore and many Felix
  instances; it caches datastore state to cut API-server load, and operator installs
  always install it.
- Policy: Kubernetes NetworkPolicy plus Calico `NetworkPolicy`/`GlobalNetworkPolicy`,
  **tiers** (ordered groups with higher-precedence policies other teams cannot
  override) and `HostEndpoint` policy for the node itself.
- Optional eBPF dataplane replaces kube-proxy. Enable it with the operator
  `Installation` field `spec.calicoNetwork.linuxDataplane: BPF`; the docs require Linux
  kernel 5.10+ (or RHEL 8.4's 4.18.0-305 build or later).

## 4. Cilium: eBPF-native, most capability
- Identity-based policy: endpoints get a **security identity** derived from labels, and
  policy is enforced against identities rather than IP addresses.
- Routing: native routing or an overlay (VXLAN or Geneve). Cloud IPAM modes exist for
  AWS ENI and GKE, among others (see Cilium's IPAM docs).
- Can replace kube-proxy (`kubeProxyReplacement`). See
  `computing-software.cloud-infrastructure-engineering.kubernetes.cilium-ebpf-dataplane-and-hubble`
  for the operational detail and observability (Hubble).
- Kernel requirement for Cilium 1.20: Linux kernel **5.10 or later** (or 4.18 on
  RHEL 8.10). Individual features can need newer kernels; check the system requirements
  page of the exact release before upgrading a host OS.

## 5. Choosing (decision table)
| Need | Pick |
|---|---|
| Simplest possible, no policy needed | Flannel |
| BGP-native on-prem, tiered policy, host firewalling | Calico |
| FQDN/L7 policy, deep observability, kube-proxy replacement | Cilium |
| Already running a service mesh (Istio/Linkerd) for L7 | CNI can be simpler (Flannel/Calico); let the mesh own L7 |

## 6. Migration reality check
- Calico's requirements page says that, generally, Calico cannot be used together with
  another network provider (exceptions: Flannel, and platform CNIs such as AWS VPC CNI and
  Azure VNet CNI) and that you cannot migrate an existing cluster from another CNI to
  Calico in place. Plan CNI migration as new nodes or a new cluster: cordon and drain in
  batches, or stand up a new node pool with the new CNI and move workloads (blue/green at
  node-pool level). Never run two CNIs live on the same node.
- Before migrating, audit every `NetworkPolicy`/CRD policy resource for CNI-specific
  extensions (Calico `GlobalNetworkPolicy`, Cilium `CiliumNetworkPolicy`): they do not port
  automatically to another plugin.

## Debug routine
```bash
kubectl -n kube-system get pods -o wide | grep -E 'calico|cilium|flannel'
kubectl get nodes -o jsonpath='{.items[*].spec.podCIDR}'
# Calico
calicoctl node status; calicoctl get bgppeer
# Cilium
cilium status; cilium connectivity test
# Flannel (on the node)
cat /run/flannel/subnet.env; ip -d link show flannel.1
```

## Verify
- [ ] Identify which of VXLAN/IPIP/native-routing/eBPF is actually active (`ip -d link show`,
  not the plugin's marketing name).
- [ ] Cross-node pod-to-pod ping/curl works and packet capture shows the expected
  encapsulation (or none).
- [ ] NetworkPolicy enforcement is confirmed working if the plugin claims to support it;
  test with a denied connection.

## Checked
2026-10-27. Documentation releases: Flannel v0.28.10, Calico 3.33 (docs.tigera.io), Cilium v1.20.4.
Confirmed: Flannel VXLAN default port 8472 (not 4789), backend list and "do not change backend at runtime", optional netpol since v0.25.5; Calico traffic modes, ~100-node full-mesh guidance, Felix/BIRD/Typha roles, tiers, eBPF `linuxDataplane: BPF` and kernel 5.10+; Cilium kernel 5.10+ (4.18 on RHEL 8.10), identity-based policy.
Method: documentation only; no commands were run.
