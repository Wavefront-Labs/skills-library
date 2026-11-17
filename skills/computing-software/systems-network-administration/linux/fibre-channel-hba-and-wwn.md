---
id: computing-software.systems-network-administration.linux.fibre-channel-hba-and-wwn
name: fibre-channel-hba-and-wwn
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, fibre-channel, fc-hba, wwn, wwpn, fc-host, san-zoning, lip, lpfc, qla2xxx, systool, lpic-2, sysadmin]
level: practitioner
status: docs-checked
description: "Work with Fibre Channel HBAs on Linux: find WWPNs for zoning, check port state and speed in sysfs, rescan for new LUNs (LIP), driver/firmware checks, and removing LUNs cleanly."
sources:
  - https://docs.kernel.org/scsi/scsi_fc_transport.html
  - https://man.archlinux.org/man/lsscsi.8
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Fibre Channel HBAs and WWNs

**Goal:** give the SAN team the right WWPNs, confirm links are up, and see which targets and LUNs the host has.

## 1. Identify HBAs and WWNs
```bash
ls /sys/class/fc_host/                     # host5 host6 ...
for h in /sys/class/fc_host/host*; do
  echo "$h  WWPN=$(cat $h/port_name)  WWNN=$(cat $h/node_name)  state=$(cat $h/port_state)"
done
```
The kernel FC transport class exposes `node_name` (WWNN), `port_name` (WWPN) and `port_state` per host under
`/sys/class/fc_host/`, and link speed as a per-port attribute. Zoning uses the **WWPN** (`port_name`). Read `port_state`
before blaming the array: a link-down state points at cable, SFP or switch port.

## 2. Remote ports (targets) and LUNs
```bash
ls /sys/class/fc_remote_ports/             # rport entries
cat /sys/class/fc_remote_ports/rport-*/port_name   # target WWPNs visible to this host
lsscsi -t                                  # LUNs, with FC transport shown as fc:<wwpn>
```
`lsscsi -t` (`--transport`) prefixes FC devices with `fc:` (or `fcoe:` for FCoE). A missing target WWPN is a zoning or
array host-group question, not a Linux one.

## 3. Rescan, remove LUNs, timeouts
Rescan, LIP and LUN-removal steps, and FC timeout settings, differ by distro and array vendor: follow the
storage-device chapter of your distribution's documentation and the array vendor's host guide. Unmount and deactivate
LVM before removing a LUN, and have the SAN team unmap it only after the host side is clean.

## Gotchas
- Changing HBAs changes WWPNs: re-zone and update host groups.
- Boot-from-SAN hosts need the HBA driver in the initramfs.

## Verify
- [ ] All fc_host ports report an online `port_state`; target WWPNs visible in `fc_remote_ports`.
- [ ] New LUN appears in `lsscsi` on every path.

## Checked
2026-10-28. Confirmed in the Linux kernel FC transport documentation and the lsscsi man page: `node_name`, `port_name`,
`port_state`, `/sys/class/fc_host/`, `/sys/class/fc_remote_ports/`, rport naming, `lsscsi --transport` and the `fc:`
prefix. Removed as unconfirmed (the Red Hat storage chapter in `sources` returned 404 and was dropped): `issue_lip`,
scan and delete sysfs commands, `rescan-scsi-bus.sh`, `systool`, driver and firmware attribute paths, `dev_loss_tmo`
and `fast_io_fail_tmo`, state value names and the `fabric_name` attribute.
Method: documentation only; no commands were run.
