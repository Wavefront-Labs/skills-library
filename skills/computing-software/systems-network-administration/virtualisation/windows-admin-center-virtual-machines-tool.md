---
id: computing-software.systems-network-administration.virtualisation.windows-admin-center-virtual-machines-tool
name: windows-admin-center-virtual-machines-tool
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [wac-virtual-machines, windows-admin-center, hyper-v, vm-management]
level: intro
status: docs-checked
description: "Manage Hyper-V VMs in Windows Admin Center: connections, inventory, creating and editing VMs, console via VMConnect, checkpoints and live migration in a cluster."
sources:
  - https://learn.microsoft.com/en-us/windows-server/manage/windows-admin-center/use/manage-virtual-machines
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Windows Admin Center virtual machines tool

**Goal:** day-to-day Hyper-V VM management from a browser, including for Server Core hosts.

## Connect
The Virtual Machines tool appears in server, failover cluster and hyper-converged cluster connections when the
Hyper-V role is enabled. It manages Hyper-V hosts running Windows Server with Desktop Experience or Server Core
(Hyper-V Server 2016 and 2019 are also supported). In a cluster connection the tool lists only clustered VMs.

## Virtual machines tool
- **Summary**: host or cluster CPU, memory and I/O performance, VM health alerts and recent Hyper-V event log
  events. Alerts and storage charts are available only for hyper-converged clusters on Windows Server 2016 or later;
  historical data only on Windows Server 2019 hyper-converged clusters.
- **Inventory**: VMs with state, host (for clusters), CPU and memory demand, uptime, heartbeat status and protection
  status through Azure Site Recovery. Actions: create, delete, start, turn off, shut down, pause, resume, reset,
  rename, save, delete saved state, create a checkpoint, change settings.
- **Create**: name, generation 1 or 2, host (recommended for clusters on Windows Server 2016 or later), path,
  vCPUs, nested virtualisation, memory, network adapters, virtual disks, and an OS installation source (.iso or
  network). Using an SMB share for VM storage requires CredSSP.
- **Settings**: General, Memory, Processors, Disks, Networks, Boot order and Checkpoints tabs; some settings
  require the VM to be stopped.
- **Connect**: the console uses VMConnect through the Hyper-V host: select **Connect** > **Download RDP file** and
  open it in Remote Desktop Connection with the Hyper-V host's admin credentials. Enhanced Session Mode is also
  listed in the tool.
- **Move** (cluster connections): **Manage** > **Move** live migrates a VM to another cluster node.
- **Checkpoints and details**: view, create, apply, rename and delete checkpoints for a single VM, with detailed
  information and performance charts.

## Strengths and gaps
- Good for Server Core, single hosts and small clusters; it combines Hyper-V Manager and Failover Cluster Manager
  capabilities in one view.
- Bulk changes and complex scripting still belong to PowerShell (see the bulk operations skill).

## Gotchas
- A cluster connection shows only clustered VMs.
- Some settings cannot change on a running VM.

## Verify
The VM list matches `Get-VM` on the hosts; console sessions and a test live migration work from WAC.

## Checked

Date checked: 2026-10-27. Documentation: "Manage virtual machines with Windows Admin Center" (windowsserverdocs main branch).
Confirmed: availability by connection type and Server Core support; Summary, Inventory, Create, Settings, Move and checkpoint features; console through VMConnect and RDP file download; CredSSP requirement for SMB share storage; cluster connections list only clustered VMs.
Method: documentation only; no commands were run.
