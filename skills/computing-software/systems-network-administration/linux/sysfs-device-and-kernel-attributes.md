---
id: computing-software.systems-network-administration.linux.sysfs-device-and-kernel-attributes
name: sysfs-device-and-kernel-attributes
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, sysfs, sys-class, sys-block, device-attributes, module-parameters, udev, kernel-objects, lpic-1, lpic-2, sysadmin]
level: practitioner
status: docs-checked
description: "Read and change device and driver state through /sys: block queue settings, network device stats, module parameters, rescan/remove controls, and persisting changes."
sources:
  - https://www.kernel.org/doc/html/latest/filesystems/sysfs.html
  - https://github.com/torvalds/linux/blob/master/Documentation/ABI/stable/sysfs-block
  - https://github.com/torvalds/linux/blob/master/Documentation/ABI/testing/sysfs-class-net
  - https://github.com/torvalds/linux/blob/master/Documentation/ABI/testing/sysfs-bus-pci
  - https://github.com/torvalds/linux/blob/master/Documentation/ABI/testing/sysfs-class-power
  - https://www.kernel.org/doc/html/latest/admin-guide/mm/transhuge.html
  - https://github.com/systemd/systemd/blob/main/man/tmpfiles.d.xml
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# sysfs: device and kernel attributes

**Goal:** query and tune hardware/driver settings that have no dedicated tool, and know how to
make those changes survive reboot.

## 1. Layout
- `/sys/devices/` — a filesystem representation of the device tree; `/sys/bus/*/devices` and `/sys/class` hold symlinks to it.
- `/sys/class/<class>/` — devices grouped by function (for example `net`, `block`, `power_supply`).
- `/sys/block/` — block devices; `/sys/bus/<bus>/devices|drivers/`; `/sys/module/<mod>/parameters/`.
- Attributes are text files, preferably with one value each; read with `cat`, write with `echo` (root).
```bash
grep -r . /sys/class/net/eth0/statistics/ 2>/dev/null | sed 's|.*/||'   # quick dump name:value
```

## 2. Useful attributes
```bash
cat /sys/block/sda/queue/{rotational,scheduler,nr_requests,read_ahead_kb,logical_block_size,physical_block_size}
echo mq-deadline > /sys/block/sda/queue/scheduler       # choose among the schedulers listed by 'cat'
cat /sys/class/net/eth0/{operstate,speed,duplex,carrier_changes}
cat /sys/class/net/eth0/device/numa_node
cat /sys/class/power_supply/BAT0/capacity
echo 1 > /sys/bus/pci/devices/0000:03:00.0/remove; echo 1 > /sys/bus/pci/rescan   # hot-remove/rescan PCI
cat /sys/kernel/mm/transparent_hugepage/enabled
```
Parameters under `/sys/module/<mod>/parameters/` are only writable if the module exposes them as such;
others need `modprobe.d` options and a module reload or reboot.

## 3. Make changes persistent
sysfs resets at boot. Options, best first:
1. A purpose-built mechanism: a udev rule with `ATTR{queue/scheduler}="bfq"` (applies on device add, also for hotplugged
   devices), `modprobe.d` options for module parameters.
2. `systemd-tmpfiles`: a `w` line (`w /sys/kernel/mm/transparent_hugepage/enabled - - - - madvise`) in
   `/etc/tmpfiles.d/thp.conf`.
Avoid rc.local hacks.

## Gotchas
- Paths under `/sys/class` are symlinks; device paths change with topology — match in udev rules by attributes, not paths.
- Writes can fail (for example with `EINVAL` or `EBUSY`); check the exit status or read the value back.

## Verify
- [ ] Read back the value after writing (`cat` shows the new setting, e.g. `[bfq]`).
- [ ] After reboot (and after hot-plugging the device), the persistent mechanism re-applied it.

## Checked

2026-10-26. Linux kernel documentation (torvalds/linux master, 2026-10): sysfs.rst (one value per attribute file), ABI entries for block queue attributes (rotational, scheduler, read_ahead_kb, nr_requests, logical and physical block size), net operstate, speed, duplex and carrier_changes, PCI remove and rescan, power_supply capacity, transparent_hugepage/enabled; systemd tmpfiles.d(5) w line type. Removed the thermal, SCSI rescan and delete, nvme_core, tuned and sysfsutils lines and the speculative gotcha about unused devices, which were not confirmed. The mtu, address and carrier checks were reduced to documented attributes.

Method: documentation only; no commands were run.
