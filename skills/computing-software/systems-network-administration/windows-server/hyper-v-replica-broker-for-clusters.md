---
id: computing-software.systems-network-administration.windows-server.hyper-v-replica-broker-for-clusters
name: hyper-v-replica-broker-for-clusters
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, hyper-v-replica, replica-broker, failover-clustering, add-clustervmreplicabroker, clustered-hyper-v, disaster-recovery]
level: advanced
status: docs-checked
description: "Configure the Hyper-V Replica Broker role so failover clusters can send and receive replication: create the broker, certificates, and target the broker name."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/configure-replication-failover-cluster
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/replication-overview
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Hyper-V Replica Broker for clusters

A Hyper-V cluster cannot be addressed by node name for replication because VMs move. The Replica Broker is a clustered
role on the **receiving** cluster that acts as the single point of contact for the primary server, even if the replica VM
moves between nodes. Configure the receiving cluster, not the primary cluster or host.

## Create the role
Use Windows Admin Center (Virtualization mode), Failover Cluster Manager (Configure Role, Hyper-V Replica Broker) or
PowerShell. The broker name is a NetBIOS name (15 characters at most) unique in the domain, and the role needs an IP
address (DHCP or static) on the management cluster network. The CNO needs rights to create the broker's computer object,
or prestage it.
```powershell
$netbiosName = 'HVR-BROKER'
$clusterNetwork = Get-ClusterNetwork -Name '<management network name>'
Add-ClusterGroup -Name $netbiosName -GroupType VMReplicaBroker
Add-ClusterResource -Name "Hyper-V Replica Broker $netbiosName" -Group $netbiosName -ResourceType 'Virtual Machine Replication Broker'
Add-ClusterResource -Name $netbiosName -Group $netbiosName -ResourceType 'Network Name'
Add-ClusterResource -Name ('IP Address ' + $clusterNetwork.Address) -Group $netbiosName -ResourceType 'IP Address'
Get-ClusterResource -Name ('IP Address ' + $clusterNetwork.Address) | Set-ClusterParameter -Multiple @{Network=$clusterNetwork.Name;EnableDhcp=1} -Create
Get-ClusterResource -Name $netbiosName | Set-ClusterParameter -Name DnsName -Value $netbiosName
Add-ClusterResourceDependency -Resource $netbiosName ('IP Address ' + $clusterNetwork.Address)
Add-ClusterResourceDependency -Resource "Hyper-V Replica Broker $netbiosName" $netbiosName
Start-ClusterGroup -Name $netbiosName
Get-ClusterGroup | ? GroupType -eq VMReplicaBroker
```
For a static address, set `Address`, `SubnetMask` and `EnableDhcp=0` on the IP Address resource instead.

## Replication settings
In the broker's Replication Settings (Windows Admin Center or Failover Cluster Manager) enable the cluster as a Replica
server and choose Kerberos (HTTP, port 80 by default) or certificate-based (HTTPS, port 443 by default) authentication.
Kerberos suits clusters and hosts in the same or trusted domains; use certificates for untrusted or workgroup hosts or
when you want encryption. Enable the matching Windows Firewall rule for Hyper-V Replica on every node.

## Certificates
The certificate subject common name or SAN must match the FQDN of the Replica Broker role you give for the receiving
cluster. A cluster that sends VMs also needs its own certificate.

## Enabling VMs
On the primary, point the replica server at the broker FQDN, not at a node, and test the path first:
```powershell
Test-VMReplicationConnection -ReplicaServerName 'hvr-broker.corp.example.com' -ReplicaServerPort 80 -AuthenticationType Kerberos
```

## Verify
- [ ] Broker role Online; moving it to another node keeps replication healthy.

## Checked

Confirmed 2026-10-25 against the Windows Server docs (configure-replication-failover-cluster, repository last commit 2026-10-23): the broker is a clustered role on the receiving cluster that gives the primary one point of contact, the documented PowerShell creates the role with Add-ClusterGroup -GroupType VMReplicaBroker plus resources of type Virtual Machine Replication Broker, Network Name and IP Address, broker names are NetBIOS names limited to 15 characters, Kerberos uses HTTP port 80 and certificates use HTTPS port 443, the certificate subject or SAN must match the broker FQDN, firewall rules must be enabled, and Test-VMReplicationConnection checks connectivity. Replaced the previous Add-ClusterServerRole creation commands and Set-VMReplicationServer example, which are not documented there, and removed the per-node certificate SAN and Measure-VMReplication claims.

Method: documentation only; no commands were run.
