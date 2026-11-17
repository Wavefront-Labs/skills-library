---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.detecting-dns-over-https-and-dot
name: detecting-dns-over-https-and-dot
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [dns-over-https, dns-forensics, encrypted-traffic-analysis, c2-beaconing, dfir]
level: advanced
status: verified
description: "Detect DNS-over-HTTPS and DNS-over-TLS that bypass enterprise resolvers: known resolver endpoints, port 853, TLS SNI/JA4, browser and malware DoH settings."
sources: ["https://datatracker.ietf.org/doc/html/rfc8484", "https://datatracker.ietf.org/doc/html/rfc7858", "https://attack.mitre.org/techniques/T1071/004/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Detecting DNS-over-HTTPS and DoT

**Goal:** encrypted DNS hides lookups from your DNS logs and RPZ blocks. Malware (and browsers)
use it to resolve C2 domains invisibly. Detect it and decide policy.

## DNS-over-TLS (RFC 7858)
- TCP **853** to resolvers (1.1.1.1, 8.8.8.8, 9.9.9.9 ...). Easy: `tcp.port == 853` or firewall logs on 853.

## DNS-over-HTTPS (RFC 8484)
- HTTPS on 443 to DoH endpoints; looks like web traffic. Indicators:
  - **SNI** of known DoH providers: `cloudflare-dns.com`, `mozilla.cloudflare-dns.com`, `dns.google`, `dns.quad9.net`, `doh.opendns.com`, `dns.nextdns.io`, plus many smaller ones (maintain a list).
  - Connections to resolver IPs on 443 without a preceding DNS lookup for them (hard-coded IP use).
  - Traffic pattern: many small request/response pairs on a long-lived HTTP/2 connection.
  - Wireshark (if decrypted or cleartext): the HTTP exchange has content-type `application/dns-message` (RFC 8484) and Wireshark decodes the body as DNS, labelled `DoH` in the Protocol column; the `dns` filter matches it.
```text
tls.handshake.extensions_server_name in {"cloudflare-dns.com", "dns.google", "dns.quad9.net", "mozilla.cloudflare-dns.com"}
tcp.port == 853
```
Set members are comma-separated (a space-separated set is a syntax error in Wireshark 4.4.1).
- QUIC-based DoQ (UDP 853) and DoH over HTTP/3 (UDP 443) also exist.

## Host side
- Browser settings: Firefox `network.trr.mode` (prefs.js), Chrome/Edge "Use secure DNS" policies (`DnsOverHttpsMode`).
- Windows 11 native DoH: `netsh dns show encryption`, registry `Dnscache\Parameters\DohWellKnownServers`.
- Malware: hard-coded DoH URLs in strings/configs (common in modern implants).

## Response
- Block known DoH/DoT endpoints at egress and use the Firefox canary domain (`use-application-dns.net` returning NXDOMAIN) to disable automatic DoH; enforce enterprise DNS via policy.
- Hosts still using DoH after policy = investigate the process (EDR network events with process name).

## Gotchas
- Lists of DoH endpoints are never complete; self-hosted DoH on attacker domains looks like normal HTTPS - rely on process-level telemetry.

## Verify
Hosts and processes using encrypted DNS are enumerated and each is explained or contained.

## Checked
Run on Wireshark 4.4.1 with a synthetic capture (ClientHellos with the listed SNIs on 443 and 853, plus a cleartext
`application/dns-message` POST): the SNI set filter (comma form) and `tcp.port == 853` matched exactly the intended
frames, and the DNS body decoded as `DoH` and matched `dns`. `netsh dns show encryption` and the
`Dnscache\Parameters\DohWellKnownServers` registry key exist on this Windows 11 host. Firefox `network.trr.mode`
(Mozilla policy-templates page), Chrome `DnsOverHttpsMode` (Chromium policy definition), the canary domain with
`NS_ERROR_UNKNOWN_HOST` handling (Firefox `DoHHeuristics.sys.mjs`), port 853 for DoT (RFC 7858) and for DoQ
(RFC 9250) and `application/dns-message` (RFC 8484) were read from the sources. The provider hostnames all resolve
(`nslookup`). The list of providers is illustrative, not complete.
