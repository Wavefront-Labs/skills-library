---
id: computing-software.systems-network-administration.linux.dm-multipath-configuration
name: dm-multipath-configuration
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, multipath, multipath-conf, multipathd, device-mapper-multipath, mpathconf, wwid, user-friendly-names, san, iscsi, lpic-2, sysadmin]
level: practitioner
status: docs-checked
description: "Configure device-mapper multipath for SAN/iSCSI LUNs: mpathconf, multipath.conf defaults/blacklist/devices/multipaths, aliases by WWID, path checking and failover verification."
sources:
  - https://github.com/opensvc/multipath-tools/blob/master/multipath/multipath.conf.5.in
  - https://github.com/opensvc/multipath-tools/blob/master/multipath/multipath.8.in
  - https://github.com/opensvc/multipath-tools/blob/master/multipathd/multipathd.8.in
  - https://github.com/dracut-ng/dracut-ng/blob/main/man/dracut.8.adoc
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# dm-multipath: multipath.conf and multipathd

**Goal:** one stable device per LUN (`/dev/mapper/<alias>`) that survives losing any single
path (HBA, cable, switch, controller), with I/O spread across active paths.

## 1. Enable
```bash
# install the distribution's multipath package and create /etc/multipath.conf (package names and helper tools are distribution-specific)
multipath -ll                           # show topology from sysfs, device mapper and path checkers
```

## 2. multipath.conf
```
defaults {
    user_friendly_names yes
    find_multipaths     yes          # on: a device needs 2+ paths or an entry in the wwids file (the built-in default is strict)
}
blacklist {
    devnode "^(ram|zram|loop|fd|md|dm-|sr|scd|st)[0-9]*"   # the built-in default blacklist is "!^(sd[a-z]|dasd[a-z]|nvme[0-9])"
    wwid "3600508b1001c5a1d…"          # local boot disk
}
devices {
    device {                        # only if vendor docs say so — built-in defaults cover most arrays
        vendor "NETAPP"
        product "LUN.*"
        path_grouping_policy group_by_prio
        prio alua
        failback immediate
        no_path_retry 12
    }
}
multipaths {
    multipath {
        wwid  3600a098038303053743f4d4a6b2f4f41
        alias db_data
    }
}
```
`multipath -t` displays the currently used configuration; `multipath -T` limits it to devices actually present (usable as a template for multipath.conf). After edits: `multipathd reconfigure` (rereads the config and reloads changed maps), or `multipath -r` to force a reload of all maps.

## 3. Key behaviours
- `no_path_retry`: what to do when **all** paths are down — a number of retries before I/O queueing is disabled, `fail` (default, no queueing) or `queue` (queue forever, like `queue_if_no_path`; can hang processes and shutdown, see KNOWN ISSUES in multipath.conf(5)).
- ALUA arrays: `group_by_prio` creates one priority group per ALUA target port group and requires `prio alua` on all paths.
- WWIDs seen as multipath devices are remembered in the wwids file; with `user_friendly_names yes` the bindings file assigns persistent `mpathN` names. An alias in `multipaths` overrides both.

## 4. Use the maps, not paths
Filesystems/LVM must use `/dev/mapper/db_data` (or `mpathX`), never `sdX`. LVM filter:
accept `/dev/mapper/mpath.*`/aliases, reject `sd*` (see LVM filter skill). With dracut, add the multipath module to the initramfs (`dracut -f --add multipath`) when the root/boot disk is multipathed.

## 5. Operations
```bash
multipathd show paths format "%d %w %t %T %s"     # dev, wwid, dm state, checker state, vendor/product/revision
multipathd show maps topology
multipathd resize map db_data                     # after LUN growth + path rescans
multipath -f db_data                              # flush (remove) an unused map before unmapping LUN
```

## Gotchas
- Flush the map (`multipath -f`) and remove the path devices before unmapping a LUN on the array; with queueing enabled, I/O to a vanished LUN can hang.
- `find_multipaths yes` on a fresh single-path setup → no map created; add the WWID (`multipath -a <wwid>`) or set up the map manually with `multipathd add map`.
- A `devices` entry overrides the built-in hardware table entry for that vendor/product; check `multipath -t` before adding one.

## Verify
- [ ] `multipath -ll` shows every expected path `active ready running`.
- [ ] Fail one path (`multipathd fail path sdX`, or disable a switch port in a window): I/O continues; `multipathd reinstate path sdX` (or the checker) returns it.

## Checked

Checked against multipath-tools master (multipath/multipath.conf.5.in dated 2026-06-13, multipath/multipath.8.in, multipathd/multipathd.8.in; repository last pushed 2026-09-02) and dracut-ng modules.d (70multipath module, `--add`).
Confirmed: `find_multipaths` values and default (strict; yes is an alias for on); `no_path_retry` values and default (fail); default blacklist and blacklist_exceptions; `group_by_prio` and `prio alua`; `user_friendly_names` default no and bindings file; `multipath -t` versus `-T`; `-f`, `-r`, `-a`; `multipathd` commands `show paths format`, `show maps topology`, `resize map`, `reconfigure`, `fail path`, `reinstate path`, `add map`; format wildcards %d %w %t %T %s.
Fixed: the skill said `-T` prints only non-defaults; the man page says it limits output to devices actually present. Removed unconfirmed claims: mpathconf and package names, `systemctl reload multipathd`, sysfs offline/delete commands, and the claim that aliases are the only cluster-safe names.

Method: documentation only; no commands were run.
