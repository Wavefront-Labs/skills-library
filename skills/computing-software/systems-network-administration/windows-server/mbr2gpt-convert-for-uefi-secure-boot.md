---
id: computing-software.systems-network-administration.windows-server.mbr2gpt-convert-for-uefi-secure-boot
name: mbr2gpt-convert-for-uefi-secure-boot
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, boot-troubleshooting, mbr2gpt, uefi, secure-boot, gpt]
level: advanced
status: gated
description: "Convert a server's OS disk from MBR to GPT with mbr2gpt so it can boot UEFI with Secure Boot, including validation, BitLocker, and Hyper-V Gen 1 limits."
sources:
  - https://learn.microsoft.com/en-us/windows/deployment/mbr-to-gpt
  - https://learn.microsoft.com/en-us/windows-hardware/design/device-experiences/oem-secure-boot
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Convert MBR to GPT with mbr2gpt

Secure Boot, VBS/Credential Guard and many hardening baselines need UEFI, which needs a GPT system disk. mbr2gpt
converts in place without data loss.

## Requirements
- Learn's validation list includes: at most three primary partitions in the MBR partition table, space at the start and
  end of the disk (16 KB + 2 sectors at the front, 16 KB + 1 sector at the end), and a boot/system partition marked active.
  Run `/validate` and read its output rather than relying on this list.
- Firmware supports UEFI.

## Steps
```cmd
REM suspend BitLocker first if on (see BitLocker documentation for the exact command)
mbr2gpt /validate /disk:0 /allowFullOS
mbr2gpt /convert /disk:0 /allowFullOS
```
Logs: Learn names `diagerr.xml`, `diagwrn.xml`, `setupact.log` and `setuperr.log`. Then reboot into firmware setup, switch boot mode from Legacy/CSM to
**UEFI**, enable Secure Boot, boot Windows. Re-enable BitLocker protectors.

From WinPE you can omit `/allowFullOS` (Learn: it is needed to run from the full OS).

## Virtual machines
- Hyper-V Generation 1 VMs cannot switch to UEFI; Secure Boot needs a Generation 2 VM, so many choose to rebuild.
- VMware: change firmware to EFI in VM settings after conversion.

## Verify
```powershell
Get-Disk 0 | Select PartitionStyle            # GPT
Confirm-SecureBootUEFI                        # True
msinfo32  # BIOS Mode: UEFI, Secure Boot State: On
```
- [ ] Server boots UEFI with Secure Boot on; BitLocker protection resumed.

## Checked
2026-10-28. Confirmed on Learn "MBR2GPT": validate/convert with /allowFullOS, the partition-count and disk-space validation
conditions, the four log files. Removed as unconfirmed: extended-partition ban, ~100 MB ESP size, manage-bde command and
RebootCount. The verification commands (Get-Disk PartitionStyle, Confirm-SecureBootUEFI, msinfo32 fields) and the
Generation 1/VMware remarks are general practice not shown on the fetched pages (gated: unconfirmed, source is paywalled or blocked).
Method: documentation only; no commands were run.
