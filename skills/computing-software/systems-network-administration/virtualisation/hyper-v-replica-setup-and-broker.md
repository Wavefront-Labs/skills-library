---
id: computing-software.systems-network-administration.virtualisation.hyper-v-replica-setup-and-broker
name: hyper-v-replica-setup-and-broker
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v, hyper-v-replica, enable-vmreplication, replica-broker, replication-authentication, disaster-recovery, windows-server]
level: advanced
status: docs-checked
description: "Set up Hyper-V Replica: replica server settings, Kerberos or certificate authentication, firewall rules, the cluster Replica Broker, and initial replication options."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/configure-replication-failover-cluster
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/configure-replication-single-host
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/enable-vmreplication
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmreplicationserver
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hyper-V Replica setup and Replica Broker

**Goal:** asynchronously replicate VMs to a second host or cluster for DR.

## Replica (target) server
```powershell
Set-VMReplicationServer -ReplicationEnabled $true -AllowedAuthenticationType Kerberos `
  -ReplicationAllowedFromAnyServer $true -DefaultStorageLocation '<REPLICA_DIR>'
Enable-NetFirewallRule -DisplayName 'Hyper-V Replica HTTP Listener (TCP-In)'
```
- **Kerberos** (HTTP, port 80): same or trusted domain; no encryption.
- **Certificate** (HTTPS, 443): non-domain-joined or untrusted hosts, or when you want encryption; certificates need both Client and Server Authentication EKU, a private key, a valid root, and CN or SAN matching the host or broker FQDN.

## Clustered target: Replica Broker
A cluster cannot be addressed by node; add the broker role:
```powershell
Failover Cluster Manager: Configure Role -> Hyper-V Replica Broker, give it a Client Access Point (NetBIOS name, 15 characters at most, unique in AD), then right-click the role -> Replication Settings. PowerShell equivalent (per the Microsoft procedure, with a DHCP or static IP resource added to the group):
```powershell
$n = 'HVR-Broker'
Add-ClusterGroup -Name $n -GroupType VMReplicaBroker
Add-ClusterResource -Name "Hyper-V Replica Broker $n" -Group $n -ResourceType 'Virtual Machine Replication Broker'
Add-ClusterResource -Name $n -Group $n -ResourceType 'Network Name'
# add an 'IP Address' resource for the management network, set DnsName, add dependencies, then:
Start-ClusterGroup -Name $n
```
Configure the broker on the receiving cluster. A cluster that sends VMs needs a certificate for the broker FQDN on each primary host when using certificate authentication.

## Enable replication per VM (on primary)
```powershell
Enable-VMReplication -VMName app01 -ReplicaServerName 'hvr-broker.corp.example' -ReplicaServerPort 80 `
  -AuthenticationType Kerberos -ReplicationFrequencySec 300 -CompressionEnabled $true
Start-VMInitialReplication -VMName app01            # or -DestinationPath for out-of-band seeding
```
Frequency: 30, 300 or 900 seconds (the documented example default is 5 minutes). Exclude disks you do not need with `-ExcludedVhdPath`.

## Gotchas
- Attach the replica VM to a network if needed after failover, and set the test switch with `Set-VMNetworkAdapter -TestReplicaSwitchName`.
- Initial replication of large VMs over WAN: seed via external media (`Start-VMInitialReplication -DestinationPath`).

## Verify
`Get-VMReplication` shows `State Replicating, Health Normal` on both ends.

## Checked
Checked 2026-10-25 against Microsoft Learn Hyper-V documentation (MicrosoftDocs/windowsserverdocs, latest commit 2026-10-23) and the Windows Server 2025 PowerShell reference (MicrosoftDocs/windows-powershell-docs, latest commit 2026-10-23). Confirmed: the Replica Broker procedure (Add-ClusterGroup -GroupType VMReplicaBroker and the Virtual Machine Replication Broker resource type, 15-character name), Kerberos HTTP port 80 versus certificate HTTPS port 443, certificate requirements, and the listener firewall rule names. Removed because no documentation page confirmed them: the Add-ClusterServerRole broker command (not the documented method), and the same-switch-name claim.
Method: documentation only; no commands were run.
