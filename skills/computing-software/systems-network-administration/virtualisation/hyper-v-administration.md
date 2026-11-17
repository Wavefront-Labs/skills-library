---
id: computing-software.systems-network-administration.virtualisation.hyper-v-administration
name: hyper-v-administration
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v, windows-server, windows-server-2022, windows-server-2025, failover-clustering, csv, cluster-shared-volumes, live-migration, kerberos-constrained-delegation, credssp, vswitch, set, switch-embedded-teaming, vmswitch, generation-2, secure-boot, vhdx, dynamic-memory, production-checkpoint, hyper-v-replica, cluster-aware-updating, cau, windows-admin-center, scvmm, powershell, hyper-v-powershell, storage-spaces-direct, s2d, integration-services]
level: advanced
status: docs-checked
description: "Administer Hyper-V hosts and failover clusters with PowerShell: SET switches, Gen 2 VMs and Linux Secure Boot, checkpoint types, CSV, live migration auth, Replica, CAU."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/overview
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/failover-clustering-overview
  - https://learn.microsoft.com/en-us/azure/azure-local/concepts/host-network-requirements
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/cluster-aware-updating
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/checkpoints
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hyper-V administration — script the host, cluster it, patch it without downtime

**Goal:** stand up Hyper-V hosts and a failover cluster that is consistent (PowerShell, not
clicks), migrates VMs live, and patches itself. Generic VM lifecycle and checkpoint
cautions are in
`computing-software.systems-network-administration.virtualisation.vm-lifecycle-snapshots-and-migration`.

## 1. Host build
```powershell
Install-WindowsFeature Hyper-V, Failover-Clustering -IncludeManagementTools -Restart
Set-VMHost -VirtualHardDiskPath '<CSV_ROOT>\Volume1\VHDs' `
           -VirtualMachinePath '<CSV_ROOT>\Volume1\VMs'
```
Server Core is a common choice for hosts; manage it remotely. Keep hosts identical: same NICs, firmware, drivers and
Windows build, because cluster validation flags differences. Live migration between hosts with different
processors needs processor compatibility mode (`Set-VMProcessor -CompatibilityForMigrationEnabled $true`, VM
off); it does not allow moving between Intel and AMD hosts.

## 2. Networking: Switch Embedded Teaming (SET)
SET is the teaming technology built into the Hyper-V virtual switch (Windows Server 2016 and later) and supports up
to eight adapters in a team. LBFO is not supported on Azure Local; on Windows Server prefer SET for new designs.
```powershell
New-VMSwitch -Name 'SETswitch' -NetAdapterName 'NIC1','NIC2' `
             -EnableEmbeddedTeaming $true -AllowManagementOS $false
Set-VMSwitchTeam -Name 'SETswitch' -LoadBalancingAlgorithm HyperVPort    # values: Dynamic (default) or HyperVPort
Add-VMNetworkAdapter -ManagementOS -SwitchName 'SETswitch' -Name 'Mgmt'
Add-VMNetworkAdapter -ManagementOS -SwitchName 'SETswitch' -Name 'LiveMigration'
Set-VMNetworkAdapterVlan -ManagementOS -VMNetworkAdapterName 'Mgmt' -Access -VlanId 99
Set-VMNetworkAdapterVlan -ManagementOS -VMNetworkAdapterName 'LiveMigration' -Access -VlanId 98
```
- Build the switch from the console or out-of-band; creating it over the NIC you are remoted through can drop the
  session.
- VM VLANs: `Set-VMNetworkAdapterVlan -VMName APP01 -Access -VlanId 10`.
- On Azure Local, Network ATC configures SET and the switch; do not build it by hand there.

## 3. VM defaults
- **Generation 2** for modern guests (UEFI firmware, Secure Boot, virtual TPM, SCSI boot).
- **Linux Gen 2:** Secure Boot needs the Microsoft UEFI Certificate Authority template (shown as "UEFI CA" in the
  generation guidance); choose it in the VM's firmware or security settings, or Linux guests will not boot with
  Secure Boot on.
