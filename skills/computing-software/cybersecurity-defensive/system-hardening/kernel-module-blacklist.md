---
id: computing-software.cybersecurity-defensive.system-hardening.kernel-module-blacklist
name: kernel-module-blacklist
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [kernel-module-blacklist, modprobe, linux-hardening, usb-storage, cis-benchmarks, attack-surface-reduction]
level: practitioner
status: docs-checked
description: "Block unneeded Linux kernel modules (rare filesystems, protocols, USB storage, FireWire) via modprobe.d install directives, verify, and optionally lock module loading."
sources: ["https://github.com/kmod-project/kmod/blob/master/man/modprobe.d.5.scd", "https://github.com/kmod-project/kmod/blob/master/man/modprobe.8.scd", "https://github.com/torvalds/linux/blob/master/Documentation/admin-guide/sysctl/kernel.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kernel module blacklisting

Linux auto-loads modules on demand: mounting a filesystem image or opening a socket of a rare protocol loads
module code that the host may never otherwise need. Disable what the host does not need.

## Candidate modules to review (choose per host; confirm the list against your benchmark)
- Filesystems: `cramfs`, `freevxfs`, `hfs`, `hfsplus`, `jffs2`, `squashfs`, `udf`.
- Network protocols: `dccp`, `sctp`, `rds`, `tipc`.
- Devices: `usb-storage`, `firewire-core`/`firewire-ohci`, `thunderbolt`.
- Optional: `bluetooth`, `btusb`.

## Configure
Per modprobe.d(5), `blacklist` makes modprobe ignore the module's own internal aliases (the ones that match hardware or other identifiers); it does not stop an explicit `modprobe name`. An `install` command makes modprobe run your command instead of inserting the module, so `/bin/false` makes loading fail (modprobe.d(5) warns that the long-term future of `install` is not assured):
```
# /etc/modprobe.d/hardening.conf
install cramfs /bin/false
blacklist cramfs
install dccp /bin/false
blacklist dccp
install usb-storage /bin/false
blacklist usb-storage
```
Then unload it if loaded (`modprobe -r usb-storage`) and rebuild the initramfs with your distribution's tool if the module could be included there. Module and alias names treat `-` and `_` as interchangeable.

## Verify
```bash
modprobe -n -v dccp        # dry run (-n) with verbose output (-v): expect the install command, not an insertion
lsmod | grep -E 'dccp|usb_storage'   # expected: no output
```

## Lock module loading entirely
- `sysctl kernel.modules_disabled=1` after boot: once set, modules can be neither loaded nor unloaded and the toggle cannot be set back to 0 until reboot (kernel sysctl documentation; generally used with `kexec_load_disabled`). Good
  for appliances with a fixed module set; load everything needed first (systemd unit ordered late).

## Gotchas
- Before blocking a module, check that no mounted filesystem, required device or workload uses it (`lsmod`, `/proc/filesystems`, `findmnt`); blocking a filesystem you need prevents mounting it.
- Configuration management should own the file so manual edits do not drift.

## Verify (overall)
A compliance scan of your chosen benchmark shows the module rules passing, and `modprobe -n -v <module>` shows the install command for each blocked module.

## Checked
Checked 2026-10-25 against the kmod manual pages modprobe.d(5) and modprobe(8) (kmod-project/kmod) and the Linux kernel sysctl documentation (torvalds/linux, kernel.rst). Confirmed: `blacklist` semantics (ignores internal aliases), `install` runs a command instead of inserting the module, `-n`/`-v`/`-r` options, `-`/`_` equivalence, `kernel.modules_disabled` being one-way. Removed unconfirmed claims: CVE history, the CIS module list and CIS check behaviour (the module list is now a review list), snapd/udf/vfat/CNI notes, kernel lockdown and signed-module statement, and distribution initramfs commands.

Method: documentation only; no commands were run.
