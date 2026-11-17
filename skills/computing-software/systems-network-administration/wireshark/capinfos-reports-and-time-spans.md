---
id: computing-software.systems-network-administration.wireshark.capinfos-reports-and-time-spans
name: capinfos-reports-and-time-spans
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, capinfos, capinfos-report, capture-file-properties, pcapng, triage, hashing]
level: practitioner
status: verified
description: "Triage capture files fast with capinfos: packet counts, time span, data rates, drops, interfaces, hashes, and table output for comparing many files."
sources:
  - https://www.wireshark.org/docs/man-pages/capinfos.html
  - https://www.wireshark.org/docs/wsug_html_chunked/ChStatSummary.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# capinfos reports

Before opening a 4 GB capture in the GUI, know what is in it.

## Full summary
```
capinfos trace.pcapng
```
Key lines: File type/encapsulation, Number of packets, File size, Data size, Capture duration,
Earliest/Latest packet time, Data byte rate, Average packet size, SHA256 and SHA1, and for pcapng the Capture
hardware, oper-sys and application. `capinfos -I` adds per-interface name, description, hardware, `Filter string`,
`Number of stat entries` and `Number of packets`. In 4.4.1 it shows only the count of interface statistics entries, not a
"dropped" figure; dumpcap prints `Packets received/dropped on interface` when the live capture ends, so keep that output.

## Pick fields
```
capinfos -c -u -a -e trace.pcapng          # count, duration, earliest/latest time
capinfos -i -z trace.pcapng                # data bit rate, average packet size
capinfos -H trace.pcapng                   # hashes (SHA256, SHA1; man page: SHA1 may be removed) for evidence records
capinfos -E -I trace.pcapng                # encapsulation and interface details (-I is not available in table format)
capinfos -M -c -u trace.pcapng             # raw machine-readable values instead of SI suffixes
```

## Many files as a table
```
capinfos -T -r -c -a -e -u ring_*.pcapng | column -t
#  -T table (tab separated), -r no header row; add -m for comma separated, -N no quotes, -Q double quotes
```
Use it to find which ring-buffer file covers the incident time:
```
capinfos -T -a -e ring_*.pcapng | awk -F'\t' '$2 <= "2026-10-18 14:05" && $3 >= "2026-10-18 14:05"'
```
(Times print as `YYYY-MM-DD hh:mm:ss.ffffff` in the capture's local time zone, so string comparison with a `YYYY-MM-DD hh:mm` prefix works.
Without `-r` the first line is a header row that the comparison simply fails on.)

## The GUI equivalent
Statistics > Capture File Properties shows the same data plus capture file comments and a "Displayed"
column for the current display filter; Copy To Clipboard copies the details (User's Guide, Capture File Properties).

## What to look for
- Dropped packets > 0 (from the dumpcap end-of-capture message): expect false "previous segment not captured".
- Encapsulation `Per packet`: mixed link types (pcapng from several interfaces).
- Capture filter recorded: tells you what traffic cannot be in the file.
- Duration vs expected: a 2-hour incident in a 10-minute capture means you need other files.

## Gotchas
- Classic pcap has no drop counts or interface metadata; convert carefully, as pcap -> pcapng
  cannot restore what was never recorded.
- Truncated files (capture killed) still report but print an error such as `The file "cut.pcap" appears to have been cut short in the middle of a packet`.

## Verify
- [ ] The file chosen for analysis spans the incident time and the capture log showed zero (or known) drops.
