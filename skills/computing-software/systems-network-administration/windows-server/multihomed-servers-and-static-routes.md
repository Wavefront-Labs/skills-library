---
id: computing-software.systems-network-administration.windows-server.multihomed-servers-and-static-routes
name: multihomed-servers-and-static-routes
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, network-adapters, multihomed-server, new-netroute, static-routes, interface-metric]
level: advanced
status: docs-checked
description: "Configure multihomed Windows servers correctly: one default gateway, persistent static routes with New-NetRoute, interface metrics and DNS registration per NIC."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/nettcpip/new-netroute
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/connectivity-issues-multiple-default-gateways
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/automatic-metric-for-ipv4-routes
  - https://learn.microsoft.com/en-us/powershell/module/nettcpip/set-netipinterface
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Multihomed servers and static routes

Servers with NICs on several networks (production, backup, storage, management) break in predictable ways:
asymmetric routing, wrong source address, DNS registering the backup IP.

## Rules
1. One default gateway, on the production NIC. Microsoft advises against default gateways across disjoint networks
   (for example on private interfaces of an edge server) because it can cause improper routing; with several gateways
   TCP can switch to another gateway after failures and lose connectivity to remote networks.
2. Reach remote subnets behind other NICs with **static routes**.
3. Only the production NIC registers in DNS.
4. Set interface metrics so production wins when routes tie (Windows assigns automatic metrics from link speed
   unless you set one).

## Commands
```powershell
New-NetRoute -DestinationPrefix 10.50.0.0/16 -InterfaceAlias Backup -NextHop 10.40.0.1 -RouteMetric 10   # saved in both ActiveStore and PersistentStore by default
Get-NetRoute -AddressFamily IPv4 | ? DestinationPrefix -ne '255.255.255.255/32' | ft DestinationPrefix,NextHop,InterfaceAlias,RouteMetric
Remove-NetRoute -DestinationPrefix 10.50.0.0/16 -Confirm:$false
Set-NetIPInterface -InterfaceAlias Production -InterfaceMetric 10
Set-NetIPInterface -InterfaceAlias Backup -InterfaceMetric 50
Set-DnsClient -InterfaceAlias Backup -RegisterThisConnectionsAddress $false
```
The older `route` utility (`route add <net> MASK <mask> <gateway>`) is the legacy equivalent.

## Strong host model
Per interface, `WeakHostSend` and `WeakHostReceive` are Disabled by default: with them disabled a host does not
send or receive packets on an interface that does not own the packet's address. Replies to a client on the backup
network that targeted the production IP therefore follow the route table and may be asymmetric. Fix with routes;
enable `-WeakHostSend`/`-WeakHostReceive` on `Set-NetIPInterface` only for special cases.

## Verify
- [ ] `Find-NetRoute -RemoteIPAddress 10.50.1.5` picks the backup NIC; `Resolve-DnsName <server>` returns only the production IP.

## Checked

2026-10-27. Documentation release: Support Articles 'Multiple default gateways can cause connectivity problems' (2026-02-12) and 'Automatic Metric feature for IPv4 routes', plus the New-NetRoute and Set-NetIPInterface references (Windows Server 2022 docset). Confirmed: guidance on default gateways across disjoint networks, static routes, automatic metrics, route saved in both policy stores by default, WeakHostSend/WeakHostReceive defaults and meaning, Set-DnsClient -RegisterThisConnectionsAddress. Removed the Windows Vista+ strong-host statement and the multihomed domain controller advice as unconfirmed.

Method: documentation only; no commands were run.
