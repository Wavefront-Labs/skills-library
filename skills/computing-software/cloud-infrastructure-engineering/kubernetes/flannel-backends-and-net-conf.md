---
id: computing-software.cloud-infrastructure-engineering.kubernetes.flannel-backends-and-net-conf
name: flannel-backends-and-net-conf
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cni, flannel, flannel-backend, net-conf-json, vxlan]
level: practitioner
status: docs-checked
description: "Configure Flannel's net-conf.json (pod network, vxlan, host-gw, wireguard backends, DirectRouting) and plan backend choice, since the backend should not change at runtime."
sources: ["https://github.com/flannel-io/flannel/blob/master/Documentation/backends.md", "https://github.com/flannel-io/flannel/blob/master/Documentation/configuration.md", "https://github.com/flannel-io/flannel/blob/master/Documentation/troubleshooting.md", "https://github.com/flannel-io/flannel/blob/master/Documentation/kube-flannel.yml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flannel backends and net-conf.json

Config lives in the `kube-flannel-cfg` ConfigMap (namespace `kube-flannel`; DaemonSet
`kube-flannel-ds`) in the project's `kube-flannel.yml` manifest:
```json
{
  "Network": "10.244.0.0/16",
  "EnableNFTables": false,
  "Backend": { "Type": "vxlan", "VNI": 1, "Port": 8472, "DirectRouting": true }
}
```
`Network` must match the cluster pod CIDR; with kubeadm pass
`--pod-network-cidr=10.244.0.0/16` to `kubeadm init` so every node gets a `podCIDR`. Each
node's subnet comes from its `node.spec.podCIDR` (flannel in `--kube-subnet-mgr` mode).
`EnableNFTables` (nftables instead of iptables for masquerading) is marked experimental.
`Backend` defaults to `vxlan`.

## Backends
| Type | How | Requirements |
|---|---|---|
| `vxlan` (recommended) | in-kernel VXLAN; `VNI` default 1; `Port` default is the kernel default (currently 8472 on Linux) | open that UDP port between nodes; `MTU` option, else the external interface MTU is used |
| `vxlan` + `DirectRouting: true` | host-gw style routes between hosts on the same subnet, VXLAN only across subnets | mixed networks |
| `host-gw` | IP routes to peer subnets via node IPs, no encapsulation | direct layer-2 connectivity between hosts; typically not usable in cloud environments |
| `wireguard` | in-kernel WireGuard, encrypted; `ListenPort` default 51820, `ListenPortV6` 51821 | kernel WireGuard (kernels older than 5.6 need the package) |
| `udp` | userspace, default port 8285 | debugging only, or kernels without VXLAN |
`ipip` and `ipsec` also exist but the docs list them as experimental. If `firewalld` is
enabled on a node, open the backend's port with `firewall-cmd --permanent --zone=public
--add-port=<port>/udp`.

## Changing the backend
Flannel's documentation says that once the backend is set it should not be changed at
runtime. Decide the backend before the cluster carries traffic; to switch later, plan it as
a rebuild (new nodes or a new cluster) or a full maintenance window, not a rolling edit of
the ConfigMap.

## Debug
```bash
kubectl -n kube-flannel logs ds/kube-flannel-ds | grep -i -E 'backend|error'
cat /run/flannel/subnet.env            # FLANNEL_NETWORK, FLANNEL_SUBNET, FLANNEL_MTU, FLANNEL_IPMASQ
ip -d link show flannel.1; ip route | grep 10.244
```
Pods on different nodes cannot talk with the `vxlan` backend: the troubleshooting guide
says the kernel uses UDP 8472 for encapsulated packets, so check the firewall rules
(including cloud security groups) between all nodes.

## Gotchas
Plain Flannel does not enforce NetworkPolicy. From v0.25.5 the optional
`kube-network-policies` controller can be deployed with it (Helm `netpol.enabled=true`);
otherwise pair Flannel with Calico (Canal) or use another CNI.

## Checked
2026-10-27. Documentation release: Flannel v0.28.10 (backends, configuration, kubernetes, netpol and troubleshooting docs, kube-flannel.yml).
Confirmed: ConfigMap and DaemonSet names, `Network`/`Backend` defaults, per-backend options and ports, experimental status of `EnableNFTables`/`ipip`/`ipsec`, `subnet.env` variables, "backend should not be changed at runtime", NetworkPolicy support via kube-network-policies.
Method: documentation only; no commands were run.
