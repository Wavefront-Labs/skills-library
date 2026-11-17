---
id: computing-software.systems-network-administration.virtualisation.proxmox-vm-migration-between-nodes
name: proxmox-vm-migration-between-nodes
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [qm-migrate, pve-migration, live-migration, migration-network, with-local-disks, bulk-migrate, remote-migrate, proxmox, proxmox-ve]
level: practitioner
status: docs-checked
description: "Migrate Proxmox guests: online and offline qm migrate, local-disk migration, dedicated insecure migration network, bulk migrate, remote cross-cluster migration and common failures."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-qm.html#qm_migration
  - https://pve.proxmox.com/pve-docs/qm.1.html
  - https://pve.proxmox.com/pve-docs/datacenter.cfg.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating VMs and containers between Proxmox nodes

**Goal:** move guests between nodes (and clusters) with no or minimal downtime.

## Within a cluster
```sh
qm migrate 120 pve2 --online                          # shared storage: memory only
qm migrate 120 pve2 --online --with-local-disks       # enables live storage migration of local disks
qm migrate 120 pve2 --online --with-local-disks --targetstorage local-zfs   # map source storages to the target storage
pct migrate 200 pve2 --restart                        # containers: restart migration
```
The web interface defaults to live migration for a running VM. A running container cannot be live-migrated; a restart migration shuts it down (default timeout 180 seconds), moves it and starts it again.

## Migration network
Cluster-wide setting in the datacenter options (`/etc/pve/datacenter.cfg`): `migration: type=<secure|insecure>,network=<CIDR>`. `secure` (the default) encrypts migration traffic with an SSH tunnel; `insecure` can be used on secure, completely private networks to increase performance. `qm migrate` also accepts `--migration_type` and `--migration_network`. Example: `migration: type=insecure,network=10.70.0.0/24`.

## Remote migration (between clusters, experimental)
```sh
qm remote-migrate 120 520 'host=<target>,apitoken=PVEAPIToken=<user>@<realm>!<token>=<secret>,fingerprint=<fp>' \
  --target-bridge vmbr0 --target-storage local-lvm --online
```

## Common failures
| Error | Cause / fix |
|---|---|
| Local disks | Use `--with-local-disks` for live migration, or move the disk to shared storage; offline migration copies local disks as long as the storage is defined on both hosts |
| CPU flag errors / guest crash after move | CPU type `host` across different CPUs; use a generic model, and keep hosts to the same CPU vendor with similar capabilities |
| Passthrough devices | PCI or USB passthrough blocks live migration; offline only, and the passthrough config may need adapting to the target |
| Version mismatch | The target must run the same or a newer version of the Proxmox VE packages; the other direction may work but is not guaranteed |

## Gotchas
- Live migration copies memory repeatedly while the guest runs and pauses it only for a final small difference; the hosts need a reliable network connection and must be in the same cluster (use remote migration across clusters).
- Conntrack state migration for the firewall is best-effort and likely fails with source NAT on the host.
- HA-managed guests: migrate via HA with `ha-manager migrate vm:120 pve2` (an alias for `ha-manager crm-command migrate`).

## Verify
Guest runs on the target (`qm list` there), connectivity returns without a reboot, and the task log shows the migration completed.

## Checked

2026-10-26 against the Proxmox VE admin guide sources (github.com/proxmox/pve-docs master, last commit 2026-10-17: qm.adoc Migration sections, pct.adoc Migration, generated qm.1-synopsis.adoc migrate and remote-migrate, datacenter.cfg.5-opts.adoc migration, ha-manager synopsis) and confirmed the --online, --with-local-disks, --targetstorage, --migration_type and --migration_network options, the datacenter migration option and its secure default, the live-migration requirements, the remote-migrate endpoint format and its experimental status, the container restart migration and the ha-manager migrate alias. Removed the unconfirmed 7.3 gate, local CD/DVD, local snapshot and bulk migrate claims.

Method: documentation only; no commands were run.
