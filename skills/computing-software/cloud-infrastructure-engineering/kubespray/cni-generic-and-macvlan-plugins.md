---
id: computing-software.cloud-infrastructure-engineering.kubespray.cni-generic-and-macvlan-plugins
name: cni-generic-and-macvlan-plugins
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [cni, macvlan, custom-cni, nodelocaldns, kube-proxy-masquerade]
level: practitioner
status: docs-checked
description: "Use Kubespray's bare cni plugin for custom setups, or the macvlan plugin with macvlan_interface, and apply the documented DNS fixes."
sources:
  - https://kubespray.io/docs/CNI/cni.md
  - https://kubespray.io/docs/CNI/macvlan.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Generic cni.** This network plugin only unpacks CNI plugins version `cni_version` into `/opt/cni/bin` and tells the container runtime CRI to use CNI. It is for custom CNI configuration (for example manual routing tables plus a bridge and loopback plugin outside Kubespray's scope) and for CNI plugins Kubespray does not support, which you install afterwards. You must fill `/etc/cni/net.d` with a valid CNI configuration after Kubespray finishes.

**Macvlan.** Enable it in `group_vars/k8s_cluster/k8s_cluster.yml`:

```yml
kube_network_plugin: macvlan
```

Then set `macvlan_interface` in `group_vars/k8s_cluster/k8s-net-macvlan.yml`, or per host in the inventory:

```yml
all:
  hosts:
    node1:
      ip: 10.2.2.1
      access_ip: 10.2.2.1
      ansible_host: 10.2.2.1
      macvlan_interface: ens5
```

Two issues are documented:
- Service DNS replying "from unexpected source": add `kube_proxy_masquerade_all: true` in `group_vars/all/all.yml`.
- The nodelocal DNS IP is not reachable: disable it with `enable_nodelocaldns: false` in `sample/group_vars/k8s_cluster/k8s_cluster.yml`.

## Checked

2026-11-08. Cited pages re-read in full. The generic plugin behaviour and the macvlan settings and issues were confirmed on the CNI and Macvlan pages.

Method: documentation only; no commands were run.
