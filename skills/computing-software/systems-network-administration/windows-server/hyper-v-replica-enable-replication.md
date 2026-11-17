---
id: computing-software.systems-network-administration.windows-server.hyper-v-replica-enable-replication
name: hyper-v-replica-enable-replication
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, hyper-v-replica, enable-vmreplication, set-vmreplicationserver, kerberos-authentication, certificate-authentication, initial-replication, disaster-recovery]
level: practitioner
status: docs-checked
description: "Enable Hyper-V Replica: configure the replica server for Kerberos or certificate auth, firewall, Enable-VMReplication, initial replication options and frequency."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/configure-replication-single-host
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/replication-virtual-machines
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/enable-vmreplication
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmreplicationserver
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enable Hyper-V Replica

Asynchronous VM replication between Hyper-V hosts or clusters. Changes are sent every 30 seconds, 5 minutes or
15 minutes; no shared storage is needed. Hyper-V Replica is not available on Windows client Hyper-V.

## Replica server
```powershell
# Kerberos (HTTP port 80, same or trusted domain)
Set-VMReplicationServer -ReplicationEnabled $true -AllowedAuthenticationType Kerberos `
  -ReplicationAllowedFromAnyServer $true -DefaultStorageLocation '<vol>:\Replica'
Enable-NetFirewallRule -DisplayName 'Hyper-V Replica HTTP Listener (TCP-In)'
# Certificate (HTTPS port 443, workgroup or untrusted domains)
Set-VMReplicationServer -ReplicationEnabled $true -AllowedAuthenticationType Certificate `
  -CertificateThumbprint <thumb> -ReplicationAllowedFromAnyServer $true -DefaultStorageLocation '<vol>:\Replica'
Enable-NetFirewallRule -DisplayName 'Hyper-V Replica HTTPS Listener (TCP-In)'
Get-VMReplicationServer
```
The Hyper-V role creates the HTTP and HTTPS exceptions but does not enable them; enable the rule that matches the
authentication type on every receiving host. Certificates need both Client and Server Authentication EKUs and a private
key. `Set-VMReplicationServer` also takes `-KerberosAuthenticationPort`, `-CertificateAuthenticationPort`,
`-MonitoringInterval` and `-MonitoringStartTime`; see its reference page for authorization-entry options to restrict
which primaries may replicate in.

## Enable for a VM
```powershell
Enable-VMReplication -VMName APP01 -ReplicaServerName hv-dr01.corp.example.com -ReplicaServerPort 80 `
  -AuthenticationType Kerberos -ReplicationFrequencySec 300 -RecoveryHistory 4 -VSSSnapshotFrequencyHour 4 `
  -CompressionEnabled $true -ExcludedVhdPath '<vol>:\VMs\APP01\pagefile.vhdx'
Start-VMInitialReplication -VMName APP01                          # send the initial copy over the network now
Start-VMInitialReplication -VMName APP01 -InitialReplicationStartTime (Get-Date '22:00')  # schedule (up to 7 days ahead)
Start-VMInitialReplication -VMName APP01 -DestinationPath '<external media path>'        # export to external media
```
- Defaults when only the minimum parameters are given: 5 minute frequency, no extra recovery points.
- `-RecoveryHistory` keeps up to 24 extra hourly recovery points; `-VSSSnapshotFrequencyHour` only applies when
  RecoveryHistory is not zero.
- Exclude page file or temporary VHDX files with `-ExcludedVhdPath` to cut churn.
- To seed a large VM, restore a copy on the replica server and run `Start-VMInitialReplication -UseBackup`, or use
  external media (see the initial-replication-media skill).

## Monitor
```powershell
Get-VMReplication -VMName APP01
Measure-VMReplication -VMName APP01
```
The primary shows State `Replicating` once the initial copy completes. Health values are Normal, Warning and
Critical; a placeholder VM waiting for an external-media import shows Warning.

## Verify
- [ ] State Replicating, Health Normal for each VM.
- [ ] Test failover performed (see failover skill).

## Checked

2026-10-26 against the Windows Server docs (configure-replication-single-host, replication-overview, replication-virtual-machines; repository last commit 2026-10-23) and the Hyper-V module reference (Windows Server 2025): frequencies of 30 s, 5 min and 15 min, firewall rule display names and that they are not enabled by default, EKU requirement, Set-VMReplicationServer, Enable-VMReplication and Start-VMInitialReplication parameter names including -UseBackup and -DestinationPath, 24 recovery points maximum, the 5 minute default, a scheduled start of up to seven days, and Warning on a placeholder VM. Removed unconfirmed claims about unencrypted Kerberos traffic, the certificate revocation registry value, the 20% Warning rule and `.hrl` growth behaviour.

Method: documentation only; no commands were run.
