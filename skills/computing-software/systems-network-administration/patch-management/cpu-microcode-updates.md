---
id: computing-software.systems-network-administration.patch-management.cpu-microcode-updates
name: cpu-microcode-updates
category: computing-software
field: systems-network-administration
product: patch-management
tags: [microcode, cpu-microcode, intel-microcode, amd64-microcode, spectre-mitigations, firmware-patching, linux]
level: advanced
status: docs-checked
description: "Keep CPU microcode current on Linux, Windows and hypervisors: early-load packages, BIOS-delivered updates, checking loaded revisions and vulnerability status, and late-load risks."
sources:
  - https://docs.kernel.org/arch/x86/microcode.html
  - https://docs.kernel.org/admin-guide/hw-vuln/index.html
  - https://docs.kernel.org/admin-guide/hw-vuln/spectre.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CPU microcode updates

**Goal:** CPUs run vendor microcode that carries fixes for hardware vulnerabilities and errata.

## Delivery paths
1. **System firmware (BIOS/UEFI) updates**: durable, applies before any OS; the primary route on servers.
2. **OS early loading**: microcode bundled into the initramfs and applied at boot.
   - Linux: install the microcode packages your distribution supplies (package names and repositories differ by distribution); the kernel looks for blobs in `/lib/firmware/intel-ucode` and `/lib/firmware/amd-ucode`.
   - Windows and hypervisors: check the vendor's update documentation for microcode delivery.
3. **Late loading** (`echo 1 > /sys/devices/system/cpu/microcode/reload` as root): the kernel documentation has a section on why late loading is dangerous (all CPUs and SMT threads must be synchronised), and since kernel 5.19 it is not enabled by default.

## Check what is running
```bash
grep -m1 microcode /proc/cpuinfo          # revision
dmesg | grep -i microcode                  # early-load messages
grep . /sys/devices/system/cpu/vulnerabilities/*
```
The `vulnerabilities` files report per-issue status such as "Not affected" or "Mitigation: ..." (kernel hardware-vulnerability documentation). For Windows hosts use the vendor's firmware inventory tooling.

## Process
- Track vendor security advisories (Intel SA, AMD SB) for affected CPU families.
- Update firmware through vendor tools in rolling cluster maintenance; OS packages provide coverage between firmware cycles.
- Early loading reads microcode from an initrd, so after updating the package make sure the initramfs is regenerated (normally the package does this) and reboot.

## Gotchas
- Check your hypervisor vendor's documentation before mixing microcode revisions in one cluster.

## Verify
All hosts in a cluster report the same target revision, and `vulnerabilities/*` show "Mitigation" rather than "Vulnerable".

## Checked

Checked 2026-10-27 against the Linux kernel x86 microcode documentation and the Spectre hardware-vulnerability page.
- Early loading from an initrd, blob location under `/lib/firmware/{intel-ucode,amd-ucode}`, late loading via `/sys/devices/system/cpu/microcode/reload`, "late loading is not enabled by default since 5.19", and the section on why late loading is dangerous: confirmed.
- `/sys/devices/system/cpu/vulnerabilities/*` status strings: confirmed.
- Removed unconfirmed: distribution package names, the Windows registry value, the exact dmesg and cpuinfo output, and the initramfs rebuild commands (the Debian wiki page could not be read).
Method: documentation only; no commands were run.
