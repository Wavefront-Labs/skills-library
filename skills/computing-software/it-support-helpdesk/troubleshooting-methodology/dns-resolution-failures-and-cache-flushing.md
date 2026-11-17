---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.dns-resolution-failures-and-cache-flushing
name: dns-resolution-failures-and-cache-flushing
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, networking, network-troubleshooting, dns-troubleshooting, nslookup, resolve-dnsname, ipconfig-flushdns, hosts-file, dns-suffix, nrpt, split-dns]
level: practitioner
status: draft
description: "Prove and fix DNS problems on clients: name vs IP tests, nslookup against specific servers, flushing caches, hosts file, DNS suffix and split-DNS over VPN, and NRPT rules."
sources:
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/troubleshoot-dns-guidance"
  - "https://learn.microsoft.com/en-us/powershell/module/dnsclient/resolve-dnsname"
  - "https://www.comptia.org/certifications/a"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# dns-resolution-failures-and-cache-flushing

Goal: confirm or rule out DNS in two minutes and fix the client-side part.

## Prove it's DNS
```powershell
Test-NetConnection 10.20.1.15 -Port 443       # by IP: works?
Resolve-DnsName intranet.corp.example.com     # by name: fails / wrong IP?
nslookup intranet.corp.example.com 10.20.0.10 # ask a specific DNS server directly
```
IP works, name fails → DNS. Name resolves to the wrong address → stale
record, hosts file, wrong server or split-DNS issue.

## Client checks
- Which DNS servers? `Get-DnsClientServerAddress` / `ipconfig /all`.
  Home router or public DNS (8.8.8.8) while on VPN can't resolve internal
  names.
- **Cache**: `ipconfig /displaydns`, `ipconfig /flushdns` (also browser:
  `edge://net-internals/#dns` → Clear host cache).
- **Hosts file**: `%windir%\System32\drivers\etc\hosts` — leftover test
  entries or malware redirects.
- **Suffix**: short names (`intranet`) need the DNS suffix search list —
  `Get-DnsClient | Select InterfaceAlias, ConnectionSpecificSuffix` and
  the global suffix list; VPN usually adds it.
- **NRPT** (Name Resolution Policy Table) on Always On VPN/DirectAccess:
  `Get-DnsClientNrptPolicy` — rules send `corp.example.com` to internal DNS.
- macOS: `scutil --dns`, flush with
  `sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder`.

## Common scenarios
| Symptom | Cause |
|---|---|
| Internal sites fail on VPN, internet fine | VPN not pushing DNS / split-tunnel DNS config |
| Site moved, some users still hit old server | cached record (TTL) — flush, wait TTL |
| Works by FQDN not short name | suffix search list |
| Everything fails, IPs work | DNS server unreachable / wrong |
| One site redirects to weird page | hosts file / malware / DNS hijack on home router |

## Gotchas
- `ping` uses the full resolver (including hosts and LLMNR/NetBIOS);
  `nslookup` queries DNS only — results can differ.
- Secure DNS (DoH) in browsers bypasses corporate DNS — check policy.

## Verify
`Resolve-DnsName` returns the correct address from the intended server, and
the app/site opens by name after cache clears.
