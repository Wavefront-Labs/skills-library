---
id: computing-software.cloud-infrastructure-engineering.calico.mtu-sizing-for-overlays-and-wireguard
name: mtu-sizing-for-overlays-and-wireguard
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [mtu, veth, tunnel, wireguard, vxlan, ipip, installation, aks, fragmentation]
level: practitioner
status: docs-checked
description: "Set Calico MTU from the underlay MTU: subtract 20 for IP-in-IP, 50 for IPv4 VXLAN, 60 for IPv4 WireGuard, 80 for IPv6 WireGuard; patch Installation or calico-config."
sources:
  - https://docs.tigera.io/calico/latest/networking/configuring/mtu
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Calico auto-detects MTU from node configuration and enabled networking modes. For this to work, disable unused encapsulations in FelixConfiguration (`vxlanEnabled` and the like). Override when auto-detection is wrong. MTU is applied to workload veths and tunnel devices; use the highest value that avoids fragmentation or drops on every path, i.e. the minimum MTU of any path.

**Header costs:** IP-in-IP 20 bytes, IPv4 VXLAN 50, IPv6 VXLAN 70, IPv4 WireGuard 60, IPv6 WireGuard 80. Sample rows from the page's table (Calico MTU for IPv4 IP-in-IP, VXLAN, WireGuard): network 1500 gives 1480, 1450, 1440; 9000 gives 8980, 8950, 8940; GCE 1460 gives 1440, 1410, 1400. AKS is 1500 on the interface but the underlay is 1400, so WireGuard there is 1340 (IPv6 1320) because WireGuard sets the Don't Fragment bit.

**Rule when mixing:** use the smallest value any encapsulation needs.

- IPv4 WireGuard anywhere: physical MTU minus 60 (IPv6: minus 80)
- else IPv4 VXLAN anywhere: minus 50 (IPv6: minus 70)
- else IP-in-IP only: minus 20
- Set workload and tunnel MTUs the same.

In eBPF mode NodePorts use VXLAN, so size workloads as physical minus 50. With flannel, match the flannel interface MTU.

**Set it.** Operator:

```bash
kubectl patch installation.operator.tigera.io default --type merge -p '{"spec":{"calicoNetwork":{"mtu":1440}}}'
```

(`oc` on OpenShift.) Manifests: patch ConfigMap `calico-config` in `kube-system` with `veth_mtu`, then `kubectl rollout restart daemonset calico-node -n kube-system`. New MTU applies only to new workloads. Inspect tunnels with `ip link show` (IP-in-IP appears as `tunl0`).

## Checked

2026-11-08. The Configure MTU page was read in full. Header sizes, selected table rows, rules, commands and the new-workloads-only note were confirmed on the Configure MTU page.

Method: documentation only; no commands were run.
