---
id: computing-software.systems-network-administration.virtualisation.vsphere-ha-disable-host-monitoring-for-maintenance
name: vsphere-ha-disable-host-monitoring-for-maintenance
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [host-monitoring-disable, vsphere-ha, network-maintenance, isolation-response, vmware, vsphere]
level: practitioner
status: draft
description: "Suspend vSphere HA host monitoring before switch or network maintenance so a lost heartbeat does not trigger isolation responses and mass VM restarts."
sources:
  - https://knowledge.broadcom.com/external/article?legacyId=1033634
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Disable HA host monitoring during network maintenance

**Goal:** network work on management or vSAN switches without HA powering off VMs.

## Why
Host isolation is decided by missing network heartbeats plus failed pings to isolation addresses. Rebooting both core switches or changing management VLANs can make every host think it is isolated, and the isolation response (power off/shut down) runs.

## Procedure
1. Before the change: Cluster -> Configure -> vSphere Availability -> Edit -> Failures and responses -> **Enable Host Monitoring: off**. VM restart on actual host crash is also disabled while off.
   PowerCLI:
```powershell
$c = Get-Cluster prod-cl01
$spec = New-Object VMware.Vim.ClusterConfigSpecEx
$spec.dasConfig = New-Object VMware.Vim.ClusterDasConfigInfo
$spec.dasConfig.hostMonitoring = 'disabled'
$c.ExtensionData.ReconfigureComputeResource_Task($spec, $true)
```
2. Do the network change; confirm hosts reconnect and vmkernel pings work (`vmkping -I vmk0 <gw>`).
3. Re-enable host monitoring (`'enabled'`). Check Cluster -> Monitor -> vSphere HA for a clean state.

## Alternatives
- Change isolation response to *Disabled* (Leave powered on) for the window: hosts still restart VMs from truly failed hosts, but isolated hosts keep VMs running.
- For a single host's NIC work, put that host into maintenance mode instead.

## Gotchas
- Forgetting to turn it back on leaves the cluster unprotected; add the re-enable step to the change plan and a reminder.
- vSAN clusters: switch work on the vSAN network also partitions vSAN; plan with vSAN maintenance or a full outage window.
- VM monitoring is separate; disabling host monitoring does not stop VMCP/VM monitoring actions.

## Verify
After the window `(Get-Cluster prod-cl01).ExtensionData.Configuration.DasConfig.HostMonitoring` returns `enabled`, and no VMs restarted during the change.
