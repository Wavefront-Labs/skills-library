---
id: computing-software.systems-network-administration.dns-dhcp.ad-stub-zones-and-delegations
name: ad-stub-zones-and-delegations
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, windows-dns, ad-stub-zone, delegation, active-directory-dns, dnsserver-powershell]
level: practitioner
status: docs-checked
description: "Create stub zones and zone delegations on Windows DNS with Add-DnsServerStubZone and Add-DnsServerZoneDelegation, including AD replication scope."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/dnsserver/add-dnsserverstubzone
  - https://learn.microsoft.com/en-us/powershell/module/dnsserver/add-dnsserverzonedelegation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stub zones and delegations

## Delegation (child zone in your namespace)
`Add-DnsServerZoneDelegation` adds a delegation to a zone: for example a child domain `west01` of `contoso.com` with a DNS server for that child.
```powershell
Add-DnsServerZoneDelegation -Name "corp.example.com" -ChildZoneName "emea" `
  -NameServer "dc1.emea.corp.example.com" -IPAddress <CHILD_DNS_IP>
```
- `-Name` is the parent zone, `-ChildZoneName` the child, `-NameServer` the server hosting the child zone, `-IPAddress` an array of IP addresses of the child zone's DNS servers.
- Keep the delegation's name servers current when the child's servers change (practitioner advice; stale delegations point resolvers at servers that no longer answer).

## Stub zone
A stub zone is a copy of a zone that contains only the resource records that identify the DNS servers for that zone.
```powershell
Add-DnsServerStubZone -Name "partner.example.com" -MasterServers <MASTER_IP> -ReplicationScope Forest
Add-DnsServerStubZone -NetworkId 10.1.2.0/24 -MasterServers <MASTER_IP> -ReplicationScope Forest   # reverse zone
```
- `-MasterServers` takes IPv4 or IPv6 addresses of the zone's master servers.
- AD-integrated: `-ReplicationScope` accepts Forest, Domain, Legacy or Custom (Custom needs `-DirectoryPartitionName`). Forest stores it in the ForestDnsZone partition, so it is replicated to all DNS servers in the forest.
- File-backed: use `-ZoneFile` instead of a replication scope; that zone exists on that server only.
- `-NetworkId` (format A.B.C.D/prefix) creates the matching reverse lookup stub zone.

## Choosing
Use a delegation for a child of a zone you host; use a stub zone for another party's zone where you want to keep its name server list. Compare conditional forwarders (Add-DnsServerConditionalForwarderZone) when you prefer to point at fixed servers. Whether the partner must allow transfers to you depends on your environment; confirm it in testing.

## Verify
- [ ] `Resolve-DnsName host.partner.example.com -Server <DC>` works, and `Get-DnsServerZone` shows the stub zone with the right master servers.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Read the Add-DnsServerStubZone and Add-DnsServerZoneDelegation Learn pages. Removed as not in those pages: the SOA/NS/glue transfer detail, the comparison table with conditional forwarders, the dcpromo behaviour and the trust-scenario advice.
