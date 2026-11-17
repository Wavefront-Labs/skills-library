---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.tshark-statistics-with-z
name: tshark-statistics-with-z
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [tshark-statistics, tshark, pcap-triage, protocol-hierarchy, dfir]
level: practitioner
status: verified
description: "Generate capture statistics from the command line with tshark -z: conversations, endpoints, protocol hierarchy, HTTP/DNS trees, expert info and I/O stats."
sources: ["https://www.wireshark.org/docs/man-pages/tshark.html", "https://www.wireshark.org/docs/wsug_html_chunked/ChStatistics.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tshark statistics with -z

**Goal:** summarise large captures quickly, script triage across many files, and produce
reproducible numbers for reports.

## Common statistics
```bash
tshark -r cap.pcapng -q -z io,phs                       # protocol hierarchy
tshark -r cap.pcapng -q -z conv,tcp                     # TCP conversations (bytes, duration, rel start)
tshark -r cap.pcapng -q -z conv,ip -z endpoints,ip      # IP conversations + endpoints
tshark -r cap.pcapng -q -z http,tree                    # HTTP request methods/status codes
tshark -r cap.pcapng -q -z http_req,tree                # requests per host/URI
tshark -r cap.pcapng -q -z dns,tree                     # DNS query/response stats (qtypes, rcodes)
tshark -r cap.pcapng -q -z expert                       # expert info summary
tshark -r cap.pcapng -q -z io,stat,60,"ip.addr==10.1.2.3","tcp.analysis.retransmission"   # per-minute counts
tshark -r cap.pcapng -q -z follow,tcp,ascii,7           # follow stream 7 as text
tshark -r cap.pcapng -q -z credentials                  # cleartext credentials seen (FTP, HTTP basic, etc.)
```
- `-q` suppresses per-packet output; `-z help` lists all available statistics (the list is printed on stderr).
- Add a display filter to scope: `-Y "ip.addr==10.1.2.3"` (applied before stats) or embed the filter in the `-z` argument where supported (`conv,tcp,ip.addr==10.1.2.3`).

## Scripting across files
```bash
for f in captures/*.pcap; do echo "== $f"; tshark -r "$f" -q -z conv,ip | head -30; done > conv_summary.txt
```

## Gotchas
- Large captures: statistics require a full pass; use `editcap -A/-B` to slice by time first.
- Two-pass features (reassembly-dependent stats) may differ from GUI if preferences differ; use the same profile (`-C <profile>`).
- `conv` prints the `<-` (B to A) column group first and `->` (A to B) second, and switches units to `kB` or `MB` on larger flows, so read the headers and do not `sort -n` the raw text.

## Verify
Numbers used in reports are reproduced from the saved command line and capture hash.

## Checked
Run on Wireshark 4.4.1 against a synthetic capture (HTTP, DNS, basic-auth request): every command in the Common
statistics block produced its report (`io,phs`, `conv,tcp`, `conv,ip` with `endpoints,ip`, `http,tree`, `http_req,tree`,
`dns,tree`, `expert`, `io,stat,1,...` with two filters, `follow,tcp,ascii,1`, `credentials` listing the HTTP basic
auth user), the filter embedded in `conv,tcp,<filter>` and `-Y` both scoped the output, `-C` with a missing profile
errors out, and the per-file loop wrote one section per capture.
