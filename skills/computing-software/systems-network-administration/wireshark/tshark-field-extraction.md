---
id: computing-software.systems-network-administration.wireshark.tshark-field-extraction
name: tshark-field-extraction
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, tshark, tshark-fields, field-extraction, csv, occurrence, separator, command-line]
level: practitioner
status: verified
description: "Extract chosen fields from captures with tshark -T fields -e into CSV/TSV for scripting: headers, separators, multi-value occurrences and quoting."
sources:
  - https://www.wireshark.org/docs/man-pages/tshark.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tshark field extraction

```bash
tshark -r cap.pcapng -Y 'dns.flags.response == 1' -T fields \
  -e frame.time_epoch -e ip.src -e dns.qry.name -e dns.a -e dns.time \
  -E header=y -E separator=, -E quote=d -E occurrence=a -E aggregator=';' > dns.csv
```
- `-T fields` + one `-e` per field; names are display filter field names (see Apply as
  Filter / status bar, or `tshark -G fields | grep -P '\tdns\.'`; `grep -P` fails with "supports only unibyte and UTF-8 locales" in some Windows
  shells, where `tshark -G fields | grep dns.` is enough).
- `-E occurrence=f|l|a`: first, last or all values of multi-valued fields (several `dns.a`
  answers, tunnelled `ip.src`). `aggregator` joins them.
- `-E quote=d` double-quotes values (a quote inside a value is doubled); needed when fields contain commas (user agents).
  `escape=y` (default) turns tabs and newlines in values into C-style escapes. `bom=y` prepends a UTF-8 BOM for Excel.
- `-Y` is the display filter (single pass); `-f` is a capture filter and tshark refuses it with `-r`
  (`Only read filters, not capture filters, can be specified when reading a capture file`).
- `-n` disables name resolution (faster, and reproducible output).
- Custom column-like output: `-T fields -e _ws.col.Info` gives the Info column text.

## Common one-liners
```bash
# TLS SNI per client
tshark -r cap.pcapng -Y tls.handshake.type==1 -T fields -e ip.src -e tls.handshake.extensions_server_name | sort | uniq -c | sort -rn
# HTTP requests
tshark -r cap.pcapng -Y http.request -T fields -e ip.src -e http.host -e http.request.uri
# TCP stream ids with retransmissions
tshark -r cap.pcapng -Y tcp.analysis.retransmission -T fields -e tcp.stream | sort -n | uniq -c
```

## Gotchas
- Fields that need future knowledge or reassembly (`http.response_in`, reassembled bodies) are filled only with `-2` (two-pass);
  `-2` cannot read from a pipe. With `-2`, `http.response_in` returned frame 4 for a request in the test capture.
- Field names change between releases (e.g. the SSL dissector became TLS in 3.0; the old `ssl.*` fields were kept for a while
  but may be removed); pin a version in scripts.
- Large files: add a tight `-Y` and skip unused protocols for speed. `--disable-protocol http` makes `-Y http` match nothing.

## Verify
- [ ] CSV opens with a header row and one row per matching packet; counts match the GUI filter. The one-liners above were run
  on TShark 4.4.1 against generated captures (SNI `www.example.com`, one retransmission on stream 0).
