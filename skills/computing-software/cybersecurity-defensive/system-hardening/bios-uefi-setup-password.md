---
id: computing-software.cybersecurity-defensive.system-hardening.bios-uefi-setup-password
name: bios-uefi-setup-password
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [bios-password, uefi-password, firmware-security, boot-order-lock, dell-command-configure, hp-bcu]
level: practitioner
status: draft
description: "Set and manage BIOS/UEFI setup (supervisor) passwords at fleet scale: unique per device, vendor tools for Dell, HP and Lenovo, boot order lock, escrow and rotation."
sources: ["https://www.dell.com/support/kbdoc/en-us/000177240/dell-command-configure", "https://ftp.ext.hp.com/pub/caps-softpaq/cmit/whitepapers/BIOS_Configuration_Utility_User_Guide.pdf", "https://docs.lenovocdrt.com/guides/tbct/", "https://learn.microsoft.com/en-us/mem/intune/configuration/device-firmware-configuration-interface-windows"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# BIOS and UEFI setup password

Without a firmware setup (admin/supervisor) password, anyone with brief physical access can disable Secure
Boot, enable boot from USB, turn off TPM, or reset security settings, defeating disk encryption protections
and boot integrity.

## What to set
- **Setup/administrator password** (protects configuration). Required.
- **Power-on/user password**: usually not, if BitLocker/LUKS with TPM+PIN or pre-boot authentication is used;
  it adds help-desk load.
- With the password set, lock: boot order (internal disk first), disable USB/PXE boot unless required, Secure
  Boot on, TPM on, disable legacy/CSM boot, disable Thunderbolt pre-boot DMA where relevant (or Kernel DMA
  Protection on), "lock BIOS settings" options.

## Fleet tooling
- **Dell**: Dell Command | Configure (`cctk --SetupPwd=<new> --ValSetupPwd=<old>`, `cctk --BootOrder`, export
  packages), or Intune/ConfigMgr integration; Dell Client Device Manageability via WMI.
- **HP**: BIOS Configuration Utility (`BiosConfigUtility64.exe /npwdfile:"new.bin" /cpwdfile:"old.bin"`),
  HP Sure Admin (certificate-based, no shared password), HP Client Management Script Library (PowerShell
  `Set-HPBIOSSetupPassword`).
- **Lenovo**: Think BIOS Config Tool, WMI interface (`Lenovo_SetBiosPassword`), Lenovo Device Manager;
  supervisor password plus "lock UEFI BIOS settings".
- **Microsoft DFCI** (Device Firmware Configuration Interface) via Intune on supported Surface and OEM models:
  cloud-managed firmware settings without any local password, by certificate.

## Password management
- **Unique per device**; a single fleet-wide BIOS password is eventually leaked and printed in help desk notes.
- Escrow in a vault or device management tool, retrievable with audit; rotate after technician use.
- Certificate-based schemes (HP Sure Admin, DFCI, Dell's certificate-based BIOS management on newer models)
  avoid shared secrets entirely.

## Servers
BMC/iDRAC/iLO controls firmware settings remotely; harden the BMC (separate skill) and set the BIOS admin
password on servers in less trusted locations.

## Gotchas
- Some firmware updates require the password; build it into update tooling.
- Lost passwords on some models need vendor service to reset; escrow before rollout.
- Physical attacks (clearing CMOS, chip reflash) still exist; this raises the bar, it does not eliminate risk.

## Verify
Inventory/WMI query reports "setup password set" for all devices; boot to firmware setup prompts for a password;
USB boot is disabled; the vault has an entry per serial number.
