---
id: computing-software.systems-network-administration.wireshark.traffic-baselining-with-wireshark
name: traffic-baselining-with-wireshark
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, traffic-baseline, baselining, performance-analysis, protocol-hierarchy]
level: practitioner
status: verified
description: "Build a traffic baseline from captures: protocol mix, top talkers, response times, broadcast rates and TCP error rates to compare during incidents."
sources:
  - https://www.wireshark.org/docs/wsug_html_chunked/ChStatHierarchy.html
  - https://www.wireshark.org/docs/man-pages/tshark.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Baselining normal traffic

Without knowing normal, every retransmission looks like the problem.

## What to capture
Same capture points used during incidents (client access port, server port, WAN edge), at busy and
quiet times, 10-30 minutes each, repeated over weeks or after major changes.

## Metrics to record
```
tshark -r base.pcapng -q -z io,phs                     # protocol hierarchy
tshark -r base.pcapng -q -z conv,ip | head -30         # top talkers
tshark -r base.pcapng -q -z endpoints,tcp
tshark -r base.pcapng -q -z io,stat,60,"COUNT(tcp.analysis.retransmission)tcp.analysis.retransmission","COUNT(tcp.analysis.flags)tcp.analysis.flags"
tshark -r base.pcapng -q -z io,stat,60,"eth.dst.ig==1"  # frames and bytes with the group bit set (multicast and broadcast) per minute
tshark -r base.pcapng -q -z smb2,srt -z dns,tree -z http,tree     # `srt,smb2` is rejected: the order is smb2,srt
```
Keep a simple sheet per capture point:
| Metric | Normal range (measure it; there is no universal figure) |
|--------|--------------|
| Retransmission % of TCP packets | your own measured range per capture point |
| DNS response time p95 | your own measured range |
| SMB2 SRT average | your own measured range |
| Broadcasts/s per VLAN | your own measured range |
| TCP handshake RTT to key servers | your own measured range |

## Using the baseline
During an incident capture the same way and compare. Differences point to the layer: new
protocols (backup jobs, updates), new talkers, higher RTT (path), higher SRT with normal RTT (server).

## Gotchas
- Baselines go stale; refresh after migrations, new apps or WAN changes.
- Keep baseline captures (not just numbers) for re-analysis with new filters.

## Verify
- [ ] Each metric has a documented normal range, date and capture point.

## Checked
Run with TShark 4.4.1 on a synthetic capture: `-q -z io,phs`, `-z conv,ip`, `-z endpoints,tcp`, the two
`io,stat,60` commands (retransmission/flag counts per 60 s interval; `eth.dst.ig==1` counted the 3 broadcast frames),
`-z dns,tree` and `-z http,tree` all produced their tables; `-z srt,smb2` and `-z srt,dns` were rejected ("Invalid -z
argument") while `-z smb2,srt` ran. The example "normal range" figures in the old table were unsourced and were removed.
