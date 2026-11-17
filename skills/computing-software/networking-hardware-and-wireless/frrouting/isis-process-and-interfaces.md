---
id: computing-software.networking-hardware-and-wireless.frrouting.isis-process-and-interfaces
name: isis-process-and-interfaces
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, isisd, isis, net, metric-style, circuit-type, overload-bit, lsp-timers, redistribute]
level: practitioner
status: docs-checked
description: "Configure FRR isisd: router isis NET, levels, metric style, interface circuits, hello and metric settings, passwords, overload bit, LSP and SPF timers, redistribution, show."
sources:
  - https://docs.frrouting.org/en/latest/isisd.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IS-IS process and interfaces
Process (`router isis WORD [vrf NAME]`):
- `net XX.XXXX....XXX.XX`; `is-type level-1|level-1-2|level-2-only`; `metric-style narrow|transition|wide` (default wide).
- `hostname dynamic`; `area-password` / `domain-password clear|md5 PASSWORD`.
- `set-overload-bit`, `set-overload-bit on-startup (0-86400)`; `attached-bit receive ignore|send`; `lsp-mtu (128-4352)`.
- Timers, optionally `level-1|level-2`: `lsp-gen-interval (1-120)`, `lsp-refresh-interval (1-65235)`, `max-lsp-lifetime (350-65535)`, `spf-interval (1-120)`.
- `redistribute ipv4|ipv6 table (1-65535) level-1|level-2 [metric N|route-map WORD]`; `default-information originate ipv4|ipv6 level-1|level-2 [always]`.

Interface (after `ip router isis WORD` or `ipv6 router isis WORD`):
- `isis circuit-type level-1|level-1-2|level-2-only`; `isis network point-to-point` (default broadcast); `isis passive`.
- `isis hello-interval (1-600)`, `isis hello-multiplier (2-100)`, `isis csnp-interval (1-600)`, `isis psnp-interval (1-120)`, `isis priority (0-127)`; all accept a level.
- `isis metric [level] N` (0-63 narrow, 0-16777215 wide).
- `isis password clear|md5 PASSWORD`; `isis three-way-handshake` default on for P2P; `isis bfd [profile NAME]`.

Show: `show isis summary|interface|neighbor|database|topology|route|hostname` (accept `vrf NAME|all`). `debug isis` options include adj-packets, spf-events, update-packets.

## Checked

2026-11-04. Confirmed against the FRR IS-IS page: process, timer and interface commands with their ranges and defaults, three-way handshake default, isis bfd, show and debug commands. Nothing changed.
Method: documentation only; no commands were run.
