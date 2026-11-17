---
id: computing-software.systems-network-administration.dns-dhcp.windows-dns-forwarders-vs-root-hints
name: windows-dns-forwarders-vs-root-hints
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, windows-dns, windows-forwarders, root-hints, dnsserver-powershell]
level: practitioner
status: docs-checked
description: "Choose and configure Windows DNS Server forwarders vs root hints: PowerShell commands, forwarding and recursion timeouts, root-hint fallback and troubleshooting."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/dnsserver/set-dnsserverforwarder
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/forwarders-resolution-timeouts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Forwarders vs root hints on Windows

Windows DNS resolves external names by either forwarding to upstream resolvers or iterating from
root hints.

## Configure
```powershell
Get-DnsServerForwarder
Set-DnsServerForwarder -IPAddress 192.0.2.53,198.51.100.53 -UseRootHint $true -Timeout 3
Add-DnsServerForwarder -IPAddress 10.10.0.53
Remove-DnsServerForwarder -IPAddress 198.51.100.53
Get-DnsServerRootHint
```
`-UseRootHint $false` stops the server trying iterative queries when the forwarders do not resolve
a query; by default the server falls back to root hints after the forwarders fail. `-Timeout` is the
seconds to wait for each forwarder (ForwardingTimeout, default 3). The server-wide RecursionTimeout
defaults to 8 seconds, so with default settings at most three forwarders are tried before the
client gets a server failure.

## Choosing
| Forwarders | Root hints |
|------------|------------|
| Central filtering (DNS security service, proxy) | No dependency on a third party |
| Outbound 53 allowed only to specific resolvers | DC needs outbound 53 to any internet server |
| Simpler troubleshooting with one upstream | Iterates from the root servers itself |
Many enterprises forward from DCs to a central secure resolver layer and disable root hints there to
avoid bypassing filtering.

## Troubleshooting
- Slow external resolution: first forwarder dead, each query waits for timeout; remove dead ones,
  order the fastest first.
- Fallback to root hints silently bypasses the security service: set `-UseRootHint $false` if policy requires.
- `Get-DnsServerForwarder` and `Get-DnsServerRecursion` show the forwarding and recursion timeouts.

## Verify
- [ ] Every DC has identical forwarder settings (`Get-DnsServerForwarder -ComputerName dcX`) and external lookups succeed.

## Checked
2026-10-28. Confirmed against the Set-DnsServerForwarder reference and the Microsoft Learn forwarder-timeouts page: `-UseRootHint` behaviour, `-Timeout`, ForwardingTimeout default 3 s, RecursionTimeout default 8 s, at most three forwarders tried, root-hint fallback. Confirmed in the DnsServer module index: Get-/Add-/Remove-DnsServerForwarder, Get-DnsServerRootHint, Get-DnsServerRecursion. Removed as unconfirmed: AD replication claim, public resolver addresses (now documentation addresses), Import-DnsServerRootHint, Resolve-DnsName example, conditional-forwarder precedence, 100 ms figure.
Method: documentation only; no commands were run.
