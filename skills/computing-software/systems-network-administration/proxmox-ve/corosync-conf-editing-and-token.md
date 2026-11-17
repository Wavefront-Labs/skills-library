---
id: computing-software.systems-network-administration.proxmox-ve.corosync-conf-editing-and-token
name: corosync-conf-editing-and-token
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [corosync-conf, config-version, token-coefficient, pvecm-expected, edit-corosync]
level: advanced
status: docs-checked
description: "Edit corosync.conf safely on Proxmox VE, tune token_coefficient, and recover a node without quorum."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pvecm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two copies exist: `/etc/pve/corosync.conf` (cluster filesystem) and `/etc/corosync/corosync.conf` (local). Editing the cluster copy propagates to the local one, not the other way round, and a saved change applies immediately. Use `pvecm` for node membership; hand-edit only for other changes, with a working copy:

```
cp /etc/pve/corosync.conf /etc/pve/corosync.conf.new
# edit the .new file, increment config_version
cp /etc/pve/corosync.conf /etc/pve/corosync.conf.bak
mv /etc/pve/corosync.conf.new /etc/pve/corosync.conf
systemctl status corosync
journalctl -b -u corosync
```

Always increment `config_version`. Restart corosync only if the change did not apply by itself. To add a redundant link, add `ringX_addr` to every node in `nodelist` and an `interface { linknumber: X }` block in `totem`.

Timing: `token = 3000 + (nodes - 2) * token_coefficient`, `consensus = 1.2 * token`. The default coefficient is 650 ms; new clusters from Proxmox VE 9.2 set `token_coefficient: 125` in `totem`. Keep token plus consensus below 30 seconds, and with HA far below 45 seconds so membership re-forms before the 60 second watchdog fences nodes. Check with:

```
corosync-cmapctl | grep -Ew 'runtime.config.totem.token|runtime.config.totem.consensus'
```

Without quorum, `pvecm expected 1` makes the cluster quorate so you can fix the config. If corosync cannot start, edit `/etc/corosync/corosync.conf` identically on all nodes. An error about `nodelist or quorum.expected_votes` means a ringX_addr hostname does not resolve.

## Checked

2026-11-03. Commands, option names, defaults, limits and behaviour claims were compared with the official Proxmox VE documentation pages: https://pve.proxmox.com/pve-docs/chapter-pvecm.html (plus the chapter-qm, qm.1, pct, pvecm, pvesm, vzdump, pvesr and sysadmin pages). Items shown as placeholder or example values (file names, VM IDs, device names) are illustrative. Figures that the pages did not state were removed or reworded.

Method: documentation only; no commands were run.
