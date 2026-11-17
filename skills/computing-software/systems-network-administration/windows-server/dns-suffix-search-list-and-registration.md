---
id: computing-software.systems-network-administration.windows-server.dns-suffix-search-list-and-registration
name: dns-suffix-search-list-and-registration
category: computing-software
field: systems-network-administration
product: windows-server
tags: [server-networking, dns-suffix-search-list, set-dnsclientserveraddress, dynamic-dns-registration, set-dnsclientglobalsetting]
level: practitioner
status: docs-checked
description: "Configure DNS client suffixes on servers: primary and connection suffixes, search list by GPO, devolution, and which adapters register in DNS."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/dnsclient/set-dnsclientglobalsetting
  - https://learn.microsoft.com/en-us/powershell/module/dnsclient/set-dnsclient
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# DNS suffix search list and registration

Short names (`\\fs01`, `sql01`) resolve by appending suffixes. Multi-domain estates and multihomed servers get this
wrong constantly.

## How Windows builds the list
Without a configured list, Windows appends the primary DNS suffix, then the connection-specific suffixes, and, if devolution is enabled (`Set-DnsClientGlobalSetting -UseDevolution`, `-DevolutionLevel`), parent labels of the primary suffix.

## Set a search list
```powershell
Set-DnsClientGlobalSetting -SuffixSearchList @('corp.example.com','dev.example.com','example.com')
Get-DnsClientGlobalSetting
```
For fleets, set the DNS Client policy "DNS Suffix Search List" in Administrative Templates; include every suffix you need in the list.

Connection-specific suffix:
```powershell
Set-DnsClient -InterfaceAlias 'LAN' -ConnectionSpecificSuffix corp.example.com
```

## Registration on multihomed servers
Only the client-facing adapter should register in DNS; storage, backup, cluster and heartbeat NICs registering cause
clients to resolve the server to an unreachable IP.
```powershell
Set-DnsClient -InterfaceAlias 'Storage1','Backup' -RegisterThisConnectionsAddress $false
ipconfig /registerdns
```
Then delete stale A records for those IPs from the zone (or let scavenging remove them).

## Diagnose
```powershell
Resolve-DnsName sql01 -Type A          # shows which FQDN answered
Get-DnsClient | Select InterfaceAlias,ConnectionSpecificSuffix,RegisterThisConnectionsAddress
```

## Verify
- [ ] Short names resolve to the right domain; only one A record per server for its client IP.

## Checked

Checked 2026-10-25 against the MicrosoftDocs/windowsserverdocs and windows-powershell-docs (Windows Server 2025 DnsServer/DhcpServer/DnsClient modules) repositories, latest commit 2026-10-23. Confirmed: `Set-DnsClientGlobalSetting` parameters `-SuffixSearchList`, `-UseDevolution`, `-DevolutionLevel`; `Set-DnsClient` parameters `-InterfaceAlias`, `-ConnectionSpecificSuffix`, `-RegisterThisConnectionsAddress`; `Resolve-DnsName` exists. Removed the exact search-order and Group Policy menu path claims, which the checked pages do not state.

Method: documentation only; no commands were run.
