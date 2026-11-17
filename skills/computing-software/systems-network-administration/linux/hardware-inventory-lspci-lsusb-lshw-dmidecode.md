---
id: computing-software.systems-network-administration.linux.hardware-inventory-lspci-lsusb-lshw-dmidecode
name: hardware-inventory-lspci-lsusb-lshw-dmidecode
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, hardware-inventory, lspci, lsusb, lshw, dmidecode, lscpu, lsblk, inxi, serial-number, firmware-version, lpic-1, sysadmin]
level: practitioner
status: docs-checked
description: "Inventory a machine's hardware from the shell: PCI and USB devices with drivers, CPU, memory DIMMs, serial numbers and BIOS versions via lspci, lsusb, lshw, dmidecode and lscpu."
sources:
  - https://github.com/pciutils/pciutils/blob/master/lspci.man
  - https://github.com/gregkh/usbutils/blob/master/man/lsusb.8
  - https://github.com/lyonel/lshw/blob/master/src/lshw.1
  - https://manpages.debian.org/trixie/dmidecode/dmidecode.8.en.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Hardware inventory: lspci, lsusb, lshw, dmidecode

**Goal:** answer "what hardware is in this box, which driver drives it, what's the serial
number / BIOS version / free DIMM slot" without opening the case or the BMC.

## 1. PCI devices and drivers
```bash
lspci                                   # all devices
lspci -nnk                              # [vendor:device] IDs + "Kernel driver in use" + modules
lspci -nnk -s 03:00.0                   # one device
lspci -vv -s 03:00.0                    # very verbose: capabilities incl. the PCIe link lines (some detail needs root)
lspci -t                                 # tree-like diagram of buses, bridges and devices
```
No driver in use → missing module/firmware: search the `[vendor:device]` ID.

## 2. USB
```bash
lsusb                                    # Bus/Device, ID vendor:product, name
lsusb -t                                 # tree (-t/--tree)
lsusb -v -d 0403:6001                    # verbose descriptors for one vendor:product (-d)
```

## 3. CPU, memory, firmware (DMI/SMBIOS)
```bash
lscpu                                    # CPU architecture from sysfs and /proc/cpuinfo (on VMs it reflects the guest's view)
dmidecode -t system                      # manufacturer, product, serial number, UUID
dmidecode -s system-serial-number; dmidecode -s bios-version; dmidecode -s bios-release-date
dmidecode -t memory                      # memory devices (DIMM slots)
dmidecode -t baseboard; dmidecode -t chassis
ls /sys/devices/virtual/dmi/id/          # most DMI strings as files (dmidecode(8))
```
In VMs, DMI shows the hypervisor's values.

## 4. Everything at once
```bash
lshw -short                              # class-sorted summary
lshw -class network -class disk -businfo   # -businfo: bus information; -class limits the output
lshw -json > inventory.json              # machine-readable
```
Disks: `lsblk -o` with the columns listed by `lsblk --list-columns`.
Firmware: `fwupdmgr get-devices` shows all devices (fwupdmgr(1)).

## Gotchas
- Run as root for complete output; lspci notes that parts of the PCI configuration space are restricted to root.
- DMI tables are often inaccurate, incomplete or wrong (dmidecode(8) BUGS section); cross-check against the BMC.
- lspci names come from the pci.ids database; `update-pciids` refreshes it.

## Verify
- [ ] Inventory export includes serial, BIOS version, CPU, DIMMs, NICs (with drivers) and disks.
- [ ] Every PCI device you care about shows a "Kernel driver in use".

## Checked
2026-10-27. Checked against the pciutils lspci manual source, usbutils lsusb(8) source, lshw(1) source, util-linux lscpu(1) source, fwupd fwupdmgr(1) source and the Debian trixie dmidecode(8) page (3.6). Confirmed: lspci -t, -v, -vv, -k, -n, -nn, -s, update-pciids and root-only parts of configuration space; lsusb -t and -d and -v; lshw -short, -businfo, -class, -json; dmidecode -t keywords (bios, system, baseboard, chassis, memory), -s keywords including system-serial-number and bios-release-date, /sys/devices/virtual/dmi/id files, and the BUGS statement about inaccurate DMI data; lscpu sources and virtual-hardware caveat; fwupdmgr get-devices. Removed: the PCIe link field names, per-device grep filters and sample output strings, VM product-name examples, inxi, hwinfo, nvme, smartctl, ipmitool remarks and the O.E.M. string, none of which the documents confirm. The linux.die.net and Arch man page links and man7.org links in sources were replaced by upstream or Debian pages.

Method: documentation only; no commands were run.
