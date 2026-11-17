---
id: computing-software.systems-network-administration.virtualisation.hyper-v-replica-failover-tcpip-settings
name: hyper-v-replica-failover-tcpip-settings
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [failover-ip-settings, hyper-v-replica, disaster-recovery, hyper-v]
level: practitioner
status: docs-checked
description: "Pre-configure failover TCP/IP settings so Hyper-V Replica VMs get the DR site IP address at failover, plus test failover networking and DNS considerations."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/replication-virtual-machines
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmnetworkadapterfailoverconfiguration
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmnetworkadapter
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Failover TCP/IP settings

**Goal:** a VM failed over to the DR site comes up with an address that works there, without someone logging in to change it.

## How it works
Static IP injection sets the IP address a VM uses when it starts after a failover. The settings are stored in the VM configuration and applied during failover by the Key Value Pair (KVP) Exchange integration component in the guest. If the VM should use a dynamically assigned address, no settings are needed.

## Configure (on the replica VM, on the replica server)
```powershell
Set-VMNetworkAdapterFailoverConfiguration -VMName app01 -VMNetworkAdapterName 'Network Adapter' `
  -IPv4Address 10.2.20.15 -IPv4SubnetMask 255.255.255.0 -IPv4DefaultGateway 10.2.20.1 `
  -IPv4PreferredDNSServer 10.2.0.10 -IPv4AlternateDNSServer 10.2.0.11
Get-VMNetworkAdapterFailoverConfiguration -VMName app01
```
Hyper-V Manager: replica VM -> Settings -> Network Adapter -> *Failover TCP/IP*. Set these values on both the primary server and the replica server (the VM and its host must run the same integration services version). IPv6 uses `-IPv6Address`, `-IPv6SubnetPrefixLength`, `-IPv6DefaultGateway`, `-IPv6PreferredDNSServer` and `-IPv6AlternateDNSServer`.

Also connect the replica VM's adapter to the DR site switch, and set the **test failover** switch:
```powershell
Set-VMNetworkAdapter -VMName app01 -TestReplicaSwitchName 'Isolated-Test'
```

## Requirements
- The latest integration services in the guest, synthetic (not legacy) network adapters, and a supported Windows guest operating system.
- A VM that takes a dynamic address needs no failover settings.

## Verify
Run a test failover: the test VM starts on the test switch; check the guest's IP configuration, then stop the test failover with `Stop-VMFailover`.

## Checked
Checked 2026-10-25 against Microsoft Learn Hyper-V documentation (MicrosoftDocs/windowsserverdocs, latest commit 2026-10-23) and the Windows Server 2025 PowerShell reference (MicrosoftDocs/windows-powershell-docs, latest commit 2026-10-23). Confirmed: static IP injection mechanism (KVP Exchange), its requirements, the IPv4 and IPv6 parameter names of Set-VMNetworkAdapterFailoverConfiguration, setting it on the replica VM and on both servers, and Set-VMNetworkAdapter -TestReplicaSwitchName. Removed because no documentation page confirmed them: the Linux KVP daemon and package names, DHCP/DNS planning advice, and the stretched-VLAN remark.
Method: documentation only; no commands were run.
