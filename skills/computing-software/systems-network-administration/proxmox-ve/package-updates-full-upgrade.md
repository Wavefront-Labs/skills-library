---
id: computing-software.systems-network-administration.proxmox-ve.package-updates-full-upgrade
name: package-updates-full-upgrade
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [updates, apt-full-upgrade, rolling-release, changelog]
level: intro
status: docs-checked
description: "Update Proxmox VE hosts with apt update and apt full-upgrade, and why plain apt upgrade is the wrong tool."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-sysadmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Proxmox VE is a rolling release on top of Debian. Install updates from the GUI (Node, Updates) or the CLI:

```
apt update
apt full-upgrade
```

Use `full-upgrade`, not `upgrade`. Proxmox packages change dependencies, and `apt full-upgrade` can remove existing packages to satisfy them while `apt upgrade` cannot, so a plain upgrade may leave a partially upgraded or broken package state.

Proxmox VE checks for package updates daily and emails the `root@pam` user when updates are available. In the GUI, the Changelog button shows details of a selected update. Major upgrades follow the Proxmox VE upgrade guide.

Ceph is upgraded separately: to move a hyper-converged cluster to the succeeding Ceph major release, follow the Ceph upgrade guide. Each Proxmox VE major release requires a minimum Ceph major release, so check the upgrade guide before upgrading a hyper-converged cluster.

Microcode updates always need a host reboot. Before rebooting a node that runs guests, make sure it can be done safely, moving or shutting down guests first. On clusters, check `pvecm status` to confirm the cluster stays quorate.

## Checked

2026-11-09. Compared with the package update, Ceph repositories and firmware sections of https://pve.proxmox.com/pve-docs/chapter-sysadmin.html. Removed the forum announcement, security patch and one-node-at-a-time statements, which the page does not make.

Method: documentation only; no commands were run.

