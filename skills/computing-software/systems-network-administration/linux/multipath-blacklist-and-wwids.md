---
id: computing-software.systems-network-administration.linux.multipath-blacklist-and-wwids
name: multipath-blacklist-and-wwids
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, multipath, multipath-blacklist, wwids, user-friendly-names, multipath-conf, local-disk-exclusion]
level: advanced
status: docs-checked
description: "Control which devices dm-multipath claims: find_multipaths policy, blacklist and blacklist_exceptions by WWID/vendor, /etc/multipath/wwids, user_friendly_names and aliases."
sources:
  - https://github.com/opensvc/multipath-tools/blob/master/multipath/multipath.conf.5.in
  - https://github.com/opensvc/multipath-tools/blob/master/multipath/multipath.8.in
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# multipath blacklist, wwids and names

## Starting point
Create `/etc/multipath.conf` with your distribution's helper (distribution-specific), then review `find_multipaths`. It decides whether a single-path disk gets claimed: `strict` (default) uses only WWIDs already in the wwids file; `on` (alias `yes`) also accepts a device once 2+ non-blacklisted paths with the same WWID are seen; `smart` also treats a first single path as multipath until a timeout; `greedy` claims every non-blacklisted device; `off` (alias `no`) behaves like strict for multipath and greedy for multipathd.

## Blacklist local disks explicitly
```
# /etc/multipath.conf
blacklist {
    wwid "3600508b1001c5a6f2c5d9e2a1b3c4d5e"       # local RAID volume
    devnode "^(ram|zram|loop|fd|md|dm-|sr|scd|st)[0-9]*"
    device { vendor "QEMU" product ".*" }
}
blacklist_exceptions {
    property "(SCSI_IDENT_|ID_WWN)"
}
multipaths {
    multipath { wwid 360000970000197600357533030303842  alias oradata01 }
}
```
Get WWIDs: `multipath -d -v3 2>/dev/null` lists the WWIDs of devices present in the system.
Apply: `multipathd reconfigure`, then `multipath -ll`. The default blacklist is `devnode "!^(sd[a-z]|dasd[a-z]|nvme[0-9])"` and the default blacklist exception is `property "(SCSI_IDENT_|ID_WWN)"`.

## /etc/multipath/wwids
Records WWIDs that have been multipathed (in the state directory, normally `/etc/multipath/wwids`); `multipath -a <device>` adds, `multipath -w <device>` removes, `multipath -W` resets the file to the current multipath devices.
The initramfs needs the same config if root/boot is on SAN; with dracut add the multipath module (`dracut -f --add multipath`).

## Names
`user_friendly_names yes` → `mpatha` (persistent names assigned from the bindings file in the state directory, normally `/etc/multipath/bindings`; default is no, which uses the WWID). An alias in the `multipaths` section overrides both and is the name to use in fstab (`/dev/mapper/oradata01`).

## Gotchas
- Mounting `/dev/sdX` of a multipathed LUN bypasses failover — always use `/dev/mapper/<name>`.
- LVM on multipath: multipath's udev rules keep devices that are valid multipath paths away from upper layers such as LVM; also restricting LVM to `/dev/mapper/` devices (filter or devices file) avoids duplicate-PV warnings.

## Verify
- [ ] `multipath -ll` lists only SAN LUNs with expected names; `lsblk` shows local disks without `mpath` children.

## Checked

Checked against multipath-tools master (multipath/multipath.conf.5.in dated 2026-06-13, multipath/multipath.8.in; repository last pushed 2026-09-02) and dracut-ng modules.d.
Confirmed: `find_multipaths` values, aliases and default; `blacklist` keywords (devnode, wwid, device with vendor/product, property) and `blacklist_exceptions`; default blacklist and exception; `multipath -a`, `-w`, `-W`, `-d -v3`; `multipathd reconfigure`; `user_friendly_names` and bindings; `alias` overrides.
Removed unconfirmed claims: mpathconf, `scsi_id`, `systemctl reload multipathd`, and the requirement that bindings be identical across cluster nodes.

Method: documentation only; no commands were run.
