---
id: computing-software.systems-network-administration.dns-dhcp.dns-timeouts-fragmentation-and-blocked-responses
name: dns-timeouts-fragmentation-and-blocked-responses
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, dns-fragmentation, edns, dns-timeout, firewall, mtu]
level: practitioner
status: docs-checked
description: "Diagnose DNS timeouts caused by fragmented large UDP responses, firewalls dropping fragments or TCP 53, and inspection devices truncating EDNS answers."
sources:
  - https://www.rfc-editor.org/rfc/rfc9715
  - https://bind9.readthedocs.io/en/latest/reference.html#namedconf-statement-edns-udp-size
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DNS timeouts and blocked/fragmented responses

Symptom: some names (DNSSEC-signed, large TXT, many A records) time out while small ones work.

## Why
UDP responses larger than the path MTU fragment if the client advertises a big EDNS buffer. Firewalls and other middleboxes may drop fragments (the BIND ARM describes broken firewalls that block fragmented packets), so the response never arrives. RFC 9715 recommends a maximum DNS/UDP payload of 1400 bytes and says fragmented responses should be discarded and the query retried over TCP. If TCP 53 is blocked too, the lookup fails.

## Test
```
dig +dnssec +bufsize=4096 example.com DNSKEY @ns1.example.com     # large; does it arrive?
dig +dnssec +bufsize=1232 example.com DNSKEY @ns1.example.com     # TC=1 expected if too large
dig +tcp example.com DNSKEY @ns1.example.com                      # TCP path works?
dig +norec +ignore +bufsize=4096 example.com TXT @server           # +ignore: do not retry over TCP, so you can see the TC flag
```
- Timeout with 4096 but TC with 1232 and success over TCP: fragmentation problem.
- Timeout over TCP: TCP 53 blocked.

## Capture
```
tcpdump -ni any 'port 53'                                 # capture on both sides of the suspected middlebox
```
Fragments leaving the server but not reaching the client point to the middlebox.

## Fixes
- BIND: `edns-udp-size` (advertised buffer in queries to authoritative servers) and `max-udp-size` (maximum response size sent) both default to 1232, valid range 512 to 4096; unbound: `edns-buffer-size` defaults to 1232 (the DNS Flag Day 2020 recommendation, per its documentation). Setting 512 avoids path MTU problems but causes excessive TCP fallback.
- Allow TCP 53 inbound and outbound for DNS servers.
- Disable firewall DNS inspection features that enforce a 512-byte limit.
- Reduce response size where you control the zone (smaller keys and fewer records per name).

## Verify
- [ ] The large query succeeds via UDP with bufsize 1232 (TC then TCP fallback) from the affected client network.

## Checked

Date: 2026-10-26. Documentation: BIND ARM (edns-udp-size, max-udp-size), Unbound unbound.conf docs (edns-buffer-size), BIND dig man page (+bufsize, +ignore, +norec, +tcp), RFC 9715 text, read 2026-10-26. Confirmed: BIND and Unbound 1232 defaults, valid range 512-4096, RFC 9715 1400-byte recommendation and TCP retry advice. Removed the unconfirmed 1472 and old-default-4096 figures, Cisco ASA command and RFC 7766 attribution; the dnsflagday.net page itself was not read.

Method: documentation only; no commands were run.
