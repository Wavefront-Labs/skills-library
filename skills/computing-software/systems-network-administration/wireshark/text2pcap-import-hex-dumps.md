---
id: computing-software.systems-network-administration.wireshark.text2pcap-import-hex-dumps
name: text2pcap-import-hex-dumps
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, text2pcap, import-hex-dump, hexdump, od, dummy-headers, packet-import]
level: practitioner
status: verified
description: "Turn hex dumps from logs, debug output or device consoles into pcaps with text2pcap or File > Import from Hex Dump, adding dummy Ethernet/IP/UDP headers."
sources:
  - https://www.wireshark.org/docs/man-pages/text2pcap.html
  - https://www.wireshark.org/docs/wsug_html_chunked/ChIOImportSection.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Import hex dumps with text2pcap

Devices and applications often log packets as hex (router debug, firewall packet dumps,
application traces). text2pcap turns them back into a capture Wireshark can dissect.

## Input format
`od -Ax -tx1 -v` style (the man page names `od -Ax -tx1 -v` and `hexdump -X -v`): an offset followed by hex bytes. An offset of 0 starts a new packet.
Offsets are 3 to 8 hex digits, optionally followed by one colon; text before the offset on a line and text after the bytes are ignored;
lines beginning with `#` are comments.
```
000000 45 00 00 3c 1c 46 40 00 40 06 b1 e6 c0 a8 00 68
000010 c0 a8 00 01 ...
```
Produce it from a binary: `od -Ax -tx1 -v payload.bin > payload.txt`.

## Convert
```bash
text2pcap payload.txt out.pcapng                         # assumes Ethernet frames
text2pcap -l 101 payload.txt out.pcapng                  # raw IP (linktype 101)
text2pcap -e 0x0800 payload.txt out.pcapng               # add dummy Ethernet header
text2pcap -i 6 -4 10.0.0.1,10.0.0.2 payload.txt out.pcap # dummy IPv4 header, protocol 6 (decimal); Ethernet is added too
text2pcap -u 5060,5060 -4 10.0.0.1,10.0.0.2 sip.txt sip.pcap   # dummy UDP so SIP dissects
text2pcap -T 1234,443 ...                                 # dummy TCP ports
text2pcap -t "%H:%M:%S.%f" log.txt out.pcap               # timestamp before each packet (%f = fraction)
```
Choose dummy ports so Wireshark's heuristics pick the right dissector, or use Decode As.
Checked on TShark 4.4.1: `-u 5060,5060 -4 10.0.0.1,10.0.0.2` on a SIP request dissected as SIP INVITE; `-l 101` on a raw IPv4/TCP
packet; `-e 0x0800` gave `eth.type 0x0800`; `-i 6` gave `ip.proto 6`; `-T 1234,443` gave those TCP ports. With `-t "%H:%M:%S.%f"` the
timestamps `10:00:01.5` and `10:00:07.25` were kept (frame times 1.5 s and 7.25 s past the minute); without `%f` the fraction is lost.
With no timestamp text, later packets are one microsecond after the previous one.

## GUI
File > Import from Hex Dump: same options, plus a regex mode for arbitrary log formats
with named groups `(?<data>...)`, `(?<time>...)`, `(?<dir>...)`; the User's Guide example is
`^(?<dir>[<>])\s(?<time>[0-9]+:[0-9][0-9]:[0-9][0-9].[0-9]+)\s(?<data>[0-9a-fA-F]+)$` (digit classes written out here).

## Gotchas
- An ASCII dump after the hex is ignored; if there is no delimiter between the hex and the ASCII text, use `-a` so hex digits in
  the ASCII column are not read as bytes (man page).
- Offsets must be correct: the man page says an unexpected offset aborts the current packet. In a test the packet was still written, cut
  short at the bytes read before the bad offset (32 bytes instead of 45), so compare `frame.len` with what you expect.
- Dummy headers get valid checksums: with `ip.check_checksum` and `udp.check_checksum` on, tshark reported status 1 (good) for the `-u`/`-4` import.
  Checksums inside your payload bytes are not recomputed.

## Verify
- [ ] Wireshark dissects the payload protocol correctly with the expected number of packets.
