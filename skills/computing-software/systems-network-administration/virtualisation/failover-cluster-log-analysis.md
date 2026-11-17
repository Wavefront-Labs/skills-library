---
id: computing-software.systems-network-administration.virtualisation.failover-cluster-log-analysis
name: failover-cluster-log-analysis
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [get-clusterlog, failover-clustering, hyper-v-cluster, cluster-events, troubleshooting, hyper-v]
level: advanced
status: docs-checked
description: "Generate and read failover cluster logs with Get-ClusterLog: time windows, local time, key System event IDs (1135, 1069, 1177, 5120) and tracing a node removal or role failure."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/failoverclusters/get-clusterlog
  - https://learn.microsoft.com/en-us/powershell/module/failoverclusters/set-clusterlog
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/high-availability/troubleshoot-cluster-event-id-1135
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/high-availability/event-id-5120-cluster-shared-volume-troubleshooting-guidance
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Failover cluster log analysis

## Generate
```powershell
Get-ClusterLog -Destination "<TEMP_DIR>\clusterlogs" -TimeSpan 30 -UseLocalTime
Get-ClusterLog -Node hv01,hv02 -Destination "<TEMP_DIR>\clusterlogs" -TimeSpan 120
```
One log per node. `-TimeSpan` is the number of minutes back to include; `-UseLocalTime` makes timestamps local
time (the default is UTC, so compare nodes in the same time base). Without `-Destination` the logs go to the
`Cluster\Reports` folder under the Windows directory on each node. Generate soon after an incident: the log size is
capped and older entries are overwritten. Check or raise the cap with `Set-ClusterLog -Size 1024` (megabytes; the
reference gives 8 to 1024 on Windows Server 2016 and 8 to 2048 on 2019 and later).

## Start with the System event log (FailoverClustering source)
| ID | Meaning |
|---|---|
| 1135 | one or more nodes removed from active failover cluster membership |
| 1177 | quorum and connectivity needed for quorum were lost |
| 1069 | clustered service or application resource failed |
| 5120 | communication between a node and a Cluster Shared Volume was interrupted; the description carries a status code such as STATUS_IO_TIMEOUT |
```powershell
Get-WinEvent -FilterHashtable @{LogName='System'; ProviderName='Microsoft-Windows-FailoverClustering'; StartTime=(Get-Date).AddHours(-6)} |
  Select TimeCreated, Id, Message | Format-Table -Wrap
```
For event 5120, read the status code in the description first: Microsoft notes that occasional
STATUS_CLUSTER_CSV_AUTO_PAUSE_ERROR (c0130021) events can be ignored, while other codes indicate a problem.

## Reading the cluster log
Open the log around the timestamp of the System event and search for lines marked `ERR` and `WARN`; the first error
before the failure usually matters most. Correlate the same time window across nodes.
```powershell
Select-String -Path "<TEMP_DIR>\clusterlogs\hv01_cluster.log" -Pattern " ERR " | Select -First 50
```

## Typical causes for event 1135
Microsoft's 1135 article walks through node-to-node communication loss: the scenarios include a single node losing
contact and sites separated by a WAN link, and it points to cluster validation (network and firewall checks) and
ports and ping latency between nodes. Review heartbeat settings with `Get-Cluster | Format-List *Subnet*` (for example CrossSubnetDelay is a common cluster property) and
apply the fixes listed in that article before changing thresholds.

## Verify
You can name the first failing component and timestamp, correlated across nodes, and the change (network
isolation, threshold, driver) that addresses it.

## Checked

Date checked: 2026-10-27. Documentation: Get-ClusterLog and Set-ClusterLog reference (Windows Server 2025 docset), the Event ID 1135 troubleshooting article (applies to Windows Server 2016 to 2022 and Azure Stack HCI 21H2) and the Event ID 5120 CSV guidance article.
Confirmed: -TimeSpan in minutes, -UseLocalTime, default UTC, -Destination, -Node; Set-ClusterLog -Size ranges; event IDs 1135, 1177, 1069 and 5120 meanings; auto-pause status code guidance; CrossSubnetDelay as a common cluster property.

Method: documentation only; no commands were run.
