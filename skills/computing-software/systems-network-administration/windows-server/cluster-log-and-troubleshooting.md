---
id: computing-software.systems-network-administration.windows-server.cluster-log-and-troubleshooting
name: cluster-log-and-troubleshooting
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, failover-clustering, failover-cluster, get-clusterlog, cluster-troubleshooting, event-1135, cluster-diagnostics, clussvc]
level: advanced
status: docs-checked
description: "Troubleshoot failover clusters with Get-ClusterLog, key events (1135, 1069, 1146, 1205), resource state, and node removal and network partition patterns."
sources:
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/troubleshooting-using-wer-reports
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/high-availability/troubleshoot-cluster-event-id-1135
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/high-availability/event-id-5120-cluster-shared-volume-troubleshooting-guidance
  - https://learn.microsoft.com/en-us/powershell/module/failoverclusters/get-clusterlog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshoot clusters with Get-ClusterLog and events

## Generate the cluster log
```powershell
Get-ClusterLog -Destination '<vol>:\Temp' -TimeSpan 60 -UseLocalTime     # last 60 minutes, every node
Get-ClusterLog -Node NODE2 -Destination '<vol>:\Temp' -Health
```
- `-TimeSpan` is in minutes. Timestamps are GMT unless `-UseLocalTime`; match the System event log time zone to the
  cluster log before correlating events.
- Increase verbosity temporarily: `Set-ClusterLog -Level 5` (levels 0-5, default 3 = errors, warnings, info), size with `-Size`.

## Key events (System log, source FailoverClustering)
| Event | Meaning |
|---|---|
| 1135 | one or more nodes removed from active cluster membership (lost communication between nodes) |
| 1177 | quorum lost |
| 1069 | clustered resource failed or could not be brought online |
| 1146 | seen alongside 1069 and 1230 when a resource is unresponsive (see the unexpected-failover article) |
| 1205 | one or more resources failed to come online |
| 1194 | cluster network name could not create its computer object in AD (CNO permissions) |
| 5120 | CSV lost its path on this node; the status code in the description names the cause |
| 5142 | non-owner node disconnected from the CSV, I/O no longer queued |
Plus `Microsoft-Windows-FailoverClustering/Diagnostic` and `Operational` channels.

## Quick state
```powershell
Get-ClusterNode | Select Name,State
Get-ClusterResource | ? State -ne Online | Select Name,ResourceType,OwnerGroup,State
Get-ClusterGroup | Select Name,OwnerNode,State
Test-Cluster -Node (Get-ClusterNode).Name -Include Network
```

## Patterns
- 1135: review the event on every node, then check network packet loss between the nodes, NIC and switch
  configuration, and NIC teaming on the heartbeat NIC; in multi-site clusters consider raising heartbeat time-outs.
- Resource flapping: check its dependencies (`Get-ClusterResourceDependency`).
- Cluster service will not start on one node: run `Get-ClusterLog -Node` for it from another node.

## Verify
- [ ] Root cause tied to a log line and event; fix tested with a planned failover.

## Checked

Confirmed 2026-10-25 against the Windows Server 2025 PowerShell reference for Get-ClusterLog (parameters -TimeSpan minutes, -UseLocalTime GMT default, -Health) and Set-ClusterLog (levels 0-5, default 3), and the Microsoft support articles on events 1135, 1177, 1069, 1205, 1194, 5120 and 5142. Removed unconfirmed log-line component tags, search strings, the CLUSDB path and per-event root-cause lists.

Method: documentation only; no commands were run.
