---
id: computing-software.systems-network-administration.wireshark.packet-lengths-statistics
name: packet-lengths-statistics
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, packet-lengths, statistics, mtu, plen]
level: practitioner
status: verified
description: "Read Wireshark Statistics > Packet Lengths and tshark -z plen to spot small-packet chatter, MTU limits, jumbo frames and fragmentation patterns."
sources:
  - https://www.wireshark.org/docs/wsug_html_chunked/ChStatPacketLengths.html
  - https://www.wireshark.org/docs/man-pages/tshark.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Packet lengths statistics

Statistics > Packet Lengths buckets frames by size (0-19, 20-39, 40-79, ... 2560-5119, 5120+) with
count, average, min, max, rate and percentage. Apply a display filter to restrict it.

## tshark
```
tshark -r in.pcapng -q -z plen,tree
tshark -r in.pcapng -q -z plen,tree,"ip.addr==10.1.1.5 && tcp"
```

Run: the buckets are 0-19, 20-39, 40-79, 80-159, 160-319, 320-639, 640-1279, 1280-2559, 2560-5119 and 5120 and
greater (the last is labelled "5120 and greater"); a 1514-byte frame landed in 1280-2559, and the display-filter
form ran too.

## Patterns and what they mean
| Pattern | Likely cause |
|---------|--------------|
| Most packets 40-79 bytes | ACK-heavy or chatty small-request application; check turn counts |
| Bulk at 1280-2559 but max 1514 | normal full-size Ethernet frames, MSS 1460 |
| Max well below 1514 (e.g. 1414) | MTU/MSS clamp somewhere, tunnel overhead, PMTUD in effect |
| Frames 5120+ | jumbo frames, or TSO/GRO on the capturing host (offload, not on the wire) |
| Large and small alternating | IP fragmentation (first fragment full, tail small) |

## Gotchas
- Capturing on the sending host with TCP segmentation offload shows 64 KB "packets" that never exist
  on the wire. Disable segmentation offload on the NIC (OS and driver specific) or capture on a SPAN/TAP.
- Frame length includes the link-layer header; IP length is 14 bytes smaller on Ethernet.

## Follow-up filters
```
frame.len > 1514
ip.flags.mf == 1 || ip.frag_offset > 0
tcp.len > 0 && tcp.len < 100
```

## Verify
- [ ] The maximum observed size matches the path MTU you expect (a 1500-byte MTU carries a 1472-byte ICMP payload,
  since 20 + 8 header bytes are added; test with don't-fragment ping, e.g. Windows `ping -f -l 1472 host`).
