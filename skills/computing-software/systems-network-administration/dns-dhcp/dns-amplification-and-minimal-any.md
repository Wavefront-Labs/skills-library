---
id: computing-software.systems-network-administration.dns-dhcp.dns-amplification-and-minimal-any
name: dns-amplification-and-minimal-any
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns-security, dns-amplification, minimal-any, rfc8482, open-resolver, ddos, rrl]
level: practitioner
status: verified
description: "Keep your DNS servers out of amplification attacks: close open resolvers, minimal ANY (RFC 8482), RRL, minimal-responses, and checking exposure from the internet."
sources:
  - https://www.rfc-editor.org/rfc/rfc8482
  - https://www.cisa.gov/news-events/alerts/2013/03/29/dns-amplification-attacks
  - https://bind9.readthedocs.io/en/latest/reference.html#namedconf-statement-minimal-any
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DNS amplification and minimal ANY

Attackers send small UDP queries with the victim's spoofed source address to DNS servers that
return large answers, so a small query elicits a large response aimed at the victim (RFC 8482 section 9 calls QTYPE=ANY a
frequent reflection-attack query).

## 1. No open resolvers
Recursive service only for your clients:
```
# BIND
acl internal { 10.0.0.0/8; 192.168.0.0/16; 2001:db8::/32; };
options { recursion yes; allow-recursion { internal; }; allow-query-cache { internal; }; };
# Unbound
access-control: 0.0.0.0/0 refuse
access-control: 10.0.0.0/8 allow
```
Authoritative servers: `recursion no`.

## 2. Minimal ANY
ANY queries are a favourite amplifier. RFC 8482 lets servers answer with one RRset (or a synthetic
HINFO) instead of everything:
```
options { minimal-any yes; };           # BIND 9.11+
```
BIND's `minimal-any` (default no) applies to ANY over UDP and also turns on `minimal-responses` for those queries; the RRset
returned is the first one found, not necessarily the smallest. RFC 8482 section 8 records Cloudflare's HINFO answer
(2015), NSD 4.1 subset answers (2016) and BIND 9.11 single-RRset answers; Knot DNS 2.9.4 answers ANY over UDP with one
RRset plus RRSIG instead of a truncated reply (Knot NEWS). Legacy tools that relied on ANY will see less data.

## 3. Smaller answers
`minimal-responses yes;` omits optional authority/additional data; BIND's `edns-udp-size` and `max-udp-size` both
default to 1232 (valid 512 to 4096).

## 4. Response rate limiting (authoritative)
```
options { rate-limit { responses-per-second 10; window 5; slip 2; }; };
```
Identical responses to the same client netblock beyond the rate are dropped, except that with `slip 2` (the default)
every second one gets a small answer: TC=1 if the request had no cookie (so a real client retries over TCP, which
cannot be spoofed) or BADCOOKIE with a server cookie if it did. See response-rate-limiting-rrl.

## 5. Network
BCP 38 ingress filtering on your edge stops spoofed sources leaving your network; ask upstreams to
do the same.

## Check exposure
```
dig @<your-public-ip> example.com A +norec      # from outside: should be REFUSED for non-authoritative names
dig @<your-public-ip> isc.org ANY               # small answer if minimal-any is on
nmap -sU -p 53 --script dns-recursion <ip>
```
Shadowserver publishes network reports on open resolvers; subscribe for your networks.

## Verify
- [ ] External recursion test returns REFUSED, ANY answers are small, and RRL counters
  (`rndc stats`, RateDropped) move during a test.
