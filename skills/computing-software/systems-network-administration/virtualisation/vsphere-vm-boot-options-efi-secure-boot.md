---
id: computing-software.systems-network-administration.virtualisation.vsphere-vm-boot-options-efi-secure-boot
name: vsphere-vm-boot-options-efi-secure-boot
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vm-boot-options, efi-secure-boot-vm, uefi, secure-boot, vmware, vsphere]
level: practitioner
status: draft
description: "Configure VM firmware, UEFI Secure Boot, boot delay, forced setup entry and boot retry in vSphere, and avoid breaking an installed OS by switching firmware."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0.html
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VM boot options, EFI firmware and Secure Boot

**Goal:** VMs boot with the right firmware and security settings, and you can get into setup when needed.

## Settings (Edit Settings -> VM Options -> Boot Options)
| Option | `.vmx` key | Notes |
|---|---|---|
| Firmware BIOS/EFI | `firmware = "efi"` | Choose before OS install |
| Secure Boot | `uefi.secureBoot.enabled = "TRUE"` | EFI only, HW version 13+ |
| Boot delay | `bios.bootDelay = "5000"` | ms; gives time to hit Esc/F2 |
| Force setup | `bios.forceSetupOnce = "TRUE"` | Next boot enters firmware setup, then resets |
| Failed boot recovery | `bios.bootRetry.enabled`, `bios.bootRetry.delay` | Retry when no boot device |

## PowerCLI
```powershell
$vm = Get-VM win11-01   # must be powered off
$spec = New-Object VMware.Vim.VirtualMachineConfigSpec
$spec.Firmware = 'efi'
$spec.BootOptions = New-Object VMware.Vim.VirtualMachineBootOptions
$spec.BootOptions.EfiSecureBootEnabled = $true
$spec.BootOptions.BootDelay = 3000
$vm.ExtensionData.ReconfigVM($spec)
```

## Gotchas
- Switching BIOS to EFI on an installed OS makes it unbootable (MBR vs GPT). Convert inside the guest first (Windows `mbr2gpt /convert`), then change firmware.
- Windows 11 and Credential Guard need EFI + Secure Boot + vTPM (vTPM needs a key provider).
- Linux with Secure Boot must use signed shim/kernel; unsigned third-party kernel modules (some backup or AV agents) fail to load.
- Turning Secure Boot on for an older ESXi-hosted VM with unsigned drivers gives a boot failure; turn it off, update drivers, retry.
- VMs cloned from BIOS templates stay BIOS; keep separate EFI templates.

## Verify
In the guest: Windows `msinfo32` shows *BIOS Mode UEFI* and *Secure Boot State On*; Linux `mokutil --sb-state` prints `SecureBoot enabled`.
