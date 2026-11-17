---
id: computing-software.cloud-infrastructure-engineering.calico.overlay-ipip-and-vxlan-pool-modes
name: overlay-ipip-and-vxlan-pool-modes
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [encapsulation, ipip, vxlan, crosssubnet, ippool, overlay, felix, cluster-routes]
level: practitioner
status: docs-checked
description: "Choose and configure Calico overlays: IP-in-IP versus VXLAN, CrossSubnet, install-time settings, IPPool modes, and who programs cluster routes for each pool type."
sources:
  - https://docs.tigera.io/calico/latest/networking/configuring/vxlan-ipip
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Calico recommends running without encapsulation where the network can learn workload IPs (via static routes, BGP, or layer 2 learning): the packet leaving the workload is the packet on the wire. Use an overlay when the underlay cannot, for example across AWS VPC subnets.

**Which type.** IP-in-IP and VXLAN are supported. VXLAN works where IP-in-IP is blocked (Azure) but has a larger header. IP-in-IP is IPv4 only; IPv6 VXLAN needs kernel 4.19.1 or later (Red Hat 4.18.0 or later). Not supported with Calico for OpenStack.

**Best practice: CrossSubnet.** Encapsulate only traffic that crosses a subnet boundary. Switching modes can disrupt in-progress connections.

Operator install:

```yaml
kind: Installation
apiVersion: operator.tigera.io/v1
metadata:
  name: default
spec:
  calicoNetwork:
    ipPools:
      - cidr: 192.168.0.0/16
        encapsulation: VXLANCrossSubnet
```

Manifest installs use the `CALICO_IPV4POOL_VXLAN`, `CALICO_IPV4POOL_IPIP` and `CALICO_IPV6POOL_VXLAN` environment variables on calico-node.

**IPPool resource modes.** `ipipMode` and `vxlanMode` each take `Always` or `CrossSubnet`; for example:

```yaml
apiVersion: projectcalico.org/v3
kind: IPPool
metadata:
  name: ippool-vxlan-cross-subnet-1
spec:
  cidr: 192.168.0.0/16
  vxlanMode: CrossSubnet
  natOutgoing: true
```

**Cluster routes.** By default Felix programs cluster routes for VXLAN pools, while BGP distributes them for IP-in-IP pools and pools with no encapsulation. With only VXLAN pools BGP is not needed internally; it is still needed to advertise routes to external peers, and you may disable it in the manifests.

## Checked

2026-11-04. Guidance, limitations, YAML and cluster route behaviour were confirmed on the Configure overlay networking page.

Method: documentation only; no commands were run.
