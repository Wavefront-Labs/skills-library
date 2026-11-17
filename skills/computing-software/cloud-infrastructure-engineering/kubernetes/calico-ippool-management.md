---
id: computing-software.cloud-infrastructure-engineering.kubernetes.calico-ippool-management
name: calico-ippool-management
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, calico, calico-ipam, ippool, ipam, cni]
level: practitioner
status: docs-checked
description: "Manage Calico IPPools: blockSize, encapsulation and natOutgoing per pool, node selectors for per-rack pools, and migrating pods to a new pool safely."
sources: ["https://docs.tigera.io/calico/latest/reference/resources/ippool", "https://docs.tigera.io/calico/latest/networking/ipam/migrate-pools", "https://docs.tigera.io/calico/latest/reference/configure-cni-plugins", "https://docs.tigera.io/calico/latest/networking/ipam/change-block-size", "https://github.com/tigera/operator/blob/master/api/v1/installation_types.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Calico IPPools

```bash
calicoctl get ippool -o wide     # v3 API; kubectl also works with the Calico API server or native v3 CRDs
calicoctl ipam show
calicoctl ipam show --show-blocks
```

## Pool fields
```yaml
apiVersion: projectcalico.org/v3
kind: IPPool
metadata: {name: pool-b}
spec:
  cidr: 10.48.0.0/16
  blockSize: 26               # /26 = 64 IPs per block (default IPv4 26, IPv6 122); set at creation only
  ipipMode: Never
  vxlanMode: CrossSubnet      # encapsulate only between subnets
  natOutgoing: true           # masquerade traffic to destinations outside any Calico IP pool
  nodeSelector: all()         # or rack == "r1" for per-rack pools
  disabled: false
```
Each node claims blocks on demand. `ipipMode` and `vxlanMode` cannot both be enabled; `blockSize` can only be
set when the pool is created (IPv4 20 to 32). A larger block (for example 24) means fewer blocks per host and
potentially fewer routes; a smaller one (for example 28) means more blocks and routes but less waste on
small nodes. `allowedUses` (`Workload`, `Tunnel`, `LoadBalancer`; since v3.21) controls what a pool is used for.

## Migrate pods to a new pool
1. Add the new pool. Keep it inside the Kubernetes cluster CIDR, and make sure a kube-proxy `clusterCIDR`
   contains it, or some traffic is NAT-ed unnecessarily.
2. Disable the old pool (`disabled: true`). This only stops new allocations; existing pods keep working.
3. Delete pods that use the old pool (including any created before it was disabled); expect brief
   unavailability depending on the application.
4. Verify new pods get addresses from the new pool (`calicoctl ipam show --show-blocks`), then delete the old pool.
Deleting the old pool before the new one is created and verified affects existing pods.
With the Tigera operator, pools are defined in `Installation.spec.calicoNetwork.ipPools`;
change them there or the operator recreates the old pool.

## Per-namespace or per-pod pools
Annotation `cni.projectcalico.org/ipv4pools: '["pool-b"]'` on a pod or namespace (a list of pool names; the
`ipv6pools` annotation does the same for IPv6). A pool's `namespaceSelector` can also bind it to namespaces
(when set, `namespaceSelector` and `nodeSelector` must both match).

## Gotchas
- Pools should sit inside the cluster CIDR (for kubeadm, `--pod-network-cidr`), and a kube-proxy
  `clusterCIDR` must contain them to avoid unwanted NAT.
- Calico recommends `natOutgoing` on pools with IPIP or VXLAN enabled; without it, routing between
  workloads and external destinations needs the network to route pod addresses back.
- Leaked IPs after node deletion: `calicoctl ipam check` then `calicoctl ipam release`.

## Checked

Documentation release: Calico docs (tigera/docs repo, calico/ docs, repo commit 2026-10-23; Calico release v3.33.0).
Confirmed: IPPool fields (`cidr`, `blockSize` 20-32 IPv4 / 116-128 IPv6, creation only, defaults 26 and 122; `ipipMode`/`vxlanMode` mutually exclusive with `Always|CrossSubnet|Never`; `natOutgoing`; `disabled`; `nodeSelector`; `namespaceSelector`; `allowedUses` since v3.21); the pool migration procedure; the `cni.projectcalico.org/ipv4pools` annotation; `calicoctl ipam show --show-blocks`, `ipam check`, `ipam release` exist; the operator `Installation` type has `ipPools`.
Removed or corrected: the `kubectl get ippools.crd.projectcalico.org` form (native v3 CRDs are an alternative storage mode), the unsourced "small blockSize spreads IPs on small nodes" explanation, the step "wait until no allocations" (the docs say delete the pods, verify, then delete).

Method: documentation only; no commands were run.
