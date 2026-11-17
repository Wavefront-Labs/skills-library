---
id: computing-software.cybersecurity-defensive.network-defence.amplification-prevention
name: amplification-prevention
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [amplification-prevention, reflection-attacks, bcp38, source-address-validation, open-resolver, ntp-monlist, memcached, ddos-mitigation]
level: practitioner
status: gated
description: "Stop your network being used for reflection/amplification DDoS: BCP 38 egress filtering, closing open resolvers, NTP, SSDP, memcached, SNMP and CLDAP exposure, and monitoring."
sources: ["https://datatracker.ietf.org/doc/html/rfc2827", "https://www.cisa.gov/news-events/alerts/2014/01/17/udp-based-amplification-attacks", "https://www.shadowserver.org/what-we-do/network-reporting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Amplification and reflection prevention

Reflection attacks send small spoofed UDP requests to services that reply with large responses toward the
victim. Prevent your infrastructure from being either the spoof source or the reflector.

## 1. Anti-spoofing (BCP 38 / BCP 84)
- Egress filter: only packets with source addresses from your own prefixes leave your network.

## 2. Close reflectors (common amplification factors)
| Service | Port | Fix |
|---|---|---|
| DNS open resolver | 53 | Recursion only for internal clients (see dns-resolver-hardening); RRL on authoritative servers |
| NTP monlist | 123 | NTP 4.2.7+; `restrict default kod nomodify notrap nopeer noquery`; disable mode 6/7 queries |
| Memcached | 11211/udp | Disable UDP (`-U 0`), bind to localhost/private only |
| SSDP/UPnP | 1900 | Block from internet; disable UPnP on edge devices |
| CLDAP | 389/udp | Never expose DCs/LDAP to the internet |
| SNMP | 161 | v3 only, no internet exposure |
| Chargen/QOTD, WS-Discovery 3702, ARMS 3283, TFTP | various | Disable or firewall |

(gated: unconfirmed, source is paywalled or blocked)

## 3. Monitor
- External scans of your space (Shadowserver network reports) for open UDP services.
- NetFlow: high outbound UDP from these ports to many destinations.

## Verify
- [ ] Shadowserver/attack surface reports show no open reflectors in your ranges.
- [ ] Egress filter test: packet with spoofed source dropped at edge.

## Checked
2026-10-28. Confirmed against official pages: ingress/egress source filtering (RFC 2827) and Shadowserver network reporting.
Removed or rewritten: the uRPF command, MANRS and Spoofer lines (MANRS page 404), and the dead MANRS source. The reflector table (services, ports and fixes) is gated because its source, the CISA alert, returns 403 to scripts.
Method: documentation only; no commands were run.