- **VHDX:** dynamically expanding or fixed is a capacity-planning choice; monitor CSV free space either way.
- **Dynamic memory:** disable it for workloads that size caches at startup (for example database servers).
- **Checkpoints:** `Set-VM -CheckpointType Production` uses VSS (or file-system freeze on Linux) and takes no memory
  state; if it fails a standard checkpoint is created. `ProductionOnly` fails instead of falling back. Standard
  checkpoints can cause data-consistency problems for systems that replicate data, such as Active Directory.

## 4. Failover cluster
```powershell
Test-Cluster -Node HV01,HV02,HV03            # read every warning, not just failures
New-Cluster -Name HVCLU01 -Node HV01,HV02,HV03 -StaticAddress 10.99.0.50 -NoStorage
Add-ClusterSharedVolume -Name 'Cluster Disk 1'
Set-ClusterQuorum -FileShareWitness \\witness.corp.example\HVCLU01   # or -CloudWitness
```
- Configure a **witness** (file share or cloud) so the cluster tolerates losing half an even number of nodes.
- Make VMs highly available: `Add-ClusterVirtualMachineRole -VMName APP01`. A VM created only in Hyper-V Manager is
  not clustered.

## 5. Live migration
- Inside a cluster, the cluster handles migration. Outside a cluster (shared-nothing), use **Kerberos** with
  constrained delegation on the computer objects (`cifs` to move storage, `Microsoft Virtual System Migration
  Service` to move VMs); **CredSSP** needs no delegation but you must be signed in to the source server. CredSSP is
  the default authentication type.
- `Set-VMHost -VirtualMachineMigrationPerformanceOption SMB` (values TCPIP, Compression, SMB; Compression is the
  default) uses SMB for the highest throughput.
- Restrict migration to the dedicated network: `Add-VMMigrationNetwork 10.98.0.0/24` and
  `Set-VMHost -UseAnyNetworkForMigration $false`.

## 6. Replica and patching
- **Hyper-V Replica** replicates asynchronously every 30 seconds, 5 minutes or 15 minutes. It is DR, not backup.
- **Cluster-Aware Updating:** `Add-CauClusterRole -ClusterName HVCLU01 -DaysOfWeek Sunday -WeeksOfMonth 2
  -EnableFirewallRules` schedules self-updating runs that patch nodes one at a time. Keep enough capacity to run the
  cluster with one node out.

## Verify
- [ ] `Test-Cluster` passes with warnings understood; witness configured.
- [ ] `Get-VMSwitchTeam` shows SET with both NICs; host vNICs on correct VLANs.
- [ ] Every production VM is a clustered role (`Get-ClusterGroup`).
- [ ] Live migration of a test VM between every node pair succeeds.
- [ ] Linux Gen 2 VMs boot with Secure Boot on; no stale checkpoints (`Get-VMSnapshot`).
- [ ] A CAU run completed with no VM downtime.

## Checked

Date checked: 2026-10-27. Documentation: Windows Server Hyper-V and failover clustering pages (windowsserverdocs main branch), Azure Local host network requirements, Hyper-V PowerShell reference (Windows Server 2025 docset).
Confirmed: SET since Windows Server 2016, up to eight adapters, LBFO unsupported on Azure Local; New-VMSwitch -EnableEmbeddedTeaming and -AllowManagementOS; Set-VMSwitchTeam values Dynamic and HyperVPort; Set-VM -CheckpointType values and fallback behaviour; Microsoft UEFI Certificate Authority template for Linux; New-Cluster -NoStorage and -StaticAddress; Set-ClusterQuorum -FileShareWitness and -CloudWitness; Kerberos and CredSSP behaviour and CredSSP default; Set-VMHost migration performance values and Compression default; Add-VMMigrationNetwork; Replica intervals; Add-CauClusterRole parameters.

Method: documentation only; no commands were run.
