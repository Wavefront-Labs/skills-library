---
id: computing-software.cloud-infrastructure-engineering.kubernetes.dual-stack-cni-calico-cilium
name: dual-stack-cni-calico-cilium
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, dual-stack, dual-stack-cni, calico, cilium, ipv6]
level: practitioner
status: docs-checked
description: "Configure Calico or Cilium for dual-stack pod addressing (IPv4 and IPv6 pools, IPAM, NAT and routing) to match a dual-stack cluster."
sources: ["https://docs.tigera.io/calico/latest/networking/ipam/ipv6", "https://docs.cilium.io/en/stable/network/concepts/ipam/kubernetes/", "https://kubernetes.io/docs/concepts/services-networking/dual-stack/", "https://docs.tigera.io/calico/latest/networking/configuring/vxlan-ipip"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dual-stack CNI configuration

The cluster must already have two pod CIDRs and two service CIDRs (kube-apiserver
`--service-cluster-ip-range=10.96.0.0/16,fd00:10:96::/112`, controller-manager
`--cluster-cidr=10.244.0.0/16,fd00:10:244::/56`). The CNI then has to hand out both families.
Kubernetes dual-stack is stable (since v1.23); IPv6 service ranges cannot be larger than
2^20 addresses (prefix length 108 or longer).

## Calico (operator)
```yaml
apiVersion: operator.tigera.io/v1
kind: Installation
metadata: {name: default}
spec:
  calicoNetwork:
    ipPools:
    - {cidr: 10.244.0.0/16, encapsulation: VXLANCrossSubnet, natOutgoing: Enabled}
    - {cidr: "fd00:10:244::/56", encapsulation: None, natOutgoing: Enabled}
    nodeAddressAutodetectionV4: {firstFound: true}
    nodeAddressAutodetectionV6: {firstFound: true}
```
`encapsulation` accepts `IPIP`, `VXLAN`, `IPIPCrossSubnet`, `VXLANCrossSubnet` or `None`.
Calico's dual-stack guide covers new clusters only. Manifest installs need
`FELIX_IPV6SUPPORT=true` and `IP6=autodetect` on `calico-node`, and
`"assign_ipv4": "true"` plus `"assign_ipv6": "true"` in the `calico-ipam` CNI config. Add
`CALICO_IPV6POOL_NAT_OUTGOING=true` if the IPv6 pool uses private addresses and pods need
outbound NAT. On kubeadm clusters Calico autodetects the pod CIDRs. VXLAN for IPv6 is
supported (kernel 4.19.1 or later, or Red Hat 4.18.0 or later) and uses a 70-byte header,
so the MTU is the underlay MTU minus 70 where IPv6 VXLAN is used.

## Cilium (Helm)
```yaml
ipv4: {enabled: true}
ipv6: {enabled: true}             # Helm default is false
ipam: {mode: kubernetes}          # Helm default is cluster-pool; kubernetes uses node.spec.podCIDRs
```
`ipam.mode=kubernetes` makes the agent wait for a PodCIDR of every enabled family on the
Node object, and the controller-manager must run with `--allocate-node-cidrs`. IPv6
masquerading (`enableIPv6Masquerade`) is already `true` by default in the Helm chart.

## Verify
```bash
kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name} {.spec.podCIDRs}{"\n"}{end}'
kubectl run t --image=nicolaka/netshoot --restart=Never -- sleep 3600
kubectl get pod t -o jsonpath='{.status.podIPs}'            # one v4 and one v6
kubectl exec t -- ping -6 -c1 <other-pod-ipv6>
```

## Gotchas
- Node InternalIPs must exist in both families (kubelet `--node-ip=<v4>,<v6>`) or IPv6 routing
  between nodes fails.
- Calico's IPv6 host requirements: a reachable IPv6 address, a default IPv6 route and
  `net.ipv6.conf.all.forwarding=1`.
- Cloud VPCs need IPv6 enabled on the subnets, route tables and security groups.

## Checked
2026-10-27. Documentation releases: Calico 3.33 (docs.tigera.io and tigera/operator API), Cilium v1.20.4 (Helm values and IPAM docs), Kubernetes website main (v1.38 dev tree; latest release v1.37.1) and kube-apiserver validation at v1.37.1.
Confirmed: operator `encapsulation` values and autodetection fields; manifest variables (`FELIX_IPV6SUPPORT`, `IP6`, `assign_ipv6`); Calico IPv6 VXLAN support and 70-byte overhead; Cilium `ipv6.enabled` default false, `ipam.mode` default cluster-pool, `enableIPv6Masquerade` default true; service CIDR size limit.
Method: documentation only; no commands were run.
