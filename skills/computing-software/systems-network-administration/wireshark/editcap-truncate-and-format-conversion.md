---
id: computing-software.systems-network-administration.wireshark.editcap-truncate-and-format-conversion
name: editcap-truncate-and-format-conversion
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, editcap, editcap-truncate, file-format-conversion, snaplen, pcap]
level: practitioner
status: verified
description: "Use editcap -s to truncate packets and -F/-T to convert capture formats and encapsulations so other tools and older readers can open files."
sources:
  - https://www.wireshark.org/docs/man-pages/editcap.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# editcap truncating and format conversion

## Truncating (snap length)
```
editcap -s 128 in.pcapng hdrs.pcapng            # keep first 128 bytes of every packet
editcap -C 4 in.pcapng out.pcapng               # chop 4 bytes from the start of each packet
editcap -C -4 in.pcapng out.pcapng              # chop 4 bytes from the end (trailing FCS)
```
After `-s` or `-C`, `frame.cap_len` shrinks (`-s 128` gave 128 for every packet longer than that; `-C 4` lowered the minimum
packet size by 4) while `frame.len` keeps the original wire length. `-C` takes an optional offset (`-C 14:4`), may be
repeated, and positive values chop from the start, negative from the end.
Truncation cuts payloads for privacy and size. Size the snaplen for your deepest header stack (IPv6, tunnels and
VLAN stacks need more than plain IPv4/TCP). Wireshark flags truncated packets, e.g. `[Packet size limited during capture: HTTP
truncated]` seen after `editcap -s 60`, and TCP payload analysis becomes partial.

## Converting formats
```
editcap -F                                      # list output formats
editcap -F pcap in.pcapng out.pcap              # for tools that only read classic pcap
editcap -F pcapng in.pcap out.pcapng
editcap -F nsecpcap in.pcapng out.pcap          # nanosecond pcap
editcap -T ether in.pcap out.pcap               # override encapsulation type
```
Converting pcapng to pcap fails if the file holds several interface link types (a merge of an Ethernet and a raw-IP capture
gave `The capture file being read can't be written as a "pcap" file`); split by interface first
(`tshark -r in.pcapng -Y "frame.interface_id==0" -w if0.pcapng`, which wrote all 13 packets of interface 0 in the test).
`editcap -F` and `editcap -T` print the supported formats and encapsulation names.

## What is lost going to pcap
Packet comments (`editcap -a 1:hello` then `-F pcap` left no `frame.comment`), the decryption secrets block (`capinfos` showed
`Number of decryption secrets in file: 1` before and nothing after), other pcapng-only blocks, multiple link types and
nanosecond precision (unless nsecpcap).

## Other useful flags
- `-i <secs>` / `-c <n>` split by time or packet count; outputs are named `name_00000_YYYYmmddHHMMSS.ext`. A large time gap
  with a small `-i` creates one file per interval, including empty gaps (a 5-hour gap with `-i 2` made about 9000 files),
  so check the capture span with capinfos first.
- `-d` removes duplicates (compares length and MD5 against the previous four packets); `-D <n>` sets the window
  (SPAN of both directions).
- `-t <secs>` shifts timestamps (`-t 3600` moved the earliest packet from 08:13:20 to 09:13:20).
- `--inject-secrets tls,keys.txt` embeds TLS keys in a pcapng (`capinfos` then reports one decryption secret);
  `--inject-secrets help` lists the secret types.

## Verify
- [ ] `capinfos out.pcap` shows the expected file type, encapsulation and packet count.
