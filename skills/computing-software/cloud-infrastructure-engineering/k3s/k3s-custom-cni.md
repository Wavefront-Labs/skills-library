---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-custom-cni
name: k3s-custom-cni
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, custom-cni, canal, calico, cilium]
level: advanced
status: docs-checked
description: "Replace Flannel with Canal, Calico or Cilium by starting K3s with --flannel-backend=none and --disable-network-policy."
sources:
  - https://docs.k3s.io/networking/basic-network-options
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run your own CNI.

Start K3s with `--flannel-backend=none` and install the CNI. Most CNIs ship their own network policy engine, so also set `--disable-network-policy` to avoid conflicts.

Canal and Calico: edit the manifest so IP forwarding is allowed in container_settings:

```
"container_settings": {
  "allow_ip_forwarding": true
}
```

Apply it, then confirm on the host with `cat /etc/cni/net.d/10-canal.conflist` (or 10-calico.conflist); it should show IP forwarding true.

Cilium: before running k3s-killall.sh or k3s-uninstall.sh you must manually remove its interfaces, or you may lose network connectivity to the host when K3s stops:

```
ip link delete cilium_host
ip link delete cilium_net
ip link delete cilium_vxlan
iptables-save | grep -iv cilium | iptables-restore
ip6tables-save | grep -iv cilium | ip6tables-restore
```

## Checked

2026-11-08: read the whole Basic Network Options page (raw markdown from the k3s-io/docs repo, which backs docs.k3s.io/networking/basic-network-options), including the Custom CNI tabs. Confirmed flags, the IP forwarding snippet, conflist checks and Cilium cleanup. Removed unsupported claims: the Flannel ports note and the KUBE-ROUTER iptables cleanup.

Method: documentation only; no commands were run.
