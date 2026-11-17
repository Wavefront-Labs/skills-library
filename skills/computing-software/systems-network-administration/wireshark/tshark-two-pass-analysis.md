---
id: computing-software.systems-network-administration.wireshark.tshark-two-pass-analysis
name: tshark-two-pass-analysis
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, tshark, two-pass-analysis, read-filter, reassembly, display-filter, tcp-analysis]
level: practitioner
status: verified
description: "Use tshark -2 with -R read filters so reassembly and TCP analysis flags are correct when filtering or writing subsets, and know when one pass is wrong."
sources:
  - https://www.wireshark.org/docs/man-pages/tshark.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tshark two-pass analysis

In a single pass tshark dissects each packet once, in order, and cannot look ahead. The man page says `-2` "allows it to fill in
fields that require future knowledge, such as 'response in frame #' fields" and permits reassembly frame dependencies to be
calculated correctly. Examples checked on 4.4.1:
- Request/response links (`dns.response_in`, `http.response_in`) need a later packet: `-Y dns.response_in` matched nothing in one
  pass and the query/response pair with `-2`.
- Reassembled PDUs: the HTTP response appears on the **last** segment. With `-Y` the man page says packets that matching packets
  depend upon (for example fragments) are written to a `-w` file but not printed.
- `tcp.analysis.acks_frame` gave the same frames in one and two passes on a small file, so do not assume every `tcp.analysis.*` flag
  needs `-2`; test the field you rely on.

## Two-pass
```bash
tshark -r big.pcapng -2 -R 'tcp.stream eq 17' -w stream17.pcapng
tshark -r big.pcapng -2 -Y 'dns.flags.response==0 && !dns.response_in' -T fields -e dns.qry.name
```
- `-2` performs a first pass over the file, then dissects again with full knowledge.
- `-R` (read filter) is applied during the **first** pass; packets that do not match are not considered in later passes (man page).
  So it cannot use forward-looking fields such as `dns.response_in`, and it renumbers frames: `-2 -R dns` printed `frame.number`
  1 and 2 for what were frames 8 and 9. `-Y` is the filter applied in the final pass.
- Second example: queries with no response anywhere in the file (needs two pass and `-Y`). In the test capture a query that has a
  response gave an empty result with `-2 -Y '... && !dns.response_in'`, but with `-R` in place of `-Y` the same query was wrongly listed.
- Without `-2`, `-R` prints `tshark: -R without -2 is deprecated. For single-pass filtering use -Y.` and outputs nothing;
  a single-pass `-Y dns.response_in` also matched nothing.
- Two-pass needs to seek backwards: no live captures and no pipes or FIFOs.

## Cost
Two-pass makes tshark buffer output until the entire first pass is done (man page). On multi-GB files filter first with a cheap
single pass (`-Y 'ip.addr==10.1.1.10' -w subset`) or `editcap`, then run two-pass on the subset.

## Verify
- [ ] Output of a reassembly-dependent filter (`http.response_in`, `tcp.stream`) is complete and the
      written pcap reassembles in Wireshark.
