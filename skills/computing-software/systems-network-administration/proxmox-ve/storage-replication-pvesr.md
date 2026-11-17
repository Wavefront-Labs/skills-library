---
id: computing-software.systems-network-administration.proxmox-ve.storage-replication-pvesr
name: storage-replication-pvesr
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [pvesr, storage-replication, zfs-replication, replication-job]
level: practitioner
status: docs-checked
description: "Replicate guests between nodes on local ZFS storage with pvesr, set schedules and rate limits, and recover a guest after node failure."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pvesr.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Storage replication copies guest volumes to another node so data is available without shared storage, and it shortens migration. It uses snapshots, so after the initial full sync only deltas are sent. The supported storage type is ZFS (plugin `zfspool`). The interval ranges from one minute to once a week, defaults to every 15 minutes, uses systemd calendar event style, and failed jobs are retried every 30 minutes. A guest may replicate to several targets but not twice to the same one, and each job can have a rate limit. When you migrate a guest to its replication target, the direction switches automatically.

Jobs are identified by VMID plus job number:

```
pvesr create-local-job 100-0 pve1 --schedule "*/5" --rate 10
pvesr disable 100-0
pvesr enable 100-0
pvesr update 100-0 --schedule '*/00'
```

HA can be combined with replication, but data written since the last sync is lost if a node fails. Common failure causes: broken network, no free space on the target, or no storage with the same ID on the target node.

If node A dies for good, on node B check `pvecm status`. Without quorum, fix that first, and only if impossible use `pvecm expected 1`, avoiding cluster changes afterwards. Then move the config files and start the guests:

```
mv /etc/pve/nodes/A/qemu-server/100.conf /etc/pve/nodes/B/qemu-server/100.conf
mv /etc/pve/nodes/A/lxc/200.conf /etc/pve/nodes/B/lxc/200.conf
qm start 100
pct start 200
```

## Checked

2026-11-03. Commands, option names, defaults, limits and behaviour claims were compared with the official Proxmox VE documentation pages: https://pve.proxmox.com/pve-docs/chapter-pvesr.html (plus the chapter-qm, qm.1, pct, pvecm, pvesm, vzdump, pvesr and sysadmin pages). Items shown as placeholder or example values (file names, VM IDs, device names) are illustrative. Figures that the pages did not state were removed or reworded.

Method: documentation only; no commands were run.
