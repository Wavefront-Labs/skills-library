---
id: computing-software.systems-network-administration.wireshark.packet-capture-filtering-techniques
name: packet-capture-filtering-techniques
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, tshark, tcpdump, dumpcap, bpf, libpcap, pcap-filter, capture-filter, display-filter, dfilter, filter-syntax, vlan-tag, 802-1q, byte-offset, tcp-flags, contains, matches, regex, set-membership, field-reference, slice-operator, editcap, mergecap, reordercap, snaplen, pcap-trimming, packet-slicing, filter-buttons, ip-addr-not-equal, bpf-primitives, vlan-filter, editcap-split, deduplicate-packets, mergecap-merge]
level: advanced
status: verified
description: "Write precise BPF capture and Wireshark display filters: byte offsets, VLAN-tag traps, != semantics, in/matches/slices/field refs, plus editcap/mergecap post-capture slicing."
sources:
  - https://www.tcpdump.org/manpages/pcap-filter.7.html
  - https://www.wireshark.org/docs/man-pages/wireshark-filter.html
  - https://www.wireshark.org/docs/man-pages/editcap.html
  - https://www.wireshark.org/docs/man-pages/mergecap.html
  - https://www.wireshark.org/docs/relnotes/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Packet capture filtering techniques — save only what matters, then carve it precisely

**Goal:** write filters that catch exactly the traffic you mean (no silent misses, no
self-capture), and cut large captures down to a shareable, analysable slice. For where to
capture and how to read TCP/TLS, see
`computing-software.systems-network-administration.wireshark.traffic-capture-and-analysis`;
this skill is purely about the filter languages and post-capture carving.

