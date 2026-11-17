---
id: computing-software.systems-network-administration.proxmox-ve.cpu-microcode-and-firmware-updates
name: cpu-microcode-and-firmware-updates
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [microcode, firmware, intel-microcode, amd64-microcode, fwupd]
level: practitioner
status: docs-checked
description: "Apply CPU microcode through BIOS or early OS updates on a Proxmox VE host and verify the running revision."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-sysadmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Firmware has two layers: persistent firmware (BIOS/UEFI microcode and device firmware, applied via the vendor tools) and runtime firmware files passed to devices by the OS. The `pve-firmware` package is installed by default and stays current through normal apt updates. Proxmox ships its own `fwupd` with Secure Boot support.

Early OS microcode updates are the convenient route, especially when the board vendor no longer ships BIOS updates. This applies to x86 only. Steps:

1. Enable the Debian firmware repository (`non-free-firmware` component).
2. `apt update`
3. `apt install intel-microcode` or `apt install amd64-microcode`
4. Reboot. Every later microcode update also needs a reboot.

Check the running revision and whether early loading happened:

```
grep microcode /proc/cpuinfo | uniq
dmesg | grep microcode
```

A "microcode updated early" log line appears only if the package microcode is newer than both the CPU and BIOS versions. `lscpu` lists vulnerabilities and mitigations.

To debug, boot once without the update: in GRUB press E on the entry, append `dis_ucode_ldr` to the `linux` line and press CTRL-X. If a new microcode is suspect, prefer downgrading the package (`apt list -a intel-microcode`, then `apt install intel-microcode=VERSION`, then `apt-mark hold intel-microcode`) over `apt purge`, because purging can leave an older persisted microcode in effect. Unhold and update later.

## Checked

2026-11-09. Compared with the Firmware Updates and Early OS Microcode Updates sections of https://pve.proxmox.com/pve-docs/chapter-sysadmin.html: package names, repository component, verification commands, dis_ucode_ldr steps and the downgrade and hold advice all match.

Method: documentation only; no commands were run.

