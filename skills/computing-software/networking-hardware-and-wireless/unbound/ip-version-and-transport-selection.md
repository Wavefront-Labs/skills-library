---
id: computing-software.networking-hardware-and-wireless.unbound.ip-version-and-transport-selection
name: ip-version-and-transport-selection
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, do-ip4, do-ip6, prefer-ip6, do-udp, do-tcp, tcp-upstream]
level: practitioner
status: docs-checked
description: "Enable or disable IPv4, IPv6, UDP and TCP for Unbound, choose the preferred upstream IP version, and force TCP upstream."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/getting-started/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ip version and transport selection
- `do-ip4` and `do-ip6` (default yes) enable answering and issuing queries over that IP version. `do-ip6: no` disables IPv6 transport only; A/AAAA record contents are unaffected.
- `do-udp` and `do-tcp` (default yes) do the same for each transport.
- `prefer-ip6: yes` prefers IPv6 to upstream nameservers; `prefer-ip4: yes` prefers IPv4, useful when an IPv6 /64 has a poor reputation. Both default no.
- `tcp-upstream: yes` uses TCP only for upstream queries, mainly for tunnelling; per-zone control exists on forward and stub zones.
- `udp-upstream-without-downstream: yes` allows UDP upstream even with `do-udp: no`.
- `do-not-query-address` blocks queries to given addresses; the getting-started guide uses `0.0.0.0/0` to block outgoing IPv4.
- `tcp-mss` and `outgoing-tcp-mss` cap TCP MSS to work around path MTU problems.

## Checked

2026-11-08. Read do-ip4, do-ip6, do-udp, do-tcp, prefer-ip4, prefer-ip6, tcp-upstream, udp-upstream-without-downstream and the MSS options in the unbound.conf manual and the Network Configuration part of the getting-started guide. Claims confirmed.

Method: documentation only; no commands were run.
