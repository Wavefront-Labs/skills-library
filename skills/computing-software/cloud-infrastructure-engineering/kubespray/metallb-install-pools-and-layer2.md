---
id: computing-software.cloud-infrastructure-engineering.kubespray.metallb-install-pools-and-layer2
name: metallb-install-pools-and-layer2
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [metallb, loadbalancer, layer2, address-pools, strict-arp, addons]
level: practitioner
status: docs-checked
description: "Enable MetalLB in Kubespray with strict ARP, define address pools, run Layer2 mode and add control plane tolerations."
sources:
  - https://kubespray.io/docs/ingress/metallb.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
MetalLB provides LoadBalancer services in clusters without a cloud provider. Its default mode is Layer2; BGP is also supported.

**Prerequisite.** Configure arp_ignore and arp_announce so the node does not answer ARP queries from the `kube-ipvs0` interface:

```yaml
kube_proxy_strict_arp: true
```

**Install.** Enable explicitly (resources go to the `metallb-system` namespace unless you set `metallb_namespace`):

```yaml
metallb_enabled: true
metallb_speaker_enabled: true
```

**Control plane tolerations.** By default only the BGP speaker may run on control plane nodes. For a single-node or control-plane-as-worker cluster, give the controller a toleration for `node-role.kubernetes.io/control-plane` with effect `NoSchedule` under `metallb_config.controller`; `metallb_config.speaker` takes the same nodeselector and tolerations.

**Pools:**

```yaml
metallb_config:
  address_pools:
    primary:
      ip_range:
        - 192.0.1.0-192.0.1.254
    pool1:
      ip_range:
        - 192.0.2.1-192.0.2.1
      auto_assign: false # When set to false, you need to explicitly set the loadBalancerIP in the service!
    pool2:
      ip_range:
        - 192.0.3.0/24
      avoid_buggy_ips: true # When set to true, .0 and .255 addresses will be avoided.
```

**Layer2.** Name the pools to announce in layer2 mode as a list:

```yaml
metallb_config:
  layer2:
    - primary
```

## Checked

2026-11-08. Cited pages re-read in full. Prerequisite, install, toleration, pool and Layer2 settings were confirmed on the MetalLB page.

Method: documentation only; no commands were run.
