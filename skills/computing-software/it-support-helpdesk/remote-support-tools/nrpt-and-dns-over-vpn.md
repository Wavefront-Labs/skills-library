---
id: computing-software.it-support-helpdesk.remote-support-tools.nrpt-and-dns-over-vpn
name: nrpt-and-dns-over-vpn
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, nrpt-vpn-dns, nrpt, name-resolution-policy-table, vpn-dns, interface-metric, dns-suffix]
level: advanced
status: docs-checked
description: "Fix internal names not resolving on VPN: how Windows applies NRPT, interface metric and DNS suffix search, the VPNv2 DomainNameInformationList settings, and reading the NRPT."
sources:
  - "https://learn.microsoft.com/en-us/powershell/module/dnsclient/get-dnsclientnrptpolicy"
  - "https://learn.microsoft.com/en-us/windows/security/operating-system-security/network-security/vpn/vpn-name-resolution"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nrpt-and-dns-over-vpn

"VPN is connected but internal names do not resolve" is usually the client asking the wrong
DNS server for that name.

## How Windows resolves names with a VPN up
Per Microsoft's VPN name resolution page:
1. The network stack checks the **Name Resolution Policy Table (NRPT)** for a match and
   resolves through it if one matches.
2. With no match, the DNS suffix of the most preferred interface (by interface metric) is
   appended to a short name and the query goes to that interface.
3. If that times out, the DNS suffix search list is used in order and queries are sent on
   all interfaces.
NRPT entries can match a fully qualified name, a suffix, or "any" (try the entry's
server first).

## Fixes
- **NRPT through the VPN profile**: the VPNv2 CSP node
  `VPNv2/<ProfileName>/DomainNameInformationList` holds the rules: `DomainName`,
  `DnsServers` and `WebServers` (proxy) per row. In an Intune VPN profile these are the
  "Add or edit DNS rule" fields (Name, Servers, Proxy server). A `Persistent` node per
  row makes name resolution for that item go over the VPN.
- **DNS suffix**: the VPN profile `DnsSuffix` node sets the primary DNS suffix of the VPN
  interface and the suffix search list once connected; short names need a suffix.
- Interface metric decides step 2, so check which interface is preferred when no NRPT rule
  matches.

## Diagnose
`Get-DnsClientNrptPolicy` shows the NRPT (add `-Effective` for the effective policy,
`-Namespace` to filter). Compare resolving a name normally with asking the corporate DNS
server directly: if the direct query works but normal resolution fails, the problem is how
queries are routed (NRPT, metric or suffix), not the DNS server itself.

## Verify
On VPN, internal names resolve via the intended DNS servers and the expected NRPT rule is
listed; off VPN, no stale rules remain.

## Checked
2026-11-01. Confirmed on Microsoft Learn "VPN name resolution" (resolution order, NRPT match
types, VPNv2 nodes DomainNameInformationList/DnsSuffix/Persistent, Intune field mapping) and
Get-DnsClientNrptPolicy (cmdlet, -Effective, -Namespace). Removed: Always On VPN ProfileXML
sample, Set-NetIPInterface metric command, Resolve-DnsName/Get-NetIPInterface examples,
third-party split-DNS clients, DirectAccess stale-rule and DoH/split-brain claims, dead
Always On VPN deployment source URL.
Method: documentation only; no commands were run.
