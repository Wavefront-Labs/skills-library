---
id: computing-software.systems-network-administration.windows-server.hyper-v-live-migration-and-shared-nothing-migration
name: hyper-v-live-migration-and-shared-nothing-migration
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, hyper-v-live-migration, shared-nothing-migration, move-vm, kerberos-constrained-delegation, smb-direct-migration, compression]
level: practitioner
status: docs-checked
description: "Configure Hyper-V live migration: CredSSP vs Kerberos delegation, compression, SMB and RDMA, migration networks, shared-nothing moves."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/move-vm
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/deploy/set-up-hosts-for-live-migration-without-failover-clustering
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmhost
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# Live migration and shared-nothing migration

- **Live migration** moves a running VM between hosts with minimal downtime.
- In a failover cluster, storage is shared; only memory moves.
- **Shared-nothing live migration** (nonclustered hosts) can move the VM's storage over the network too (`Move-VM -IncludeStorage`).

## Enable on each host
Requirements: Hyper-V role on source and destination (hosts running Windows Server 2012 R2 and later can live migrate), both in the same Active Directory domain or in domains that trust each other, and membership in local Hyper-V Administrators or Administrators on both.
```powershell
Enable-VMMigration
Set-VMHost -VirtualMachineMigrationAuthenticationType Kerberos `
  -VirtualMachineMigrationPerformanceOption SMB `
  -MaximumVirtualMachineMigrations 2 -MaximumStorageMigrations 2
Add-VMMigrationNetwork 10.20.0.0/24            # restrict migration traffic to this network
Set-VMHost -UseAnyNetworkForMigration $false
```
The default for simultaneous live migrations in Hyper-V Manager is 2. Live migration traffic is not
encrypted on the wire: put it on an isolated trusted network (physical or VLAN).
`Get-VMMigrationNetwork` lists the configured migration networks.

## Authentication
`-VirtualMachineMigrationAuthenticationType` accepts `CredSSP` or `Kerberos`.
| Option | Notes |
|---|---|
| CredSSP | no delegation setup, but you must be signed in to the source server (console, RDP or remote PowerShell session); moving a VM back needs a sign-in to the other server |
| Kerberos | no sign-in to the server needed; requires **constrained delegation** |
Starting with Windows Server 2025, Credential Guard is on by default for domain-joined non-DC servers, so CredSSP live migration no longer works there: use Kerberos constrained delegation.

Constrained delegation (needs Domain Administrators): in Active Directory Users and Computers open the source
server's computer account > Delegation > *Trust this computer for delegation to the specified services only* >
*Use any authentication protocol*, Add, pick the destination server, and select `Microsoft Virtual System Migration Service`
(to move VMs) and `cifs` (to move storage). Repeat on the destination server's account, naming the source.
Changes take effect after they replicate to the domain controllers the hosts use and a new Kerberos ticket is issued.

## Performance options
`-VirtualMachineMigrationPerformanceOption` accepts `TCPIP`, `Compression` or `SMB`.
- **TCP/IP**: copies memory over a plain TCP/IP connection.
- **Compression**: compresses memory before copying; the default.
- **SMB**: copies memory over SMB 3.0; SMB Direct is used when both NICs have RDMA enabled and SMB Multichannel uses multiple connections when configured.

## Shared-nothing move
```powershell
Move-VM -Name app01 -DestinationHost HV02 -IncludeStorage -DestinationStoragePath '<VMPath>\app01'
Move-VMStorage -VMName app01 -DestinationStoragePath '<NewVMPath>\app01'      # storage only
Compare-VM -Name app01 -DestinationHost HV02          # compatibility report before moving
```
For CPUs of different generations, `Set-VMProcessor -CompatibilityForMigrationEnabled $true` limits the virtual
processor's features for migration (see the cmdlet page for when the VM must be off).

## Troubleshooting
| Error | Cause |
|---|---|
| `0x8009030E` "No credentials are available in the security package" | CredSSP without a sign-in to the source server (or Credential Guard on Server 2025): sign in to the source or use Kerberos |

## Verify
- [ ] Remote `Move-VM` from a management workstation succeeds with Kerberos (no CredSSP).
- [ ] Migration traffic uses the designated network (`Get-VMMigrationNetwork`).

## Checked
2026-10-28. Confirmed against "Set up hosts for live migration without Failover Clustering" (requirements, CredSSP/Kerberos behaviour, 0x8009030E message, Server 2025 Credential Guard note, delegation steps and services, default of 2 simultaneous migrations, performance options, unencrypted traffic, Enable-VMMigration/Set-VMHost) and the Hyper-V cmdlet reference pages for `Set-VMHost`, `Add-VMMigrationNetwork`, `Move-VM`, `Move-VMStorage`, `Compare-VM`, `Set-VMProcessor`. Fixed: delegation protocol is "Use any authentication protocol", not "Kerberos only". Removed as unconfirmed: the `Set-ADComputer msDS-AllowedToDelegateTo` snippet, `klist purge`, `Set-SmbBandwidthLimit`, same-vendor/switch-name/configuration-version rules, the other error strings and the VMMS log path.
Method: documentation only; no commands were run.
