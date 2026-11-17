---
id: computing-software.cloud-infrastructure-engineering.calico.ipv6-and-dual-stack-pools
name: ipv6-and-dual-stack-pools
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [ipv6, dual-stack, ippool, installation, cni, calico-ipam, felix, router-id]
level: practitioner
status: docs-checked
description: "Set up IPv6-only or dual-stack pod networking on a new cluster: Installation pools, CNI IPAM assign flags, IP6 and FELIX_IPV6SUPPORT."
sources:
  - https://docs.tigera.io/calico/latest/networking/ipam/ipv6
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Applies to **new clusters** only. Requires Calico IPAM; dual stack needs Kubernetes 1.16 or later. Hosts need a reachable address, forwarding sysctl `net.ipv6.conf.all.forwarding=1` (and the IPv4 equivalent) and a default route per family.

**Operator, IPv6 only:** one IPv6 pool, no IPv4 pool.

```yaml
apiVersion: operator.tigera.io/v1
kind: Installation
metadata:
  name: default
spec:
  calicoNetwork:
    ipPools:
      - blockSize: 122
        cidr: 2001::00/64
        encapsulation: None
        natOutgoing: Enabled
        nodeSelector: all()
```

**Operator, dual stack:** add an IPv4 pool (page example: `blockSize: 26`, `cidr: 10.48.0.0/21`, `encapsulation: IPIP`) beside the IPv6 one above.

**Manifest install.** Edit the `calico-config` ConfigMap IPAM block:

```json
"ipam": {
    "type": "calico-ipam",
    "assign_ipv4": "false",
    "assign_ipv6": "true"
},
```

(both `"true"` for dual stack). On the `calico-node` container set `IP6=autodetect` and `FELIX_IPV6SUPPORT=true`. Private IPv6 pools need `CALICO_IPV6POOL_NAT_OUTGOING: true` for outbound NAT. Non-kubeadm clusters also set `CALICO_IPV6POOL_CIDR` to the cluster CIDR given to kube-controller-manager and kube-proxy; kubeadm clusters are autodetected.

**IPv6 only with no IPv4 on hosts:** set `IP` to `none` to stop IPv4 autodetection, and set `CALICO_ROUTER_ID=hash` (or a unique value per node) for the BGP router ID.

## Checked

Read in full on 2026-11-08: the Configure dual stack or IPv6 only page. The requirements, both Installation examples, the CNI JSON and the environment variables match it.

Method: documentation only; no commands were run.
