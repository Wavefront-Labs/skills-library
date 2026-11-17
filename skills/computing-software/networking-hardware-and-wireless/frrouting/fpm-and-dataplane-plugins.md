---
id: computing-software.networking-hardware-and-wireless.frrouting.fpm-and-dataplane-plugins
name: fpm-and-dataplane-plugins
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, zebra, fpm, dplane-fpm-nl, dpdk, dataplane, netlink]
level: sme
status: docs-checked
description: "Send the FRR FIB to an external forwarding plane manager with the fpm or dplane_fpm_nl zebra modules, and inspect zebra dataplane providers and the DPDK plugin."
sources:
  - https://docs.frrouting.org/en/latest/zebra.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FPM and dataplane plugins
Build with `--enable-fpm`, then start zebra with `-M fpm` or `-M dplane_fpm_nl`. Once the connection is up, zebra sends a complete copy of the forwarding table to the FPM; the kernel still receives FIB updates as before.

`fpm` module (netlink or protobuf):
- `fpm connection ip A.B.C.D port (1-65535)`; default target is 127.0.0.1:2620.
- `show zebra fpm stats`, `clear zebra fpm stats`.

`dplane_fpm_nl` module (netlink only, connects only when configured):
- `fpm address <A.B.C.D|X:X::X:X> [port (1-65535)]` sets the server and connects immediately; `no` disables FPM and closes connections.
- `fpm use-next-hop-groups` uses RTM_NEWNEXTHOP/RTM_DELNEXTHOP to share nexthops; `no` includes nexthops inline.
- `fpm use-route-replace` uses NLM_F_REPLACE instead of separate delete and add.
- `show fpm counters [json]`, `show fpm status [json]`, `clear fpm counters`.

Dataplane inspection: `show zebra dplane [detailed]`, `show zebra dplane providers` (the local kernel plugin is present by default), `zebra dplane limit [NUMBER]` (pending updates for the dataplane thread).

DPDK: build with `--enable-dp-dpdk=yes`, start with `-M dplane_dpdk`; PBR rules as rte_flows also need `pbr nexthop-resolve`. Views: `show dplane dpdk port [detail]`, `show dplane dpdk pbr flows`, `show dplane dpdk counters`.

Other startup flags: `--asic-offload=[notify_on_offload|notify_on_ack]`, `-s SIZE` netlink buffer.

## Checked

2026-11-04. Confirmed against the FRR Zebra page (FPM, dataplane and DPDK sections): modules, default fpm target, command forms, netlink message options, dplane show commands, DPDK build flag and views, startup flags. Removed the unsupported 'after reconnects' and 'replace semantics' wording.
Method: documentation only; no commands were run.
