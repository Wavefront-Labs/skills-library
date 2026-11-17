---
id: computing-software.systems-network-administration.virtualisation.hyper-v-vms-on-smb3-and-scale-out-file-server
name: hyper-v-vms-on-smb3-and-scale-out-file-server
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [scale-out-file-server, smb3-hyper-v, sofs, hyper-v, storage]
level: advanced
status: docs-checked
description: "Store Hyper-V VMs on SMB 3 shares and Scale-Out File Server: creating a continuously available share, using it from Hyper-V, Kerberos delegation and checks."
sources:
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/sofs-overview
  - https://learn.microsoft.com/en-us/powershell/module/failoverclusters/add-clusterscaleoutfileserverrole
  - https://learn.microsoft.com/en-us/powershell/module/smbshare/new-smbshare
  - https://learn.microsoft.com/en-us/powershell/module/smbshare/set-smbpathacl
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/deploy/set-up-hosts-for-live-migration-without-failover-clustering
  - https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-direct
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# VMs on SMB 3 shares and Scale-Out File Server

**Goal:** Hyper-V hosts run VMs from file shares with continuous availability, as an alternative to SAN or S2D on the compute nodes.

## Build the SOFS (file cluster)
```powershell
Add-ClusterScaleOutFileServerRole -Name SOFS01 -Cluster FSCL01
New-Item -ItemType Directory "<SYSTEMDRIVE>\ClusterStorage\Volume1\VMs"
New-SmbShare -Name VMs -Path "<SYSTEMDRIVE>\ClusterStorage\Volume1\VMs" -ContinuouslyAvailable $true `
  -FullAccess 'CONTOSO\HV01$','CONTOSO\HV02$','CONTOSO\HVCL01$','CONTOSO\Hyper-V Admins' -ScopeName SOFS01
Set-SmbPathAcl -ShareName VMs -ScopeName SOFS01      # copy share permissions to NTFS
```
`Set-SmbPathAcl` copies the share permissions to the file system folder. The example grants the Hyper-V host accounts, the Hyper-V cluster account and an admin group full access; adapt it to your accounts.

## Use from Hyper-V
```powershell
New-VM -Name app01 -Generation 2 -Path '\\SOFS01\VMs' -NewVHDPath '\\SOFS01\VMs\app01\os.vhdx' -NewVHDSizeBytes 80GB -MemoryStartupBytes 4GB
Move-VMStorage -VMName old01 -DestinationStoragePath '\\SOFS01\VMs\old01'
```
When you manage a host remotely with Kerberos, configure **constrained delegation**: for storage on SMB select the `cifs` service, and for moving VMs `Microsoft Virtual System Migration Service` (per the live migration setup page).

## Performance
- SMB Multichannel detects RDMA-capable adapters and enables SMB Direct; without Multichannel, SMB Direct is not used.
- `Get-SmbMultichannelConnection` on the Hyper-V host shows the connections in use.
- Scale-Out File Server is for application data such as Hyper-V VM files, not general file shares (a general-use file server cluster is "not recommended" for Hyper-V in the feature table). Its shares are active-active across all cluster nodes and use CSV.

## Gotchas
- Create the share with `-ContinuouslyAvailable $true`, as in the example above.
- Some write-heavy operations must be committed to disk without buffering on continuously available shares, which can reduce performance versus general-purpose shares (see the SOFS overview note).

## Verify
A planned failover of a SOFS node (in a test) keeps the VMs running.

## Checked

Checked 2026-10-26 against MicrosoftDocs/windowsserverdocs (Scale-Out File Server overview, SMB Direct, live migration setup with constrained delegation; latest commit 2026-10-23) and the Windows Server 2025 `New-SmbShare`, `Set-SmbPathAcl` and `Add-ClusterScaleOutFileServerRole` references. Confirmed: SOFS is for application data such as Hyper-V VM files, active-active shares on CSV, `-ContinuouslyAvailable` and `-ScopeName` parameters, `Set-SmbPathAcl` copies share ACLs to the folder, delegation services (`cifs`, Microsoft Virtual System Migration Service), SMB Multichannel enabling SMB Direct. Removed as undocumented: the exact account permission requirement as a rule, the failure modes for non-CA shares, same-node and antivirus advice, and the `Get-SmbWitnessClient` and `Get-SmbOpenFile` verification claims.

Method: documentation only; no commands were run.
