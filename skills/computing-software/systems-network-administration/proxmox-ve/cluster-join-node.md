---
id: computing-software.systems-network-administration.proxmox-ve.cluster-join-node
name: cluster-join-node
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [pvecm-add, join-cluster, join-information, fingerprint, use-ssh]
level: practitioner
status: docs-checked
description: "Join a node to a Proxmox VE cluster using the GUI join information or pvecm add, and know what gets overwritten."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pvecm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Joining overwrites everything in `/etc/pve` on the new node, which inherits the cluster storage configuration. A joining node cannot hold guests, since guest IDs could conflict. Workaround: back up each guest with vzdump and restore it under a new ID after joining; if its storage layout differs, re-add storages and adjust each storage's node restriction.

GUI: on a cluster node open Datacenter, Cluster, Join Information, Copy Information. On the new node choose Join Cluster, paste, and enter the cluster password manually. The node certificate is replaced by one signed by the cluster CA, so the web session breaks after a few seconds; force-reload and log in again.

CLI on the new node:

```
pvecm add IP-ADDRESS-CLUSTER
pvecm status
pvecm nodes
```

Use an IP address rather than a hostname. By default it authenticates against the existing node's API with the `root@pam` password and verifies the SHA-256 certificate fingerprint, so SSH password authentication is not required. `--use_ssh` selects the legacy SSH-based join, which needs root SSH login on the existing node.

With a separate cluster network pass the local address on it: `pvecm add IP-ADDRESS-CLUSTER --link0 LOCAL-IP-ADDRESS-LINK0`, plus `--link1` for a second link. Healthy output of `pvecm status` shows `Quorate: Yes`, with expected, total and quorum votes consistent with the node count.

## Checked

2026-11-03. Commands, option names, defaults, limits and behaviour claims were compared with the official Proxmox VE documentation pages: https://pve.proxmox.com/pve-docs/chapter-pvecm.html (plus the chapter-qm, qm.1, pct, pvecm, pvesm, vzdump, pvesr and sysadmin pages). Items shown as placeholder or example values (file names, VM IDs, device names) are illustrative. Figures that the pages did not state were removed or reworded.

Method: documentation only; no commands were run.
