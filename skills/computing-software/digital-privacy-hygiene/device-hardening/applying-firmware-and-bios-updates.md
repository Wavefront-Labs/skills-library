---
id: computing-software.digital-privacy-hygiene.device-hardening.applying-firmware-and-bios-updates
name: applying-firmware-and-bios-updates
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, firmware-updates, uefi, bios, fwupd, lvfs, bitlocker, windows, linux]
level: practitioner
status: draft
description: "Apply UEFI/BIOS, SSD and peripheral firmware updates safely on Windows, Linux and Mac, suspending BitLocker first so the update does not trigger recovery."
sources:
  - "https://fwupd.org/"
  - "https://lvfs.readthedocs.io/en/latest/"
  - "https://learn.microsoft.com/en-us/powershell/module/bitlocker/suspend-bitlocker"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Applying firmware and BIOS updates

**Goal:** patch the code that runs below the OS (UEFI, Intel ME/AMD PSP, SSD controller, Thunderbolt,
dock, webcam) without bricking the machine or locking yourself out of encrypted disks.

## Where firmware comes from
| Platform | Channel |
|---|---|
| Mac | Bundled in macOS updates; nothing separate to do. |
| Windows OEM laptop | Windows Update > Advanced options > **Optional updates** (firmware/driver), plus the OEM tool: Lenovo Vantage / Lenovo System Update, Dell Command Update, HP Support Assistant. |
| Linux | `fwupd` pulling from the LVFS (most Dell, Lenovo, HP, Framework, Logitech receivers, many NVMe drives). |
| Custom desktop | Motherboard vendor support page; flash from the UEFI menu (EZ Flash, M-Flash, Q-Flash). |
| Router / NAS / printer | Admin UI "check for update"; turn on auto-update where offered. |

## Linux with fwupd
```bash
fwupdmgr refresh          # pull metadata from LVFS
fwupdmgr get-devices      # what fwupd can see, current versions
fwupdmgr get-updates
fwupdmgr update           # stages capsule updates, reboot to apply
fwupdmgr security         # Host Security ID (HSI) report
```

## Windows: suspend BitLocker first
A UEFI update changes the measurements the TPM checks, so the next boot asks for the 48-digit
recovery key. Before flashing:
```powershell
Suspend-BitLocker -MountPoint "C:" -RebootCount 1
# or: manage-bde -protectors -disable C: -RebootCount 1
```
Windows Update and most OEM tools do this automatically; manual USB/UEFI flashing does not. Have the
recovery key (account.microsoft.com/devices/recoverykey) before you start either way.

## Safety rules
- Laptop on AC power and battery above 50 percent; never interrupt a flash.
- Use only the vendor's image for your exact model; read the release notes for "cannot downgrade" warnings.
- Do not flash beta BIOS on a daily driver.
- A device whose vendor has stopped shipping firmware (common for routers after 3-5 years) is end-of-life:
  plan a replacement.

## Verify
- [ ] `msinfo32` (BIOS Version/Date) or `fwupdmgr get-devices` shows the new version.
- [ ] Machine boots without a BitLocker recovery prompt; protection shows On again (`manage-bde -status`).
- [ ] Router/NAS auto-update enabled.
