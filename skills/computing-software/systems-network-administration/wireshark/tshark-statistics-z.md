---
id: computing-software.systems-network-administration.wireshark.tshark-statistics-z
name: tshark-statistics-z
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, tshark, tshark-statistics, conversations, io-stat, endpoints, protocol-hierarchy, srt]
level: practitioner
status: verified
description: "Produce Wireshark statistics from the CLI with tshark -q -z: protocol hierarchy, conversations, endpoints, io,stat intervals and service response times."
sources:
  - https://www.wireshark.org/docs/man-pages/tshark.html
  - https://www.wireshark.org/docs/wsug_html_chunked/ChStatistics.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tshark -z statistics

`-q` suppresses per-packet output so only the statistics print. Several `-z` can be combined.

```bash
tshark -r cap.pcapng -q -z io,phs                  # protocol hierarchy
tshark -r cap.pcapng -q -z conv,tcp                # TCP conversations (bytes, duration)
tshark -r cap.pcapng -q -z endpoints,ip            # top talkers
tshark -r cap.pcapng -q -z io,stat,1               # packets/bytes per 1 s interval
tshark -r cap.pcapng -q -z "io,stat,10,tcp.analysis.retransmission,tcp.analysis.zero_window"
tshark -r cap.pcapng -q -z "io,stat,5,SUM(frame.len)frame.len,MAX(tcp.analysis.ack_rtt)tcp.analysis.ack_rtt"
tshark -r cap.pcapng -q -z http,tree               # HTTP status codes and methods
tshark -r cap.pcapng -q -z dns,tree                # DNS packet types, query types, rcodes (works in 4.4.1)
tshark -r cap.pcapng -q -z rpc,srt,100003,3        # NFSv3 service response times
tshark -r cap.pcapng -q -z smb2,srt                # SMB2 per-command response times
tshark -r cap.pcapng -q -z expert                  # expert info summary
```
`tshark -z help` lists every available statistic in your build. All the commands above ran on TShark 4.4.1; on a capture
with no NFS or SMB2 they print an empty table, not an error. `expert` takes a severity (`-z expert,warn`) and a protocol/filter.

## Filters
Most stats take a trailing filter: `-z conv,tcp,ip.addr==10.1.1.10`. `io,stat` columns
accept any display filter or `FUNC(field)filter` (COUNT, SUM, MIN, MAX, AVG, LOAD); the man page's example is
`io,stat,0.010,AVG(smb.time)smb.time`, since the field must also be in the filter part. An interval of 0 gives one total row.
`LOAD()` works only on relative-time fields such as `smb.time`: `LOAD(tcp.window_size)` is rejected with
`LOAD() is only supported for relative-time fields`.

## Use cases
- Pre-triage a huge capture on a server before downloading it.
- Cron jobs summarising rolling ring-buffer files.
- Comparing before/after captures: diff the `conv` or `expert` outputs.

## Verify
- [ ] Numbers match the GUI's Statistics menu for the same file and filter.
