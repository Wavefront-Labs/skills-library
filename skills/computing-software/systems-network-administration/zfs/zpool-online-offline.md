---
id: computing-software.systems-network-administration.zfs.zpool-online-offline
name: zpool-online-offline
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, zpool, online, offline, expand, fault, power]
level: practitioner
status: docs-checked
description: "Take ZFS devices offline or online with zpool offline and zpool online: temporary and forced faults, -e expansion, and enclosure power control on Linux."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zpool-offline.8.html
  - https://openzfs.github.io/openzfs-docs/man/master/8/zpool-online.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zpool offline and online

```
zpool offline [--power | [-ft]] pool device...
zpool online [--power] [-e] pool device...
```

## Offline

```
zpool offline tank sda
```

No reads or writes are attempted to an offline device. dRAID spares cannot be offlined; traditional spares only when active.

- `-f`: put the device into a faulted state instead of offline. The fault persists across imports unless `-t` is also given.
- `-t`: temporary; on reboot the device reverts to its previous state. With `-f`, the fault does not persist across imports.
- `--power`: power off the device's slot in the storage enclosure. Linux only; the synopsis lists it as an alternative to `-f -t`.

## Online

```
zpool online tank sda
zpool online -e tank sda
```

Brings a physical device online. It does not apply to spares.

- `-e`: expand the device to use all available space. For a device in a mirror or raidz, every device in that vdev must be expanded before the new space becomes available to the pool.
- `--power`: power on the device's slot and wait for the device to appear before onlining. Linux only. Setting `ZPOOL_AUTO_POWER_ON_SLOT` enables this every time.

## Checked

2026-11-03. Pages read: zpool-offline(8) (also served as zpool-online(8)).

Confirmed: synopsis, -f, -t, --power on Linux only, spare restrictions, online -e, ZPOOL_AUTO_POWER_ON_SLOT.

Removed or corrected: the offline-before-pulling advice, which the page does not give.

Method: documentation only; no commands were run.
