---
id: computing-software.systems-network-administration.virtualisation.hyper-v-vhdx-chain-inspect-and-repair
name: hyper-v-vhdx-chain-inspect-and-repair
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [test-vhd, reconnect-parent, avhdx, checkpoint-merge, vhdx, differencing-disk, hyper-v]
level: advanced
status: docs-checked
description: "Inspect and repair Hyper-V VHDX/AVHDX chains: map parents with Get-VHD, Test-VHD, reconnect a broken parent with Set-VHD, and merge manually with Merge-VHD safely."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vhd
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/merge-vhd
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/test-vhd
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/checkpoints
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inspecting and repairing VHDX chains

Broken chains happen after copying VMs by hand, restoring only some files, renaming
folders, or failed merges. Symptom: the VM won't start or `Test-VHD` reports a problem.

## Work on copies
Stop the VM and copy the whole folder (or take a storage snapshot) before any repair.

## Map the chain
```powershell
$d = Get-VMHardDiskDrive -VMName app01 | Select -Expand Path
$p = $d; while ($p) { $v = Get-VHD $p; $v | Format-List *; $p = $v.ParentPath }
Test-VHD -Path $d          # tests the disk for problems that would make it unusable
```

## Reconnect a parent
Parent moved or renamed:
```powershell
Set-VHD -Path "<VM_DIR>\app01_8F2A...avhdx" -ParentPath "<VM_DIR>\app01.vhdx"
```
Parent modified after the child was created (identifier mismatch): `-IgnoreIdMismatch` skips
the check. Use it only if you know the parent content is the right one (for example you
restored the same backup); a child whose parent changed after its creation is inconsistent, so
prefer restoring from backup.

## Manual merge (orphaned checkpoints, VM gone from inventory)
`Merge-VHD` merges from a source child disk into a destination disk in the chain. It is an offline operation: the chain must not be attached. Merge from the newest child down, one level at a time:
```powershell
Merge-VHD -Path "<VM_DIR>\app01_C3.avhdx" -DestinationPath "<VM_DIR>\app01_B2.avhdx"
Merge-VHD -Path "<VM_DIR>\app01_B2.avhdx" -DestinationPath "<VM_DIR>\app01.vhdx"
```
Then attach the merged base VHDX to the VM (or recreate the VM with it).

## Gotchas
- Never merge while the VM is running or attached to the chain; if Hyper-V still knows the
  checkpoints, delete them via `Remove-VMSnapshot` (Hyper-V merges the `.avhdx` into the `.vhdx`
  itself) and never delete `.avhdx` files directly.

## Verify
`Test-VHD` True for the final disk; VM boots; `Get-VMSnapshot -VMName app01` empty if you
merged all; file system check inside the guest (chkdsk/fsck) clean.

## Checked

Checked 2026-10-26 against the Windows Server 2025 Hyper-V cmdlet references (`Merge-VHD`, `Set-VHD`, `Test-VHD`, `Get-VHD`) and MicrosoftDocs/windowsserverdocs (Hyper-V checkpoints page). Confirmed: `Set-VHD -ParentPath` and `-IgnoreIdMismatch`, merge is offline and chain must not be attached, checkpoints are `.avhdx` files merged on deletion and must not be deleted directly. Removed as undocumented: the quoted error messages, the Hyper-V Manager Edit Disk path, the free-space and handle.exe gotchas, and the `Get-VHD` property names used in the chain-walk (replaced with `Format-List *` and `ParentPath`).

Method: documentation only; no commands were run.