## 1. BPF capture filters beyond host/port
Capture filters (libpcap syntax, used by tcpdump, dumpcap, Wireshark's capture dialog)
run in the kernel, so they are cheap but cannot see protocol meaning.

| Need | Filter |
|---|---|
| A subnet | `net 10.20.0.0/16` |
| TCP SYN or RST only (handshake/teardown sampling) | `tcp[tcpflags] & (tcp-syn\|tcp-rst) != 0` |
| ICMP except echo | `icmp and icmp[icmptype] != icmp-echo and icmp[icmptype] != icmp-echoreply` |
| Big packets (MTU hunting) | `greater 1400` |
| One MAC (DHCP clients before they have an IP) | `ether host 00:11:22:33:44:55` |
| HTTP GET request lines (cleartext only) | `tcp[((tcp[12:1] & 0xf0) >> 2):4] = 0x47455420` |
| IPv6 only | `ip6` |

Gotchas:
- **VLAN tags shift offsets.** If the capture interface sees 802.1Q-tagged frames (trunk
  SPAN, some TAPs), `host 10.1.1.5` silently matches nothing. Use
  `host 10.1.1.5 or (vlan and host 10.1.1.5)`. Everything after the `vlan` keyword is
  evaluated against the tagged offset. Whether the tag is visible to the filter depends on the capture platform and driver (VLAN offload can
  strip it), so the same filter can behave differently on two hosts. Test it.
- `host` and `port` match either direction and both IPv4/IPv6 (`port` covers TCP and UDP);
  use `src`/`dst` and `tcp port` when you mean less.
- BPF cannot follow IP fragments: `tcp port 443` misses the non-first fragments.
- Quote the whole filter in the shell, and always exclude your own remote session
  (`and not port 22`).
- Validate before a long capture: `dumpcap -i <iface> -f '<filter>' -d` compiles it and prints the BPF
  program (an invalid filter errors immediately), and `dumpcap -i <iface> -f '<filter>' -c 10 -w test.pcapng`
  proves it matches something. `tcpdump -d '<filter>'` is the Linux equivalent (not run here).

## 2. Display filters: the operators that matter
Display filters see every dissected field and can be changed after the fact, so when
disk allows, capture broadly and filter at display time.

- **Set membership:** `tcp.port in {80, 443, 8080}`, `ip.addr in {10.0.0.1..10.0.0.50}`. Members must be
  comma-separated; `{80 443 8080}` is a syntax error in 4.4.1 (required since 3.6).
- **Strings:** `http.host contains "example"`; regex with `matches`
  (`dns.qry.name matches "(?i)\\.corp\\.example$"`). `contains` is case-sensitive.
- **Slices:** `eth.src[0:3] == 00:50:56` (VMware OUI), `tcp.payload[0:4] == 16:03:01:00`.
- **Existence:** `tls.handshake.extensions_server_name` (field present at all),
  `!dns.response_in` (DNS queries that never got an answer).
- **Timing:** `frame.time_delta_displayed > 1`, `tcp.time_delta > 0.5` (needs TCP
  conversation timestamps enabled), `dns.time > 0.2`.
- **Tunnel layers (Wireshark 4.0+):** `ip.addr#2 == 10.1.1.5` matches the inner IP header
  of GRE/VXLAN/IPsec-in-clear traffic.
- **Field references (4.0+):** `${ip.src}` reads the value from the packet selected in the GUI, handy
  in saved filter buttons. tshark has no selected packet, so `ip.src == ${ip.src}` matches nothing there.

**The `!=` trap.** On multi-valued fields such as `ip.addr` (source *and* destination),
Wireshark 3.6+ treats `ip.addr != 10.0.0.1` as `!(ip.addr == 10.0.0.1)`, which is what
you want. Older versions (and some docs/blogs still circulating) used "any not equal",
which matched almost everything. If you are on an old build or sharing filters with
someone who is, write `!(ip.addr == 10.0.0.1)` explicitly. The explicit
"any not equal" operator is `!==` (alias `any_ne`); `~=` was deprecated in 4.0 and is a syntax error in
4.4.1, as is `ip.addr ~= x`. `===` (`all_eq`) is the strict "all must equal" form.

Build filters by clicking: right-click a field › **Apply as Filter / Prepare as Filter**,
then edit. Save the ones you reuse as **filter buttons** (the `+` on the filter toolbar)
per profile, e.g. one profile for VoIP, one for TLS.

## 3. Carving a capture after the fact
```bash
# Keep only what a display filter matches (two-pass for correct reassembly)
tshark -r big.pcapng -2 -R 'tcp.stream eq 17' -w stream17.pcapng
# Time window around the incident (ISO 8601; without Z or an offset the times are read as LOCAL time)
editcap -A 2026-10-15T14:02:00Z -B 2026-10-15T14:05:00Z big.pcapng window.pcapng
# Split into 100k-packet chunks or 60 s chunks
editcap -c 100000 big.pcapng part.pcapng
editcap -i 60 big.pcapng part.pcapng
# Trim payloads to headers before sharing (privacy, size)
editcap -s 96 big.pcapng headers-only.pcapng
# Remove duplicates produced by SPAN of both directions/ports
editcap -D 5 big.pcapng dedup.pcapng
# Merge client- and server-side captures chronologically
mergecap -w both.pcapng client.pcapng server.pcapng
# Fix out-of-order timestamps from multi-queue NICs
reordercap in.pcapng ordered.pcapng
```
Trimmed (`-s`) captures break reassembly and application dissectors; keep the original
for yourself and share the trimmed one. `mergecap` only interleaves correctly if both
capture hosts' clocks were in sync.

## Checked
Every capture filter in section 1 was compiled with `dumpcap -d` on Wireshark 4.4.1 and the program run against a
synthetic capture (plain, 802.1Q-tagged, IPv6, fragmented, ICMP, GET frames); the VLAN-tag and non-first-fragment
misses reproduced. Every display filter, the `!=`/`!==` semantics and every editcap/mergecap/reordercap/tshark
command in section 3 ran; operators were also checked against the 3.6.0 and 4.0.0 release notes.

## Verify
- [ ] Capture filter compiled with `dumpcap -d` and shown to match on a 10-packet test.
- [ ] VLAN-tagged traffic considered (`vlan and ...`) when capturing from a trunk or SPAN.
- [ ] No negated multi-value field written as bare `!=` on a pre-3.6 build.
- [ ] Shared captures are carved to the incident window and trimmed of payload where possible.
- [ ] The filter you used is written next to the evidence, so someone else can reproduce the view.
