---
id: computing-software.systems-network-administration.virtualisation.hyper-v-vhdx-disk-types
name: hyper-v-vhdx-disk-types
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v, vhdx, fixed-vhdx, dynamic-vhdx, differencing-disk, new-vhd, set-vhd, windows-server]
level: practitioner
status: docs-checked
description: "Choose between fixed, dynamic and differencing VHDX, create them with New-VHD, repair broken differencing chains with Set-VHD -ParentPath, and avoid chain pitfalls."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/new-vhd
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vhd
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/convert-vhd
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/best-practices-for-running-linux-on-hyper-v
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Fixed, dynamic and differencing VHDX

**Goal:** pick the right disk type per workload and keep differencing chains healthy.

| Type | Allocation | Use |
|---|---|---|
| Fixed | Full size at creation | Space is committed up front |
| Dynamic | Grows on write (32 MB block size by default) | General purpose |
| Differencing | Child records changes against a read-only parent | Lab templates, VDI pools; checkpoints use the same mechanism (`.avhdx`) |

## Create
```powershell
New-VHD -Path <VM_DIR>\db01-data.vhdx -SizeBytes 500GB -Fixed
New-VHD -Path <VM_DIR>\app01.vhdx -SizeBytes 127GB -Dynamic -BlockSizeBytes 1MB   # 1 MB blocks for Linux guests
New-VHD -Path <LAB_DIR>\lab01.vhdx -ParentPath <TEMPLATE_DIR>\ws2022-sysprep.vhdx -Differencing
```
Microsoft's Linux guidance: use `-BlockSizeBytes 1MB` instead of the 32 MB default for dynamic VHDX used by Linux guests, prefer ext4 to ext3, and create the file system with `mkfs.ext4 -G 4096` to reduce real disk space use.

## Inspect and repair chains
```powershell
Get-VHD <LAB_DIR>\lab01.vhdx | Format-List *
Set-VHD -Path <LAB_DIR>\lab01.vhdx -ParentPath <NEW_TEMPLATE_DIR>\ws2022-sysprep.vhdx   # parent moved
Test-VHD <LAB_DIR>\lab01.vhdx
```
If the parent was modified after children were created the identifiers no longer match; `Set-VHD -IgnoreIdMismatch` skips that check, so use it only when you know the parent content is unchanged, and otherwise restore the original parent.

## Convert
```powershell
Convert-VHD -Path app01.vhdx -DestinationPath app01-fixed.vhdx -VHDType Fixed   # offline: the disk must not be attached
```

## Gotchas
- Do not modify a parent disk that has children: the children record their parent's identifier.

## Verify
`Get-VHD` shows the intended `VhdType`, and every differencing disk's `ParentPath` exists and `Test-VHD` returns True.

## Checked

Checked 2026-10-26 against the Windows Server 2025 Hyper-V cmdlet references (`New-VHD` with `-Fixed/-Dynamic/-Differencing/-BlockSizeBytes`, `Set-VHD -ParentPath/-IgnoreIdMismatch`, `Convert-VHD -VHDType`, offline requirement) and the Best practices for running Linux on Hyper-V page (1 MB `BlockSizeBytes` instead of the 32 MB default, ext4 preferred, `mkfs.ext4 -G 4096`; checkpoints are `.avhdx` files per the checkpoints page). Removed as undocumented: performance comparisons between fixed and dynamic, the xfs remark, thin-LUN and chain-length advice, and the property list for `Get-VHD`.

Method: documentation only; no commands were run.
