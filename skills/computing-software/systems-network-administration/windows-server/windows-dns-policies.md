---
id: computing-software.systems-network-administration.windows-server.windows-dns-policies
name: windows-dns-policies
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-dns-server, dnsserver-module, dns-policies, split-brain-dns, zone-scopes, client-subnet, add-dnsserverqueryresolutionpolicy, query-filter, geo-location-dns, recursion-scope]
level: advanced
status: docs-checked
description: "Use Windows DNS Server policies: client subnets, zone scopes and query resolution policies for split-brain and geo answers, recursion scopes, and blocking queries."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/dns/deploy/dns-policies-overview
  - https://learn.microsoft.com/en-us/windows-server/networking/dns/deploy/split-brain-dns-deployment
  - https://learn.microsoft.com/en-us/windows-server/networking/dns/deploy/dns-sb-with-ad
  - https://learn.microsoft.com/en-us/powershell/module/dnsserver/add-dnsserverqueryresolutionpolicy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows DNS Server policies

DNS policy is new in Windows Server 2016. Policies evaluate criteria (client subnet, transport,
protocol, server interface, FQDN, query type, time of day) and pick a **zone scope** or an action.

## Split-brain on one server (file-backed zone)
```powershell
Add-DnsServerClientSubnet -Name 'Internal' -IPv4Subnet '10.0.0.0/8','172.16.0.0/12'
Add-DnsServerZoneScope   -ZoneName 'example.com' -Name 'internal'
Add-DnsServerResourceRecord -ZoneName 'example.com' -ZoneScope 'internal' -A -Name 'www' -IPv4Address 10.1.2.3
Add-DnsServerQueryResolutionPolicy -Name 'SplitBrain-Internal' -Action ALLOW `
  -ClientSubnet 'eq,Internal' -ZoneScope 'internal,1' -ZoneName 'example.com'
```
Internal clients get 10.1.2.3, others get the default scope record. Alternative split by the
**server interface** the query arrives on (`-ServerInterfaceIP 'eq,10.0.0.5'`).

Note: on an **AD-integrated** zone the zone scopes and their records replicate through AD, but DNS policies are not AD-integrated and are stored on the local server, so create them on **every** DNS server that hosts the zone (they can be exported from one server and imported on others). Dynamic updates and scavenging apply only to the default zone scope.

## Recursion control (split-brain with recursion off for external clients)
```powershell
Set-DnsServerRecursionScope -Name . -EnableRecursion $false
Add-DnsServerRecursionScope -Name 'InternalClients' -EnableRecursion $true
Add-DnsServerQueryResolutionPolicy -Name 'RecursionInternal' -Action ALLOW -ApplyOnRecursion `
  -RecursionScope 'InternalClients' -ServerInterfaceIP 'eq,10.0.0.5'
```

## Block/ignore queries (filters)
```powershell
Add-DnsServerQueryResolutionPolicy -Name 'BlockBadDomain' -Action IGNORE -FQDN 'EQ,*.malicious.example' -PassThru
```
`DENY` returns REFUSED; `IGNORE` drops the query.

## Inspect and order
```powershell
Get-DnsServerQueryResolutionPolicy -ZoneName example.com
Get-DnsServerQueryResolutionPolicy                    # server-level
Set-DnsServerQueryResolutionPolicy -Name SplitBrain-Internal -ProcessingOrder 1
```

## Verify
- [ ] `Resolve-DnsName www.example.com -Server dns01` from an internal and an external client returns different answers.
- [ ] Every DNS server hosting the zone has identical policies (compare `Get-DnsServerQueryResolutionPolicy` output).

## Checked

Checked 2026-10-25 against the MicrosoftDocs/windowsserverdocs and windows-powershell-docs (Windows Server 2025 DnsServer/DhcpServer/DnsClient modules) repositories, latest commit 2026-10-23. Confirmed: DNS policy introduced in Windows Server 2016; DENY returns REFUSED and IGNORE drops the query; server-level policies on incoming queries can only DENY or IGNORE; policies are stored per server and not replicated for AD-integrated zones while zone scopes replicate; default recursion scope named `.`; the split-brain and recursion-scope cmdlet examples and their parameters (`-ClientSubnet`, `-ZoneScope`, `-ApplyOnRecursion`, `-RecursionScope`, `-ServerInterfaceIP`, `-ProcessingOrder`). Removed the 'limited ways' wording that no page supports.

Method: documentation only; no commands were run.
