---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.tshark-field-extraction
name: tshark-field-extraction
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [tshark-fields, tshark, pcap, field-extraction, command-line, dfir]
level: practitioner
status: docs-checked
description: "Extract fields from captures with tshark -T fields for analysis at scale: the -E separator, quote, occurrence and aggregator options, two-pass mode, and statistics with -z."
sources: ["https://www.wireshark.org/docs/man-pages/tshark.html", "https://www.wireshark.org/docs/dfref/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tshark field extraction

**Goal:** turn large captures into tabular data you can sort, count and join, without the
Wireshark GUI.

## Basics
```bash
tshark -r cap.pcapng -Y 'http.request' -T fields \
  -e frame.time_epoch -e ip.src -e ip.dst -e http.host -e http.request.uri \
  -E header=y -E separator=, -E quote=d -E occurrence=f > http.csv
```
- `-Y` is the display filter (post-dissection); `-f` is a capture filter (only when capturing).
- `-e` adds a field and may be repeated; at least one is required with `-T fields`.
- `-E header=y` prints field names first; `-E separator=` sets the separator (default tab);
  `-E quote=d|s|n` double, single or no quotes (default none; embedded quotes are doubled).
- `-E occurrence=f|l|a` first, last or all occurrences (default all); `-E aggregator=`
  sets the character joining multiple occurrences (default comma).
- `-T ek` and `-T json` give nested output (EK is the Elasticsearch bulk format).
- Field names: the Wireshark display filter reference (dfref) lists each protocol's fields.

## Statistics without the GUI
```bash
tshark -r cap.pcapng -q -z io,phs      # protocol hierarchy
tshark -r cap.pcapng -q -z http,tree
```

## Performance and correctness
- `-2` does a two-pass analysis: output is buffered until the first pass completes, so
  fields needing future knowledge (such as "response in frame") and reassembly dependencies are
  filled in correctly. It cannot be used with live captures or pipes, and is slower.
- `-n` disables network object name resolution (hostnames, port names).
- Split multi-GB captures before running tshark and process the pieces in parallel.

## Verify
Spot-check a few rows against the same packets in Wireshark (frame numbers via `-e frame.number`).

## Checked
2026-11-01. Confirmed in the tshark man page: `-T fields|ek|json`, `-e`, every `-E` option listed
above with defaults, `-2` behaviour and limits, `-n`, `-z io,phs`, `-z http,tree`, `-Y`/`-f`.
Removed: specific TLS SNI, DNS and JA3/JA4 field names, `tshark -G fields`, `editcap` and
`tcpdump` command lines, and the `-z conv,tcp` example, which the fetched pages do not confirm.
Method: documentation only; no commands were run.
