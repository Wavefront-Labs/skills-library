---
id: computing-software.systems-network-administration.dns-dhcp.source-port-randomization
name: source-port-randomization
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, source-port-randomization, cache-poisoning, kaminsky, resolver-security]
level: practitioner
status: verified
description: "Verify and protect resolver source port randomisation against Kaminsky-style cache poisoning, including NAT/firewall de-randomisation and testing tools."
sources:
  - https://www.rfc-editor.org/rfc/rfc5452
  - https://www.kb.cert.org/vuls/id/800113
  - https://bind9.readthedocs.io/en/latest/reference.html#namedconf-statement-query-source
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Source port randomisation

Resolvers protect against off-path spoofed responses by using random 16-bit query IDs AND random
UDP source ports (RFC 5452), at most about 32 bits of combined entropy (16-bit ID plus up to ~16 bits of port).
Microsoft's July 2008 bulletin MS08-037 introduced the socket-pool randomisation for Windows DNS.

## Server config
- BIND: the ARM default is `query-source address *;` (random UDP source port); the address applies to UDP and TCP,
  the port only to UDP, and TCP queries always use a random unprivileged port. A fixed `port` in `query-source`
  disables randomisation. The `port` keyword and `use-v4-udp-ports` / `avoid-v4-udp-ports` (and the v6 forms) were
  removed in the 9.21.2 development release (release notes), so they exist only on older branches.
- Unbound: `outgoing-port-permit` / `outgoing-port-avoid` (default: unassigned ports above 1024; more permitted
  ports increase resilience), `outgoing-range` (file descriptors, i.e. ports, per thread; default depends on build).
- Windows DNS: a socket pool provides the randomisation; its size is the registry value `SocketPoolSize` under
  `HKLM\System\CurrentControlSet\Services\DNS\Parameters` and the DNS service must be restarted after a change
  (MS08-037). Confirm the default, maximum and the `dnscmd` spelling in current Microsoft documentation.

## NAT and firewalls
RFC 5452 warns that the effect of source port randomisation "may be dramatically reduced by NAT devices that either
serialize or limit in volume the UDP source ports". Place resolvers on public addresses or use 1:1 NAT without port
translation, and check with the test below from behind the device.

## Test
DNS-OARC's old command-line test (`dig +short porttest.dns-oarc.net TXT`, rating GOOD, FAIR or POOR) was deprecated on
2023-06-01 in favour of its Check My DNS web service, and the name returned NXDOMAIN when queried in this review. Use
Check My DNS (it rates GREAT, GOOD or POOR; POOR means ID or port randomness is weak somewhere on the path) and also
check with a packet capture that your resolver's outgoing queries use varied source ports.

## Related defences
DNSSEC validation (only real protection for signed zones), 0x20 case randomisation
(`use-caps-for-id` in Unbound, default no, experimental implementation of draft dns-0x20), DNS cookies, limiting `max-udp-size` to reduce fragmentation attacks.

## Verify
- [ ] Check My DNS reports GREAT from the resolver's egress and query IDs/ports look random in a capture.
