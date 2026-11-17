---
id: computing-software.systems-network-administration.windows-server.workgroup-and-multi-domain-clusters
name: workgroup-and-multi-domain-clusters
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, failover-clustering, failover-cluster, workgroup-cluster, multi-domain-cluster, ad-detached-cluster, dns-administrative-access-point, localaccounttokenfilterpolicy]
level: advanced
status: docs-checked
description: "Build AD-detached failover clusters: workgroup and multi-domain nodes, local admin account, DNS administrative access point, witness and supported workloads."
sources:
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/create-workgroup-cluster
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/deploy-cloud-witness
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Workgroup and multi-domain clusters

A workgroup cluster (introduced in Windows Server 2016) joins nodes as member servers without an on-premises domain
controller. There is no CNO in AD; the cluster uses a DNS administrative access point.

## Supported workloads
- Hyper-V VMs: supported from Windows Server 2025.
- SQL Server availability groups (Windows Server 2016 to 2025), as domain-independent availability groups.
- Not supported: file servers (authentication issues) and SQL Server failover cluster instances.

Quorum can use a cloud witness, disk witness or USB witness.

## Prepare every node
```powershell
# identical local admin account (same name and password) on all nodes
New-LocalUser -Name clusteradmin -Password (Read-Host -AsSecureString) -PasswordNeverExpires
Add-LocalGroupMember -Group Administrators -Member clusteradmin
# only if you do not use the built-in Administrator account
New-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System' -Name LocalAccountTokenFilterPolicy -Value 1 -PropertyType DWord -Force
# WinRM: trust the other nodes
Set-Item WSMan:\localhost\Client\TrustedHosts -Value 'node1,node2'
Install-WindowsFeature Failover-Clustering -IncludeManagementTools
```
Set the same primary DNS suffix on every node (System properties, Computer Name, More), and make sure the nodes resolve
each other in DNS.

## Create (as the local admin)
```powershell
New-Cluster -Name WGCL01 -Node node1,node2 -AdministrativeAccessPoint DNS -StaticAddress 10.0.0.60
Set-ClusterQuorum -CloudWitness -AccountName <acct> -AccessKey <key>
```

## Gotchas
- Manage with the local account; remote Failover Cluster Manager connections need the same credentials.
- SQL availability groups in this setup use certificates instead of Kerberos (see the domain-independent availability
  group documentation).

## Verify
- [ ] `Get-Cluster | Select AdministrativeAccessPoint` = Dns; witness online.

## Checked

Confirmed 2026-10-25 against the Windows Server docs (create-workgroup-cluster, repository last commit 2026-10-23): workgroup clusters introduced in Windows Server 2016; Hyper-V VMs supported from Windows Server 2025; SQL Server availability groups supported 2016 to 2025 (domain-independent availability groups); file servers and SQL Server FCI not supported; quorum via cloud, disk or USB witness; identical local accounts, LocalAccountTokenFilterPolicy when not using the built-in administrator, WinRM TrustedHosts, common primary DNS suffix; New-Cluster -AdministrativeAccessPoint DNS. Corrected the supported-workload list (the previous text wrongly listed general-use file servers) and removed the unconfirmed live migration, registry-suffix, certificate and file share witness claims.

Method: documentation only; no commands were run.
