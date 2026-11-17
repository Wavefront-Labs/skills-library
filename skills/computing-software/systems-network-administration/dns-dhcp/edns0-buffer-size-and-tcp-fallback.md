---
id: computing-software.systems-network-administration.dns-dhcp.edns0-buffer-size-and-tcp-fallback
name: edns0-buffer-size-and-tcp-fallback
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, edns, edns-buffer-size, dns-over-tcp, tc-bit, dns-flag-day, fragmentation, firewall]
level: practitioner
status: verified
description: "Handle large DNS responses: EDNS0 UDP buffer sizes (1232 default), truncation and TCP fallback, firewalls that break port 53/TCP or fragments, and testing with dig."
sources:
  - https://www.rfc-editor.org/rfc/rfc6891
  - https://www.rfc-editor.org/rfc/rfc7766
  - https://www.dnsflagday.net/2020/
  - https://www.dnsflagday.net/2020/
  - https://bind9.readthedocs.io/en/latest/reference.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EDNS0 buffer size and TCP fallback

Classic DNS over UDP was limited to 512 bytes. EDNS0 (RFC 6891) lets clients advertise a bigger UDP
buffer. DNSSEC, many TXT records and large NS/A sets exceed 512 bytes routinely.

## What happens with a large answer
1. Client advertises a buffer (e.g. 1232).
2. If the answer fits, server sends it over UDP.
3. If not, server sends a truncated response with `TC=1`.
4. Client retries over TCP port 53 (RFC 7766: all general-purpose DNS implementations MUST support
   both UDP and TCP).

## The 1232 recommendation
DNS Flag Day 2020: use an EDNS buffer of 1232 bytes (the 1280-byte IPv6 minimum MTU minus 48 bytes of
IPv6 and UDP headers) so responses fit in one packet without fragmentation. Large UDP buffers (4096) risk IP fragmentation, which DNS Flag Day 2020 describes
as the cause of operational and security problems.
BIND's `edns-udp-size` and `max-udp-size` and Unbound's `edns-buffer-size` all default to 1232 in their
current manuals; check Knot and PowerDNS in their own documentation.
```
# BIND (edns-udp-size: size advertised in queries BIND sends; max-udp-size: size of UDP answers it sends)
options { edns-udp-size 1232; max-udp-size 1232; };
# Unbound
edns-buffer-size: 1232
```

## Test
```
dig +bufsize=1232 +dnssec DNSKEY example.com @ns1.example.com    # see MSG SIZE rcvd and flags
dig +bufsize=512 +dnssec DNSKEY example.com                      # expect tc, dig retries over TCP
dig +tcp example.com @10.0.0.53
dig +notcp +ignore +bufsize=512 TXT example.com                  # show the truncated UDP reply itself
```
dig retries over TCP after a truncated UDP reply unless `+ignore` is set (dig manual).
Reproduced with dnspython against a local CoreDNS zone holding a 1,572-byte TXT answer (7 strings):
without EDNS, with a 512 buffer and with a 1232 buffer the UDP reply had TC=1 (460, 471 and 1,110
bytes, truncated); with a 4096 buffer the full answer came back over UDP; over TCP all 7 records
arrived; `dns.query.udp_with_fallback` retried over TCP automatically.

## Common breakage
- Firewalls allowing only UDP 53: large answers fail after TC (SERVFAIL or timeout at the client).
  Permit TCP 53 to and from resolvers and authoritative servers.
- Firewalls or IPS devices that limit UDP DNS messages to 512 bytes (check the device's DNS
  inspection settings).
- Fragmented UDP replies being dropped when large buffers (for example 4096) are advertised.

## Verify
- [ ] A large signed response (DNSKEY of a signed zone) resolves through your resolver, and dig over
  TCP works to every authoritative and recursive server you run.
