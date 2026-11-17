---
id: computing-software.systems-network-administration.network-design.ipv6-privacy-temporary-addresses
name: ipv6-privacy-temporary-addresses
category: computing-software
field: systems-network-administration
product: network-design
tags: [ipv6, privacy-extensions, temporary-address, rfc8981, stable-privacy, slaac, logging, ipv6-design]
level: practitioner
status: verified
description: "Plan for IPv6 temporary and stable-privacy addresses: RFC 8981/7217 behaviour, why hosts have many addresses, impact on logging, ACLs and forensics, and OS controls."
sources:
  - https://www.rfc-editor.org/rfc/rfc8981
  - https://www.rfc-editor.org/rfc/rfc7217
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/configure-ipv6-in-windows
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IPv6 privacy and temporary addresses

## What hosts do by default
With SLAAC a host typically holds, per prefix:
- a stable address: either RFC 7217 "stable privacy" (opaque but constant per network) or EUI-64
  (MAC-derived); which one depends on the OS and its configuration (the Linux kernel default
  `addr_gen_mode` is 0, EUI-64),
- one or more temporary addresses (RFC 8981, which obsoletes 4941) that rotate and are preferred for
  outgoing connections; RFC 8981 defaults are a 1 day preferred and 2 day valid lifetime,
- a link-local address.
So one laptop may show 4-6 IPv6 addresses, and its outbound source changes over time.

## Impact on operations
- Logs and SIEM: the IPv6 source in firewall/proxy logs maps to a host only for a few hours or days.
  Keep NDP/neighbour table history (switch-side device tracking, router neighbour tables polled
  into your NMS, or a dedicated NDP monitor) to map address -> MAC -> port.
- ACLs per host by IPv6 address do not work for clients; use identity-based policy (802.1X, SGT,
  user-ID on firewalls) or DHCPv6 with reservations for the few devices that need fixed addresses.
- Servers: disable temporary addresses and use static/DHCPv6 reserved addresses so services and DNS
  records stay fixed.

## OS controls
```
# Linux (sysctl)
net.ipv6.conf.eth0.use_tempaddr = 0        # <=0 off, 1 generate but prefer public, >1 prefer temporary
net.ipv6.conf.eth0.addr_gen_mode = 3       # 2 = RFC 7217 using stable_secret, 3 = same with a random secret if unset
                                           # (kernel default 0 = EUI-64; kernel default use_tempaddr is 0 for most devices)
# Windows
netsh interface ipv6 set privacy state=disabled
netsh interface ipv6 set global randomizeidentifiers=disabled
```
Other client OSes: check each vendor's documentation; design for temporary addresses being on.
(The Windows `netsh` option names above come from the built-in `set privacy /?` and `set global /?`
help; they were not applied here because they change system settings.)

## Enterprise options
- DHCPv6 stateful (M flag, no A flag in prefix info) for managed fleets whose OSes support DHCPv6
  address assignment; confirm per client OS, since a client without it needs SLAAC.
- Keep SLAAC + privacy and rely on NDP logging and identity-based controls (the more common modern
  choice).

## Verify
- [ ] For a test client, you can map an IPv6 address seen in a firewall log yesterday to its MAC and
  switch port from stored neighbour data.
