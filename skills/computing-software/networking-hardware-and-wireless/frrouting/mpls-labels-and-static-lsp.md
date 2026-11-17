---
id: computing-software.networking-hardware-and-wireless.frrouting.mpls-labels-and-static-lsp
name: mpls-labels-and-static-lsp
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, zebra, mpls, static-lsp, label-manager, dynamic-block, lsr, ler]
level: advanced
status: docs-checked
description: "Configure MPLS label push, swap and pop in FRR zebra with static routes and mpls lsp, reserve a dynamic label block, and allow recursive LSP resolution."
sources:
  - https://docs.frrouting.org/en/latest/zebra.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MPLS labels and static LSPs
An LSR forwards labeled traffic; a LER sits at the MPLS edge and pushes or pops labels.

- Push: `ip route NETWORK MASK GATEWAY|INTERFACE label LABEL`; verify with `show ip route`.
- Swap and pop: `mpls lsp INCOMING_LABEL GATEWAY OUTGOING_LABEL|explicit-null|implicit-null`. Labels range 16-1048575; `explicit-null` sends an explicit-null label header; with `implicit-null` the outgoing packet is IP without an MPLS header.
- `show mpls table` shows inbound and outbound labels and nexthops.
- Interface-level `mpls <enable|disable>` is Linux only.

Label manager: it prevents one label being used by multiple daemons. Static requests ask for exact values or ranges (e.g. IS-IS SR blocks); dynamic requests ask for a range size (e.g. `bgp l3vpn export auto`). Default range is 16-1048575.
- `mpls label dynamic-block (16-1048575) (16-1048575)` reserves a range for dynamic allocation; static requests inside it are rejected.
- `show debugging label-table [json]` shows chunks by protocol.

`mpls fec nexthop-resolution` lets labeled-route LSPs resolve through recursive nexthops; without it LSPs need directly connected nexthops.

Debug: `debug zebra mpls [detailed]`.

## Checked

2026-11-08. Read the MPLS section of the FRR zebra page: push, swap and pop forms, label range, show mpls table, label chunks, dynamic-block, show debugging label-table, fec nexthop-resolution. Removed the unstated pathd remark and reworded explicit and implicit null.
Method: docs-only read of cited pages, 2026-11-08
