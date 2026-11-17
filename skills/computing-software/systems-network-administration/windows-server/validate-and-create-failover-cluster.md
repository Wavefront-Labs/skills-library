---
id: computing-software.systems-network-administration.windows-server.validate-and-create-failover-cluster
name: validate-and-create-failover-cluster
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, failover-clustering, failover-cluster, test-cluster, new-cluster, cluster-validation, cno, prestage-cno]
level: practitioner
status: docs-checked
description: "Validate and create a Windows failover cluster: feature install, Test-Cluster report, CNO permissions or prestaging, New-Cluster with static IP and post-checks."
sources:
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/create-failover-cluster
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/prestage-cluster-adds
  - https://learn.microsoft.com/en-us/powershell/module/failoverclusters/test-cluster
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Validate and create a failover cluster

## Prepare nodes
- Same OS and updates on every node, same roles/features, domain joined; use at least two networks.
```powershell
Invoke-Command $nodes { Install-WindowsFeature Failover-Clustering -IncludeManagementTools }
```

## Validate
```powershell
Test-Cluster -Node NODE1,NODE2 -Include 'Inventory','Network','System Configuration','Storage'
```
- Test-Cluster writes its results to a log file in the current working directory; archive the report.
- Microsoft supports a cluster solution only if the complete configuration passes all validation tests on certified
  hardware. Fix failures; understand every warning.
- Storage tests do not test online disks or pools in use by a clustered role; stop the role first (`Stop-ClusterGroup`)
  or limit the test with `-Disk`/`-Ignore`.

## Create
```powershell
New-Cluster -Name CLUSTER01 -Node NODE1,NODE2 -StaticAddress 10.0.0.40 -NoStorage
```
- The creating account needs Create Computer objects on the OU or container where the cluster servers reside, or have
  a domain admin prestage the CNO: create a computer account named for the cluster, **disable** it, and give the
  installing user Full Control.
- The CNO then needs Create Computer objects on its OU so it can create VCOs for roles. A missing permission or an
  exhausted computer-account quota shows as event 1194.
- `-NoStorage` leaves disks unclaimed; add them deliberately afterwards (`Get-ClusterAvailableDisk | Add-ClusterDisk`).
- Multi-subnet: give one `-StaticAddress` per subnet.

## Post-create
```powershell
Get-ClusterNode; Get-ClusterNetwork; Get-ClusterResource
```
Configure the quorum witness immediately.

## Verify
- [ ] Cluster name resolves and pings; CNO enabled in AD.
- [ ] Validation report archived with the build documentation.

## Checked

Confirmed 2026-10-25 against the Windows Server docs (create-failover-cluster and prestage-cluster-adds; repository last commit 2026-10-23) and the Test-Cluster reference: Microsoft supports cluster solutions only if the complete configuration passes all validation tests, Test-Cluster writes a log file to the current working directory, storage tests skip online disks in use by clustered roles, New-Cluster -NoStorage -StaticAddress, prestaged CNO steps, Create Computer objects permission. Replaced the unconfirmed validation report path, removed the unconfirmed same-patch-level and Get-Cluster threshold comments.

Method: documentation only; no commands were run.
