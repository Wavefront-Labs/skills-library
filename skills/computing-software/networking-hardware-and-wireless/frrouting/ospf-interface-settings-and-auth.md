---
id: computing-software.networking-hardware-and-wireless.frrouting.ospf-interface-settings-and-auth
name: ospf-interface-settings-and-auth
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, ospfd, ospf, hello-interval, dead-interval, network-type, message-digest, key-chain, pacing]
level: practitioner
status: docs-checked
description: "Tune FRR OSPFv2 per-interface behaviour: cost, hello and dead timers, network type, priority, passive, MD5 and key-chain authentication, BFD, and adjacency and LSA pacing."
sources:
  - https://docs.frrouting.org/en/latest/ospfd.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OSPFv2 interface settings and authentication
Interface commands:
- `ip ospf area AREA [ADDR]`; `ip ospf cost (1-65535)`.
- `ip ospf hello-interval (1-65535)` default 10 s; `ip ospf dead-interval (1-65535)` default 40 s.
- `ip ospf dead-interval minimal hello-multiplier (2-20)` gives a 1 s dead interval with sub-second hellos and overrides hello-interval.
- `ip ospf network broadcast|non-broadcast|point-to-multipoint [delay-reflood|non-broadcast]|point-to-point [dmvpn]`.
- `ip ospf priority (0-255)` default 1; 0 means never DR.
- `ip ospf retransmit-interval (1-65535)` default 5; `ip ospf transmit-delay (1-65535)` default 1.
- `ip ospf passive [A.B.C.D]`; `ip ospf bfd [quick]`, `ip ospf bfd profile NAME`.
- Pacing: `ip ospf adjacency-pacing static (1-65535)|dynamic`, `ip ospf lsa-pacing` (initial-gap default 20 ms, min-gap 20, max-gap 1000, factor 2).

Authentication:
- `ip ospf authentication message-digest` selects MD5 HMAC on the interface (also `area AREA authentication [message-digest]`; the per-interface setting overrides the per-area one).
- `ip ospf message-digest-key KEYID md5 KEY`; KEY up to 16 characters, truncated beyond.
- `ip ospf authentication-key KEY` up to 8 characters, deprecated.
- `ip ospf authentication key-chain NAME`.
- `compatible rfc7474` (default enabled) is strict sequence validation for MD5 and HMAC; per interface `ip ospf compatible rfc7474 enable|disable`.

## Checked

2026-11-04. Confirmed against the FRR OSPFv2 page (ospfd): interface timers and defaults, priority, retransmit and transmit-delay, network types, BFD, adjacency and LSA pacing defaults, authentication key lengths, key-chain and rfc7474 commands. Fixed the plain interface authentication command, which has only the message-digest form.
Method: documentation only; no commands were run.
