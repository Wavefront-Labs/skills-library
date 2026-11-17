---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-server-roles-etcd-controlplane
name: k3s-server-roles-etcd-controlplane
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, cluster-init, disable-apiserver, disable-etcd]
level: advanced
status: docs-checked
description: "Split embedded-etcd K3s servers into dedicated etcd and control-plane nodes with the disable flags."
sources:
  - https://docs.k3s.io/installation/server-roles
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run etcd and control-plane components on separate server nodes. Only relevant with embedded etcd; otherwise every server has the control-plane role.

`--cluster-init` runs all control-plane components (apiserver, controller-manager, scheduler, etcd). Disable pieces to split roles.

Dedicated etcd node:

```
curl -fL https://get.k3s.io | sh -s - server --cluster-init --disable-apiserver --disable-controller-manager --disable-scheduler
```

It starts etcd and waits for more etcd or control-plane nodes. The cluster is not usable until you join a server with the control-plane components enabled.

Dedicated control-plane node:

```
curl -fL https://get.k3s.io | sh -s - server --token <token> --disable-etcd --server https://<etcd-only-node>:6443
```

A dedicated control-plane node cannot be the first server; an existing etcd-role node must exist before it joins.

`kubectl get nodes` then shows ROLES etcd for the etcd node and control-plane,master for the control-plane node.

Adding roles later: remove the disable flags from the systemd unit or config file and restart the service.

Config file form in /etc/rancher/k3s/config.yaml:

```
cluster-init: true
disable-apiserver: true
disable-controller-manager: true
disable-scheduler: true
```

## Checked

2026-11-03: read docs.k3s.io installation/server-roles. Confirmed: the dedicated etcd and control-plane commands, the first-server restriction, the resulting roles and the config-file form.

Method: documentation only; no commands were run.
