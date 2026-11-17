---
id: computing-software.systems-network-administration.proxmox-ve.cluster-remove-node
name: cluster-remove-node
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [delnode, remove-node, pvecm-delnode, cleanup, separate-node]
level: advanced
status: docs-checked
description: "Remove a node from a Proxmox VE cluster with pvecm delnode, including prerequisites, Ceph steps and cleanup."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pvecm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Before removal: move all guests away, back up local data, remove the node from every replication job (otherwise the job becomes irremovable), and remove any QDevice first. For a Ceph node, destroy its OSDs one at a time waiting for HEALTH_OK each time, destroy MDS, monitor and manager, then `ceph osd crush remove node4`. Make sure the remaining nodes still satisfy pool `size` (default 3) and `min_size` (default 2), or IO will block.

Then power the node off and make sure it never boots again on this network with its current config, otherwise the cluster can break. On a remaining node:

```
pvecm delnode node4
pvecm nodes
```

An error `could not kill node (error = cs_err_not_exist)` can be ignored.

Cleanup: recover then delete `/etc/pve/nodes/node4`; if SSH complains after a same-name rejoin run `pvecm updatecerts`; remove the node from HA rules; delete its public key from `/etc/pve/priv/authorized_keys`. To reuse the server, reinstall Proxmox VE and join again.

Separating a node without reinstalling is not recommended. The node must not share any storage with the old cluster, because locking does not work across clusters and VMIDs would collide. Then:

```
systemctl stop pve-cluster
systemctl stop corosync
pmxcfs -l
rm /etc/pve/corosync.conf
rm -r /etc/corosync/*
killall pmxcfs
systemctl start pve-cluster
```

Afterwards `pvecm delnode oldnode` from the cluster (use `pvecm expected 1` if quorum is lost), and `rm /var/lib/corosync/*` on the separated node.

## Checked

2026-11-09. Compared with the Remove a Cluster Node and Separate a Node Without Reinstalling sections of https://pve.proxmox.com/pve-docs/chapter-pvecm.html; prerequisites, Ceph size and min_size defaults, error note, cleanup and separation commands match.

Method: documentation only; no commands were run.

