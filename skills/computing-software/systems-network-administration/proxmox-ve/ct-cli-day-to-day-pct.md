---
id: computing-software.systems-network-administration.proxmox-ve.ct-cli-day-to-day-pct
name: ct-cli-day-to-day-pct
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [lxc, pct, pct-set, pct-destroy]
level: intro
status: docs-checked
description: "Day-to-day container management with pct on Proxmox VE, including console, enter, hot-plug set, destroy purge and volume moves."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pct.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`pct` is the Proxmox Container Toolkit. Frequent commands:

```
pct start 100
pct console 100        # login session via getty
pct enter 100          # namespace shell as root
pct config 100
pct set 100 -net0 name=eth0,bridge=vmbr0,ip=192.168.15.147/24,gw=192.168.15.1
pct set 100 -memory 512
```

Most changes are hot plugged into a running container. A change that cannot be hot plugged becomes a pending change, shown in red in the GUI, and applies after a reboot. Editing `/etc/pve/lxc/100.conf` by hand is possible for small corrections but needs a restart, so prefer `pct set`.

Destroying a container always removes it from access control lists and removes its firewall configuration. Add `--purge` to also remove it from replication jobs, backup jobs and HA resource configuration:

```
pct destroy 100 --purge
```

Purging also removes the HA resource from any affinity rules referencing it, and deletes rules left with only that one resource.

Move volumes between storages or reassign them to another container (the volume is renamed to match its new owner):

```
pct move-volume 100 mp0 other-storage
pct move-volume 100 mp0 --target-vmid 200 --target-volume mp1
```

## Checked

2026-11-03. Commands, option names, defaults, limits and behaviour claims were compared with the official Proxmox VE documentation pages: https://pve.proxmox.com/pve-docs/chapter-pct.html (plus the chapter-qm, qm.1, pct, pvecm, pvesm, vzdump, pvesr and sysadmin pages). Items shown as placeholder or example values (file names, VM IDs, device names) are illustrative. Figures that the pages did not state were removed or reworded.

Method: documentation only; no commands were run.
