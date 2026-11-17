---
id: computing-software.systems-network-administration.linux.lvm-conf-device-filters
name: lvm-conf-device-filters
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, lvm, lvm-conf, lvm-filter, global-filter, devices-file, lvmdevices, multipath-lvm, duplicate-pv, lpic-2, sysadmin]
level: practitioner
status: docs-checked
description: "Control which block devices LVM scans: the RHEL 9 devices file (lvmdevices), filter/global_filter in lvm.conf, and fixing duplicate-PV warnings from multipath or cloned disks."
sources:
  - https://github.com/lvmteam/lvm2/blob/main/man/lvmdevices.8_pregen
  - https://github.com/lvmteam/lvm2/blob/main/man/lvm.conf.5_main
  - https://github.com/lvmteam/lvm2/blob/main/conf/example.conf.in
  - https://github.com/lvmteam/lvm2/blob/main/man/vgimportclone.8_pregen
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LVM device filters and the devices file

**Goal:** LVM uses exactly the intended devices — not multipath member paths, not a VM
guest's disks seen through a host LV, not a cloned snapshot with duplicate UUIDs.

## 1. Devices file (lvm2 2.03.12 and later)
```bash
lvmconfig devices/use_devicesfile        # 1 = enabled (the default is set at build time by the distribution)
lvmdevices                               # list: IDTYPE (sys_wwid, wwid_naa, sys_serial, devname…), IDNAME, DEVNAME, PVID
lvmdevices --adddev /dev/sdc1            # allow a device (pvcreate/vgcreate/vgextend add automatically)
lvmdevices --deldev /dev/sdc1
vgimportdevices vg_data                  # add all PVs of an existing VG (e.g. disks moved from another host)
lvmdevices --check / --update            # fix stale entries after device renames
```
File: `/etc/lvm/devices/system.devices`. A disk not listed is **ignored** — the classic
"I attached the old disk and `vgs` doesn't show it" when the devices file is in use. Use `--devicesfile ""` once to
scan everything: `pvs --devicesfile ""`.

## 2. filter / global_filter (classic)
```ini
# /etc/lvm/lvm.conf  devices { }
global_filter = [ "a|^/dev/mapper/mpath.*|", "a|^/dev/sda[0-9]*$|", "r|.*|" ]
```
- Regexes, first match wins; `a` accept, `r` reject. End with `"r|.*|"` for allow-lists.
- Devices rejected by `global_filter` are not opened by any LVM system component (such as udev-driven
  activation); `filter` is for commands only. Prefer `global_filter` to hide devices system-wide.
- With the devices file in use, lvm commands ignore the `lvm.conf` filter (except `vgimportdevices`, which applies it
  when looking for VGs to import). Filters take effect again when the devices file is disabled.
Check: `lvmconfig --type full devices/global_filter`.

## 3. Common cases
- **Multipath:** accept only `/dev/mapper/mpath*` (and local boot disk), reject `sd*` paths;
  `multipath_component_detection=1` (default) also helps. Otherwise "Found duplicate PV …
  using /dev/sdc not /dev/sdb" and I/O bypasses multipath.
- **Hypervisor hosts:** reject guest LVs (`r|^/dev/vg_vms/.*|`) so the host doesn't activate VGs inside VM disks.
- **Cloned disks/snapshots attached to same host:** duplicate PV UUIDs — use
  `vgimportclone --basevgname vg_clone /dev/sdd1` to give the copy new UUIDs and name.

## 4. After changes
If your initramfs embeds a copy of `lvm.conf` or the devices file, regenerate it with your distribution's tool (distribution-specific; see its initramfs documentation).

## Gotchas
- Over-strict filters can hide the root PV. Test with `pvs` before rebooting.
- Device names (`sdX`) aren't stable — devices file uses WWID/serial for this reason.

## Verify
- [ ] `pvs` lists every expected PV once, with no duplicate warnings.
- [ ] `lvmdevices` (or the filter) contains only intended devices; reboot tested.

## Checked

Checked against the lvm2 main branch (lvmdevices(8) pregen, conf/example.conf.in, vgimportclone(8), WHATS_NEW), repository last pushed 2026-10-09.
Confirmed: devices file introduced in 2.03.12; `--check`, `--update` and `--devicesfile ""`; IDTYPE names; `multipath_component_detection = 1`; `vgimportclone --basevgname`; the filter semantics of `global_filter`.
Fixed: with the devices file in use, the lvm.conf filter is ignored (the skill said filters apply on top); IDTYPE is `sys_wwid`/`wwid_naa`, not `wwid`; lvmetad was removed in 2.03.00. Removed unconfirmed claims: the RHEL 9 default and the dracut/lsinitrd initramfs steps.

Method: documentation only; no commands were run.
