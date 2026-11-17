---
id: computing-software.cloud-infrastructure-engineering.kubespray.inventory-bastion-host
name: inventory-bastion-host
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [inventory, bastion, ssh, private-network]
level: intro
status: docs-checked
description: "Reach nodes that only have private IPs by adding a bastion group to the Kubespray inventory with the public address of the jump host."
sources:
  - https://kubespray.io/docs/ansible/inventory.md
  - https://kubespray.io/docs/operations/port-requirements.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When nodes have private IPs only and should not be publicly accessible, Kubespray supports a bastion host: a jump host that Ansible connects through to reach every node.

You declare it by adding a `bastion` group to the inventory with one line, replacing `x.x.x.x` with the bastion's public IP:

```ShellSession
[bastion]
bastion ansible_host=x.x.x.x
```

The Inventory page lists `bastion` as one of two special groups (the other being `calico_rr`), so it sits alongside, not inside, `kube_control_plane`, `kube_node` and `etcd`.

The page points to a third-party article, "Running Ansible Through an SSH Bastion Host", for the Ansible side of the setup.

The Port Requirements page lists TCP 22 (ssh for ansible) on control plane and worker nodes.

## Checked

2026-11-04. The bastion group syntax and the special-group wording are from the Inventory page; the TCP 22 requirement is from the Port Requirements page. Removed unsupported remarks about cluster variables and SSH settings.

Method: documentation only; no commands were run.
