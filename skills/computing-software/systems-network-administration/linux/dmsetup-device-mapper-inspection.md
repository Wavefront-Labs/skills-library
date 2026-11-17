---
id: computing-software.systems-network-administration.linux.dmsetup-device-mapper-inspection
name: dmsetup-device-mapper-inspection
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, dmsetup, device-mapper, dm-table, lvm, luks, multipath, stuck-device]
level: advanced
status: docs-checked
description: "Inspect and repair device-mapper stacks with dmsetup: ls --tree, info/table/status, mapping dm-N to names, removing stale or stuck mappings, and suspend/resume caveats."
sources:
  - https://github.com/lvmteam/lvm2/blob/main/man/dmsetup.8_main
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dmsetup

device-mapper underlies LVM, LUKS, multipath, thin pools, VDO and dm-cache. When higher-level tools get confused, dmsetup shows what the kernel actually has.

## Inspect
```bash
dmsetup ls --tree                     # dependencies between devices as a tree
dmsetup info -c                       # name, major:minor, attributes (live/inactive/suspended/read-only), open count, UUID
dmsetup table vg-root                 # mapping: start length target args (linear/striped/crypt/thin/multipath)
dmsetup status vg-thinpool-tpool      # target status (use --noflush to avoid committing thin-pool metadata)
lsblk                                 # dm-N ↔ name
```
Real encryption keys are suppressed in `dmsetup table` output for crypt and integrity targets unless `--showkeys` is given — never paste `--showkeys` output anywhere.

## Stale mappings
"Device or resource busy" when removing a VG/LUN, or leftover `mpathb`/`luks-...` after the disk is gone:
```bash
dmsetup info -c vg_old-lv_data        # Open count > 0? find holders:
dmsetup remove vg_old-lv_data
dmsetup remove --force vg_old-lv_data # open device: replaces the table with one that fails all I/O, then removes it
dmsetup remove --retry vg_old-lv_data  # retry for a few seconds (a quick udev rule may briefly hold the device)
dmsetup remove --deferred vg_old-lv_data   # remove when the last user closes it
```
Prefer the owning tool first (`lvchange -an`, `cryptsetup close`, `multipath -f`) — dmsetup bypasses their metadata.

## Suspended devices
A device left `SUSPENDED` (for example by a crashed lvm command) has its I/O postponed. `dmsetup resume <name>` un-suspends it (an inactive table, if loaded, becomes live and postponed I/O is re-queued) — then investigate why it was suspended.

## Gotchas
- `dmsetup suspend` syncs the filesystem first unless `--nolockfs` is given and flushes outstanding I/O unless `--noflush` is given; do not suspend the device holding the root filesystem interactively.
- LVM builds dm names from the VG name, LV name and any internal layer joined with a hyphen, and doubles any hyphens inside the names (`vg--a-lv`); the encoding may change in future versions.

## Verify
- [ ] `dmsetup ls --tree` matches `lsblk`; no SUSPENDED devices.

## Checked

Checked against the lvm2 main branch man/dmsetup.8_main (repository last pushed 2026-10-09).
Confirmed: `ls --tree`, `info -c`, `table --showkeys` key suppression, `remove` with `--force` (table replaced by one that fails all I/O), `--retry` and `--deferred`, `resume`, `suspend` with `--nolockfs`/`--noflush`, and the hyphen-doubling rule for LVM names.
Removed unconfirmed claims: UUID prefixes other than what the man page states, sample output, the /sys holders and fuser lookups, the D-state remark and the udevadm settle check.

Method: documentation only; no commands were run.
