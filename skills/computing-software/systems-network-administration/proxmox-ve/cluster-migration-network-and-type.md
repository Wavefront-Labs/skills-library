---
id: computing-software.systems-network-administration.proxmox-ve.cluster-migration-network-and-type
name: cluster-migration-network-and-type
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [migration-network, migration-type, insecure-migration, datacenter-cfg, qm-migrate]
level: practitioner
status: docs-checked
description: "Move guest migration traffic to a dedicated network and choose secure or insecure transport on Proxmox VE."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pvecm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default migration traffic uses the cluster (corosync) network, which is bad: heavy migration can disturb cluster communication, and that network may be slow. Set a dedicated migration network in CIDR form in `/etc/pve/datacenter.cfg`; each node must have exactly one IP in that network, so Proxmox can resolve the right address per node. It also covers storage traffic for offline migrations. The type must always be set together with the network.

```
migration: secure,network=10.1.2.0/24
```

For one migration, override on the command line:

```
qm migrate 106 tre --online --migration_network 10.1.2.0/24
```

Migration type `secure` (default) tunnels over SSH. `insecure` sends guest RAM unencrypted, which can leak secrets such as passwords or keys to anyone eavesdropping, so use it only on a network you fully control. It can be faster on 10 Gbit and above where encryption costs CPU, although AES hardware support reduces the penalty. Storage migration ignores this setting and always uses a secure channel.

Live migration needs CPUs from the same vendor on both nodes for reliable results. A cluster cold start works as follows: at node boot the `pve-guests` service waits for quorum, then starts guests with the `onboot` flag, so guest startup is delayed until quorum exists, which a UPS helps avoid losing in the first place.

## Checked

2026-11-03. Commands, option names, defaults, limits and behaviour claims were compared with the official Proxmox VE documentation pages: https://pve.proxmox.com/pve-docs/chapter-pvecm.html (plus the chapter-qm, qm.1, pct, pvecm, pvesm, vzdump, pvesr and sysadmin pages). Items shown as placeholder or example values (file names, VM IDs, device names) are illustrative. Figures that the pages did not state were removed or reworded.

Method: documentation only; no commands were run.
