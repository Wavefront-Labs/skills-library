---
id: computing-software.digital-privacy-hygiene.vpn-tools.verifying-which-dns-resolver-answers
name: verifying-which-dns-resolver-answers
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, dns-resolver-verification, dns-leak-test, encrypted-dns]
level: practitioner
status: draft
description: "Verify which DNS resolver is actually answering and whether queries are encrypted, using resolver test pages and dig TXT checks."
sources:
  - "https://one.one.one.one/help/"
  - "https://test.nextdns.io/"
  - "https://docs.quad9.net/"
  - "https://www.dnsleaktest.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Verifying which DNS resolver answers

**Goal:** confirm your encrypted DNS / VPN DNS setting actually took effect, rather than trusting the settings page.

## Browser pages
- Cloudflare: `one.one.one.one/help` shows "Using DNS over HTTPS/TLS" yes/no.
- NextDNS: `test.nextdns.io` shows status ok, protocol (DOH/DOT) and profile.
- Quad9: `on.quad9.net` says yes/no.
- dnsleaktest.com extended test lists resolver IPs and owners.

## Command line
```
dig +short txt proto.on.quad9.net                       # Quad9: doh / dot / udp
dig +short TXT o-o.myaddr.l.google.com @ns1.google.com   # returns the resolver IP that reached Google
dig +short TXT whoami.ds.akahelp.net                     # Akamai: shows resolver ("ns") IP
nslookup -type=txt o-o.myaddr.l.google.com ns1.google.com   # Windows equivalent
```
Look up the returned IP's owner (whois/ipinfo): ISP name = not using your chosen resolver.

## Interpreting
| Result | Meaning |
|---|---|
| Resolver = ISP | OS/browser setting not applied, or router intercepting port 53 |
| Resolver = VPN provider while connected | Good |
| Mixed results | Some queries leak (IPv6, another interface) |

## Gotchas
- The browser may use its own DoH while the OS uses plaintext; test both in browser and terminal.
- Some routers/ISPs transparently redirect port 53; encrypted DNS (DoT/DoH) bypasses that.
