---
id: computing-software.systems-network-administration.virtualisation.hyper-v-gpu-partitioning
name: hyper-v-gpu-partitioning
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [gpu-partitioning, gpu-p, hyper-v, gpu, windows-server]
level: advanced
status: docs-checked
description: "Share a physical GPU between Hyper-V VMs with GPU partitioning (GPU-P) on Windows Server 2025 and Azure Local: supported GPUs, partition setup, VM assignment and limits."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/gpu-partitioning
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/partition-assign-vm-gpu
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# GPU partitioning (GPU-P)

**Goal:** give several VMs a slice of one GPU for VDI, inference or graphics, instead of a whole device per VM (DDA).

## Requirements
- Windows Server 2025 (live migration of GPU-P VMs starts there). GPU-P suits standalone servers; Datacenter edition is required if you need clustering for unplanned failover. Supported GPUs per Microsoft: NVIDIA A2, A10, A16, A40, L2, L4, L40, L40S, RTX Pro 6000 Blackwell Server Edition, and AMD Radeon PRO V710. NVIDIA live migration needs the driver from NVIDIA vGPU software v18.x or later.
- SR-IOV and IOMMU enabled in firmware. For live migration the CPU needs IOMMU DMA bit tracking (AMD EPYC 7003 Milan or later, 4th Gen Intel Xeon Sapphire Rapids); EPYC 7002 supports GPU-P but not live migration.
- Guests: Windows 10 or later, Windows Server 2019 or later, Ubuntu 18.04/20.04/22.04, with the vendor guest driver.

## Configure the host
```powershell
Get-VMHostPartitionableGpu | Select Name, ValidPartitionCounts, PartitionCount
Set-VMHostPartitionableGpu -Name '<gpu-instance-path>' -PartitionCount 4
```
Use one of the counts listed in `ValidPartitionCounts`. Each VM gets a dedicated fraction of the GPU.

## Assign to a VM
```powershell
Add-VMGpuPartitionAdapter -VMName vdi01
Get-VMGpuPartitionAdapter -VMName vdi01 | FL InstancePath,PartitionId,PartitionVfLuid
```
Install the vendor guest driver inside the VM.

## Live migration
Windows Server 2025 supports live migration of GPU-P VMs. Microsoft requires a homogeneous configuration (same GPU make/model and the same partition count on every host). Migration falls back to TCP/IP with compression, so it is slower and uses more host CPU. Plan spare partitions on other hosts. Without IOMMU-capable CPUs a clustered VM is restarted on another host instead.

## Limits
- Partitions are auto-assigned (you cannot pick one for a VM), and each extra partition added to a VM appears as another GPU. The partition count must match across all GPUs in a homogeneous cluster.
- Windows Admin Center is Microsoft's recommended way to configure it (it validates homogeneity); with PowerShell repeat the steps on every server.
- A physical GPU is either assigned by DDA or partitionable, not both.

## Verify
In the guest, Device Manager shows the vendor GPU without errors; on the host `Get-VMGpuPartitionAdapter -VMName <name>` lists the assignment and `Get-VMHostPartitionableGpu | FL Name,ValidPartitionCounts,PartitionCount` shows the configured count.

## Checked
Checked 2026-10-25 against Microsoft Learn Hyper-V documentation (MicrosoftDocs/windowsserverdocs, latest commit 2026-10-23) and the Windows Server 2025 PowerShell reference (MicrosoftDocs/windows-powershell-docs, latest commit 2026-10-23). Confirmed: the Windows Server 2025 live-migration requirement, supported GPU and guest lists, IOMMU DMA bit-tracking CPUs, NVIDIA vGPU 18.x driver requirement, homogeneous-configuration rule, TCP/IP-with-compression fallback, and the Get-VMHostPartitionableGpu, Set-VMHostPartitionableGpu, Add-VMGpuPartitionAdapter and Get-VMGpuPartitionAdapter commands. Removed because no documentation page confirmed them: the equal-partition, powered-off assignment, vendor licence and nvidia-smi remarks, and the unconfirmed checkpoint statement.
Method: documentation only; no commands were run.
