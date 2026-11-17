---
id: computing-software.networking-hardware-and-wireless.strongswan.iptfs-aggfrag-mode
name: iptfs-aggfrag-mode
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, iptfs, aggfrag, rfc-9347, traffic-flow-security]
level: advanced
status: docs-checked
description: "Enable AGGFRAG mode (IP-TFS, RFC 9347) in strongSwan with mode = iptfs and tune the charon.iptfs section: reorder window, drop time, init delay, queue size and fragmentation."
sources:
  - https://docs.strongswan.org/docs/latest/features/iptfs.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# iptfs aggfrag mode
RFC 9347 defines AGGFRAG mode for ESP: like tunnel mode, but small IP packets are aggregated into one ESP packet and large ones fragmented across several. IP-TFS adds traffic flow confidentiality with fixed-size ESP packets at a constant rate. Linux supports AGGFRAG from 6.14 and strongSwan from 6.0.2; IP-TFS itself is not yet supported.

Enable per child with `mode = iptfs`. It is not enforced: if the peer lacks support, negotiation falls back to tunnel mode. It cannot be combined with `ipcomp` or the classic `tfc_padding`.

Global settings in `charon.iptfs` in strongswan.conf (some apply to inbound traffic only, others to outbound only):

| Key | Default | Meaning |
|---|---|---|
| `drop_time` | 1000000 | microseconds to wait for out-of-order packets (inbound) |
| `reorder_window` | 3 | packets that may arrive out of order (inbound) |
| `init_delay` | 0 | microseconds to wait for more packets to aggregate (outbound, when nothing is queued) |
| `max_queue_size` | 1048576 | bytes queued per tunnel; packets drop when full |
| `packet_size` | 0 | max outer layer 3 size; 0 uses PMTU; the kernel does not pad smaller packets |
| `accept_fragments` | yes | accept inner packet fragments across AGGFRAG payloads (an IKEv2 request; the kernel processes fragments regardless) |
| `dont_frag` | no | disable fragmenting inner packets when sending |

## Checked
2026-11-04. Confirmed against the strongSwan AGGFRAG Mode / IP-TFS page: Linux 6.14 and strongSwan 6.0.2 support, mode = iptfs fallback, ipcomp and tfc_padding exclusions, every charon.iptfs key and default. Nothing removed.

Method: documentation only; no commands were run.

