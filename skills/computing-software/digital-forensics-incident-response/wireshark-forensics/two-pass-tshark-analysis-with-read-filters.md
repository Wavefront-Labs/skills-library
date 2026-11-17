---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.two-pass-tshark-analysis-with-read-filters
name: two-pass-tshark-analysis-with-read-filters
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [two-pass-analysis, tshark, read-filter, display-filter, pcap-analysis, dfir]
level: practitioner
status: verified
description: "Use tshark two-pass analysis (-2 with -R) versus single-pass display filters (-Y): when reassembly and response-tracking fields need two passes, performance and writing filtered captures."
sources: ["https://www.wireshark.org/docs/man-pages/tshark.html", "https://www.wireshark.org/docs/wsug_html_chunked/ChAdvReassemblySection.html", "https://www.wireshark.org/docs/man-pages/wireshark-filter.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Two-pass tshark analysis with read filters

tshark normally dissects each packet once, in order. Some fields depend on later packets (a request's response, a reassembled PDU completed later, TCP analysis flags). Two-pass mode (`-2`) dissects the whole file first, then filters and prints with full knowledge.

## Filters
- `-Y "<display filter>"`: filters what is printed or written. On its own it runs in the single pass; combined with `-2` it
  runs in the second pass, after the whole file has been dissected. This is the combination that sees forward references.
- `-2 -R "<read filter>"`: the read filter runs in the FIRST pass, so it cannot see forward references such as
  `dns.response_in` (in 4.4.1 `-2 -R "dns.flags.response==0 && !dns.response_in"` matched every query). `-R` without `-2`
  prints "-R without -2 is deprecated. For single-pass filtering use -Y." and shows no packets.
- `-f` is a capture filter (BPF) and applies only when capturing live.

## When two passes matter
| Need | Why |
|---|---|
| `http.response_in`, `dns.response_in` | Point forward to a packet not yet seen in single pass |
| `http.time`, `dns.time` | Carried on the response frame (which also shows the request URI); `http.time > 2` matched in both modes in the test |
| `tcp.reassembled_in`, `smtp.data.reassembled.in` on the early segments | Reassembly completes later: 0 matches single-pass, 4 with `-2` on the test capture |
| Filtering requests that never got a response | `http.request && !http.response_in` only works with `-2 -Y` (single-pass `-Y` matched every request) |

## Examples
```bash
# DNS queries that got no answer
tshark -r cap.pcapng -2 -Y "dns.flags.response==0 && !dns.response_in" -T fields -e frame.time_utc -e ip.src -e dns.qry.name
# Slow HTTP responses
tshark -r cap.pcapng -2 -Y "http.time > 2" -T fields -e frame.number -e http.request.full_uri -e http.time
# Write a filtered evidence subset (keeps original packets, new file)
tshark -r cap.pcapng -2 -Y "ip.addr==203.0.113.50" -w subset.pcapng
```

## Performance
Two-pass holds state for the whole file in memory; on multi-GB captures, split first (`editcap -c 1000000` or `-i 3600`), or pre-filter with a cheap single-pass filter to a smaller file, then run two-pass on that.

## Gotchas
- A filter that works in the Wireshark GUI (which effectively has all packets) may silently miss frames in single-pass tshark; if counts differ from the GUI, try `-2 -Y`.
- Subsets written with `-w` are derived evidence: hash them and record the exact command and source hash.

## Verify
For any filtered count reported, running the same filter in the Wireshark GUI on the same file gives the same number of packets.

## Checked
Run on Wireshark 4.4.1 against a synthetic capture (fast, slow and unanswered HTTP requests; answered, unanswered and
NXDOMAIN DNS queries; a multi-segment SMTP message): the comparisons above were measured, including `-R` behaving as a
first-pass filter and `-R` alone being deprecated. The `-w` subset example wrote the 15 expected packets. `-f` on a
saved file is rejected ("Only read filters, not capture filters, can be specified when reading a capture file"). The
`editcap -c` and `-i` splitting options ran in an earlier check of this batch.
