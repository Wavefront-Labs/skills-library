---
id: computing-software.systems-network-administration.virtualisation.hyper-v-host-antivirus-exclusions
name: hyper-v-host-antivirus-exclusions
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v-antivirus-exclusions, hyper-v-host-security, hyper-v-host, defender, cluster-shared-volumes, hyper-v]
level: practitioner
status: docs-checked
description: "Configure antivirus on Hyper-V hosts without breaking VMs: required folder, file type and process exclusions, CSV paths, Defender commands, and host security basics."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/virtualization/antivirus-exclusions-for-hyper-v-hosts
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/plan/plan-hyper-v-security-in-windows-server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Antivirus exclusions and host hardening for Hyper-V

Real-time scanning of VM files can cause VMs to go missing or fail to start (errors 0x800704C8, 0x80070037 or
0x800703E3), so Microsoft publishes a list of exclusions. Work with your antivirus vendor for the exact
configuration steps.

## Exclusions (Microsoft guidance, updated 2026-02)
**Directories** (and subdirectories)
- Default VM configuration: `%ProgramData%\Microsoft\Windows\Hyper-V`
- Default virtual hard disks: `%Public%\Documents\Hyper-V\Virtual Hard Disks`
- Default snapshots: `%SystemDrive%\ProgramData\Microsoft\Windows\Hyper-V\Snapshots`
- Default Cluster Shared Volumes path `%SystemDrive%\ClusterStorage`, if used
- Any custom VM configuration and virtual hard disk directories
- Custom replication data directories, if you use Hyper-V Replica
- SMB 3.0 shares that store VM files, if antivirus runs on the file servers

**File types** (all directories that contain them): `.vhd .vhdx .avhd .avhdx .vhds .vhdpmem .iso .rct .mrt .vsv
.bin .xml .vmcx .vmrs .vmgs`

**Processes**: `Vmms.exe`, `Vmwp.exe` (both in `%systemroot%\System32`), `Vmsp.exe` (Windows Server 2016 and
later) and `Vmcompute.exe` (Windows Server 2019 and later); these may have to be configured as process exclusions.

## Microsoft Defender
Microsoft states that if Windows Defender is your anti-malware solution you may not need extra exclusions, because
Defender applies automatic exclusions on servers; see its list of automatic exclusions. For custom paths, add
exclusions yourself:
```powershell
Add-MpPreference -ExclusionPath "<VM_DIR>","$env:SystemDrive\ClusterStorage"
Add-MpPreference -ExclusionProcess "vmms.exe","vmwp.exe","vmsp.exe","vmcompute.exe"
Add-MpPreference -ExclusionExtension ".vhdx",".avhdx",".vmcx",".vmrs",".vmgs",".iso",".rct",".mrt"
Get-MpPreference | Select -Expand ExclusionPath
```
Third-party antivirus: apply the same list in its own policy.

## Host security basics (Microsoft Hyper-V security planning)
- Use a separate network with a dedicated adapter for the physical Hyper-V host, and a private network for live
  migration traffic (consider IPsec to encrypt it).
- Use BitLocker to protect host resources, enable Secure Boot, and use TPM 2.0 hardware if you will build a guarded
  fabric.
- Configure antivirus, firewall and intrusion detection inside VMs as appropriate for each VM's role.
- Keep the root partition dedicated to Hyper-V: extra roles can hurt performance and widen the attack surface.

## Gotchas
- Host exclusions do not replace antivirus inside the guests.
- Apply the exclusions on SMB file servers that hold VM files as well.

## Verify
`Get-MpPreference` shows the custom paths; VMs start and checkpoints merge normally with the scanner running.

## Checked

Date checked: 2026-10-27. Documentation: "Recommended antivirus exclusions for Hyper-V hosts" (SupportArticles-docs, ms.date 2026-02-12), "Plan for Hyper-V security", and the Hyper-V performance-tuning configuration page (windowsserverdocs main branch).
Confirmed: directory, file type and process exclusion lists with their version gates; Defender automatic-exclusion note; host security recommendations (separate network, private migration network, BitLocker, Secure Boot, TPM 2.0 for guarded fabric); dedicated root partition guidance. Add-MpPreference -ExclusionPath, -ExclusionProcess and -ExclusionExtension exist in the Defender module reference.

Method: documentation only; no commands were run.
