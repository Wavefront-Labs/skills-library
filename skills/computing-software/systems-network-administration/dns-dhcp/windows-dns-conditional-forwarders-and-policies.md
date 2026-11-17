---
id: computing-software.systems-network-administration.dns-dhcp.windows-dns-conditional-forwarders-and-policies
name: windows-dns-conditional-forwarders-and-policies
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, windows-dns, conditional-forwarder, dns-policy, zone-scope, client-subnet, split-brain-dns, add-dnsserverconditionalforwarderzone, add-dnsserverqueryresolutionpolicy, dnsserver-powershell, active-directory-dns]
level: practitioner
status: docs-checked
description: "Configure Windows Server DNS conditional forwarders (AD-replicated) and DNS policies: client subnets, zone scopes for split-brain or geo answers, query filters, with PowerShell."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/dns/deploy/dns-policies-overview
  - https://learn.microsoft.com/en-us/powershell/module/dnsserver/add-dnsserverconditionalforwarderzone
  - https://learn.microsoft.com/en-us/powershell/module/dnsserver/add-dnsserverqueryresolutionpolicy
  - https://learn.microsoft.com/en-us/powershell/module/dnsserver/add-dnsserverclientsubnet
  - https://learn.microsoft.com/en-us/powershell/module/dnsserver/add-dnsserverzonescope
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows DNS: conditional forwarders and DNS policies

## Conditional forwarders
```powershell
Add-DnsServerConditionalForwarderZone -Name "partner.example" -MasterServers 192.0.2.53,192.0.2.54 `
  -ReplicationScope Forest -ForwarderTimeout 3
Resolve-DnsName host.partner.example -Server dc01
```
- `-ReplicationScope` accepts `Forest` (all DNS servers on DCs in the forest), `Domain`, `Legacy` (all DCs in the
  domain) and `Custom` (a directory partition named with `-DirectoryPartitionName`). Conditional forwarders are
  stored internally as zones.
- The master servers are queried in list order; `-ForwarderTimeout` is the seconds the server waits for a master
  before trying the next one (minimum 0, maximum 15). After all masters fail, the server can try to resolve the
  query itself.

## DNS policies (new in Windows Server 2016; also on 2019, 2022 and 2025)
Policies change answers based on client subnet, time of day, transport protocol, query type or FQDN: geo-location
traffic management, time-of-day redirection, split-brain DNS (works for AD-integrated and standalone zones) and
query filtering. Split-brain within one zone:
```powershell
Add-DnsServerClientSubnet -Name "Internal" -IPv4Subnet "10.0.0.0/8"
Add-DnsServerZoneScope -ZoneName "example.org" -Name "internal"
Add-DnsServerResourceRecord -ZoneName "example.org" -ZoneScope "internal" -A -Name "www" -IPv4Address 10.20.5.10
Add-DnsServerQueryResolutionPolicy -Name "InternalView" -Action ALLOW `
  -ClientSubnet "EQ,Internal" -ZoneScope "internal,1" -ZoneName "example.org"
```
Clients in 10/8 get `www` from the internal scope; others get the default scope record.

Block queries (simple DNS filtering):
```powershell
Add-DnsServerQueryResolutionPolicy -Name "BlockBad" -Action IGNORE -FQDN "EQ,*.bad.example" -PassThru
```
Criteria use `EQ` (values OR'd) and `NE` operators; `-QType "EQ,ANY"` matches ANY queries and `-FQDN` accepts `*`
wildcards.

## Gotchas
- Policy order: the server applies server-level policies first (except recursion policies), then zone-level
  policies, then recursion policies; within each type, `-ProcessingOrder` sets the precedence.
- Recursion policies (`-ApplyOnRecursion` with `-RecursionScope`) control how recursion is handled for matching
  queries, for example a split-brain setup where only internal clients recurse.

## Verify
- [ ] `Resolve-DnsName www.example.org -Server dc01` returns internal answers from an internal client, public from outside.
- [ ] The conditional forwarder resolves the partner name from a client of each DNS server.

## Checked
Date: 2026-10-28.
Confirmed against the Learn pages for Add-DnsServerConditionalForwarderZone (ReplicationScope values,
ForwarderTimeout 0-15 s, master server order), Add-DnsServerQueryResolutionPolicy (EQ/NE criteria, -Action
ALLOW/IGNORE, -ZoneScope "name,weight", -QType, -FQDN wildcards, -ProcessingOrder, policy order, -ApplyOnRecursion
with -RecursionScope), Add-DnsServerClientSubnet, Add-DnsServerZoneScope and the DNS Policy overview (2016 and later,
split-brain for AD-integrated and standalone zones).
Removed: the 5 s default forwarder timeout, the "works on DC1 not DC2" file-based forwarder remark, stub-zone advice,
the claim that zone scopes are not replicated by AD, and `Get-DnsServerZone` / `Get-DnsServerQueryResolutionPolicy`
(not on the fetched pages).
Method: documentation only; no commands were run.
