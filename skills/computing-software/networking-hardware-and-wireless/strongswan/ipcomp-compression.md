---
id: computing-software.networking-hardware-and-wireless.strongswan.ipcomp-compression
name: ipcomp-compression
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, ipcomp, compression, deflate, ipip]
level: advanced
status: docs-checked
description: "Enable IPComp (RFC 3173) compression before ESP in strongSwan with the child ipcomp option, and understand Linux behaviour: size thresholds, IPIP states and counters."
sources:
  - https://docs.strongswan.org/docs/latest/features/ipcomp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ipcomp compression
IPComp (RFC 3173) compresses IP packet content before encryption, offsetting some IPsec overhead. Both peers must support it and negotiate it in IKE. strongSwan supports only DEFLATE. Enable it per CHILD_SA with `ipcomp = yes` in swanctl.conf (the kernel needs `xfrm_ipcomp` and `deflate`; see the kernel modules topic).

**Linux behaviour when debugging:**
- Packets smaller than a threshold are not compressed; for deflate the threshold is 90 bytes (static, in `net/xfrm/xfrm_algo.c`). Default-sized IPv4 pings fall below it.
- To handle uncompressed packets in tunnel mode the kernel implicitly creates an IPIP tunnel beside the IPComp SAs. These appear in `ip xfrm state` with proto 4 (IPv6: proto 41, but IPv6 packets are larger so even default pings get compressed).
- IPIP traffic must be allowed explicitly in the INPUT chain; this also affects firewall rules from the default updown script (the page notes fixes in 5.1.2 and, for IPv6, 5.4.0).
- Six states are in play (IPsec, IPComp, IPIP, in and out each), so `ip -s xfrm state` counters can confuse: outbound traffic never uses the IPIP state, and the IPComp counters still increase for small packets that are not compressed. Inbound behaves differently: IPComp counters count only actually decompressed traffic, and the other packets pass through the IPIP tunnel.

## Checked
2026-11-04. Confirmed against the IPComp page: DEFLATE only, `<child>.ipcomp`, the 90-byte deflate threshold, IPIP proto 4 and 41, the version notes, and the counter behaviour. The module names come from the Linux Kernel Modules page.

Method: documentation only; no commands were run.
