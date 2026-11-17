---
id: computing-software.systems-network-administration.windows-server.cluster-aware-updating
name: cluster-aware-updating
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, failover-clustering, failover-cluster, cluster-aware-updating, cau, self-updating-mode, invoke-causcan, add-cauclusterrole]
level: practitioner
status: docs-checked
description: "Patch failover clusters with Cluster-Aware Updating: self-updating role, run profiles, pre/post scripts, remote-updating runs and reading CAU reports."
sources:
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/cluster-aware-updating
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/cluster-aware-updating-options
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/cluster-aware-updating-requirements
  - https://learn.microsoft.com/en-us/powershell/module/clusterawareupdating/add-cauclusterrole
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cluster-Aware Updating (CAU)

CAU drains a node, installs updates, reboots, resumes, fails back, and moves to the next,
keeping the workload online. With S2D it also uses storage maintenance mode and waits for
resync.

## Prerequisites
- RSAT-Clustering-PowerShell and Failover Clustering tools on nodes (and the
  coordinator computer for remote mode).
- Firewall rule group "Remote Shutdown" enabled on nodes (or pass `-EnableFirewallRules`).
- PowerShell remoting and .NET Framework 4.5 or later on every node if you use pre/post-update scripts.
- `Test-CauSetup -ClusterName CLUSTER01` runs the CAU Best Practices Analyzer to test readiness.

## Self-updating mode
```powershell
Add-CauClusterRole -ClusterName CLUSTER01 -DaysOfWeek Sunday -WeeksOfMonth 2 -StartDate '2026-11-08 02:00' `
  -MaxFailedNodes 0 -MaxRetriesPerNode 2 -RequireAllNodesOnline -EnableFirewallRules -Force
Get-CauClusterRole -ClusterName CLUSTER01
```
Creates a clustered CAU role that orchestrates itself on schedule.

## Remote-updating (on demand)
```powershell
Invoke-CauScan -ClusterName CLUSTER01     # preview
Invoke-CauRun -ClusterName CLUSTER01 -MaxFailedNodes 0 -RequireAllNodesOnline -Force
```

## Plug-ins and scripts
- `Microsoft.WindowsUpdatePlugin` (default, WU/WSUS per node policy),
  `Microsoft.HotfixPlugin` (drivers/firmware/hotfixes from a share).
- `-PreUpdateScript`/`-PostUpdateScript` (a `.ps1` path) run on each node: the pre-update script before the node
  enters maintenance mode, the post-update script after it leaves. `-ConfigurationName` names the PowerShell
  session configuration used to run them.
- Most options can be saved as an XML Updating Run Profile and reused for later runs.

## Reports
```powershell
Get-CauReport -ClusterName CLUSTER01 -Last -Detailed
```

## Gotchas
- Do not let WSUS or another tool apply updates to the nodes on its own schedule; all nodes should use the same
  update source, and approvals must be correct for the cluster nodes before a run.

## Verify
- [ ] Last report: all nodes Succeeded, roles back on preferred owners.

## Checked

Confirmed 2026-10-25 against the Windows Server docs repository (MicrosoftDocs/windowsserverdocs, last commit 2026-10-23) and the Windows Server 2025 PowerShell reference: Add-CauClusterRole and Invoke-CauRun parameters (DaysOfWeek, WeeksOfMonth, StartDate, MaxFailedNodes, MaxRetriesPerNode, RequireAllNodesOnline, EnableFirewallRules, ConfigurationName), Microsoft.WindowsUpdatePlugin as default and Microsoft.HotfixPlugin, Remote Shutdown firewall group, Test-CauSetup as the Best Practices Analyzer, pre/post-update script behaviour, XML Updating Run Profiles. Removed unconfirmed claims about the Admin event channel, multi-reboot handling and that script failures stop the run.

Method: documentation only; no commands were run.
