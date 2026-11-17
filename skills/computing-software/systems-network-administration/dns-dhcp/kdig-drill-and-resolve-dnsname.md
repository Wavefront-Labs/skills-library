---
id: computing-software.systems-network-administration.dns-dhcp.kdig-drill-and-resolve-dnsname
name: kdig-drill-and-resolve-dnsname
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, dns-troubleshooting, dig, kdig, drill, resolve-dnsname, nslookup, windows-dns-client-cache, ipconfig-flushdns, get-dnsclientcache, dns-over-tls, edns-client-subnet, dnssec]
level: practitioner
status: docs-checked
description: "Pick the right DNS query tool: kdig for DoT/DoH and EDNS options, drill for DNSSEC chasing and tracing, and Resolve-DnsName with the Windows DNS client cache."
sources:
  - https://www.knot-dns.cz/docs/latest/html/man_kdig.html
  - https://github.com/NLnetLabs/ldns/blob/develop/drill/drill.1.in
  - https://learn.microsoft.com/en-us/powershell/module/dnsclient/resolve-dnsname
  - https://learn.microsoft.com/en-us/powershell/module/dnsclient/clear-dnsclientcache
  - https://learn.microsoft.com/en-us/powershell/module/dnsclient/get-dnsclientnrptpolicy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kdig, drill and Resolve-DnsName

## kdig (Knot DNS utilities)
dig-like syntax plus modern transports and options:
```
kdig @9.9.9.9 +tls example.org                       # DoT (opportunistic privacy profile, RFC 7858 4.1)
kdig @1.1.1.1 +https example.org                     # DoH
kdig @resolver +tls-ca +tls-hostname=resolver.example.org example.org   # validate the cert and hostname
kdig @8.8.8.8 +subnet=203.0.113.0/24 www.example.org # EDNS Client Subnet: see geo answers
kdig +dnssec +multiline DNSKEY example.org
kdig -t AXFR example.org @ns1 -y hmac-sha256:xfr-key:<SECRET>
```
- `+tls-ca` without a value uses the system certificate store; with `+tls-hostname` it checks the server name.
- `-y [alg:]name:key` takes a TSIG key (default algorithm hmac-sha256, key in Base64); `-k keyfile` reads it from a file.
- `+https` needs libnghttp2; `+https-get` uses GET instead of POST; `+quic` queries over DNS-over-QUIC.
- `+validate` is a debugging aid, not a security feature: kdig does not obtain or validate the whole trust chain.

## drill (ldns)
```
drill -T example.org             # trace from the root down
drill -S example.org             # chase signatures to a known key: shows the DNSSEC chain of trust
drill -D example.org             # enable DNSSEC in the query
drill -TD example.org            # DNSSEC trace (needs ldns built with OpenSSL)
```

## Windows: Resolve-DnsName
```powershell
Resolve-DnsName www.example.org
Resolve-DnsName www.example.org -Server 10.0.0.53 -Type AAAA -DnsOnly
Resolve-DnsName example.org -Type MX -NoHostsFile
Resolve-DnsName example.org -DnssecOk
Get-DnsClientCache | Where-Object Entry -like '*example*'
Clear-DnsClientCache                               # = ipconfig /flushdns
Get-DnsClientNrptPolicy                            # Name Resolution Policy Table rules per namespace
Get-DnsClientServerAddress
```
`Resolve-DnsName` is functionally similar to `nslookup`. Without `-DnsOnly` it can also issue LLMNR and NetBIOS
queries; `-DnsOnly` restricts it to the DNS protocol. `-NoHostsFile` skips the hosts file, `-DnssecOk` sets the
DO bit, and `-Server` queries a specific server.

## Verify
- [ ] Tool choice matches the question: specific server (dig/kdig `@server`), DNSSEC chain (drill -S), encrypted
  transport (kdig), Windows resolver behaviour including NRPT and the client cache (Resolve-DnsName, Get-DnsClientCache).

## Checked
Date: 2026-10-28.
Confirmed against the kdig man page (Knot DNS 3.6.2: +tls, +tls-ca, +tls-hostname, +https, +https-get, +quic,
+subnet, +dnssec, +multiline, +validate, -t, -y, -k, AXFR), the ldns drill.1.in man source (-T, -S, -D, -TD) and the
Learn pages for Resolve-DnsName, Clear-DnsClientCache (equivalent to `ipconfig /flushdns`) and Get-DnsClientNrptPolicy.
Removed: package names (`knot-dnsutils`, `knot-utils`), the claim that Resolve-DnsName follows the exact application
path, the nslookup pitfalls (suffix search, "Non-authoritative", PTR timeout, no DNSSEC support: not on the fetched
nslookup page), the DirectAccess/VPN description of NRPT, and the `delv`/`resolvectl` mention.
Method: documentation only; no commands were run.
