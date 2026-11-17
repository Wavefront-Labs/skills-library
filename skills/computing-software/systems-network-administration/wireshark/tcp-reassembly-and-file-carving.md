---
id: computing-software.systems-network-administration.wireshark.tcp-reassembly-and-file-carving
name: tcp-reassembly-and-file-carving
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, follow-stream, packet-reassembly, tcp-reassembly, ip-reassembly, file-carving, raw-stream, out-of-order, reassembly-preferences, network-forensics, foremost, binwalk]
level: advanced
status: verified
description: "Control Wireshark reassembly (IP fragments, TCP segments, out-of-order) and carve files from raw streams when no exporter exists: raw Follow Stream, magic bytes."
sources:
  - https://www.wireshark.org/docs/wsug_html_chunked/ChAdvReassemblySection.html
  - https://www.wireshark.org/docs/wsug_html_chunked/ChAdvFollowStreamSection.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Packet reassembly and carving files from streams

## Reassembly settings that change what you see
| Preference | Effect when on |
|---|---|
| IPv4/IPv6 "Reassemble fragmented datagrams" | fragments shown as one PDU in the last fragment |
| TCP "Allow subdissector to reassemble TCP streams" | application PDUs spanning segments decoded once complete |
| TCP "Reassemble out-of-order segments" (`tcp.reassemble_out_of_order`, off by default) | handles reordering; costs memory |
| HTTP/TLS/SMB "reassemble ..." | bodies and records spanning segments |
With reassembly on, intermediate segments show `[TCP segment of a reassembled PDU]` and the
decode appears on the final frame. Turn **off** TCP reassembly when you want per-segment timing
analysis (each segment shows its own app-layer bytes).

## Troubles reassembly causes
- Missing a segment (capture loss) stops decoding for the rest of the PDU; the protocol tree
  shows nothing above TCP. Check `tcp.analysis.lost_segment`.
- Huge PDUs (multi-GB downloads) use lots of RAM; limit capture or disable body reassembly.

## Follow Stream as raw
Analyze > Follow > TCP Stream. Pick one direction (dropdown) and choose the **Raw** format, Save As `stream.bin`. This is the exact byte stream the application received.
CLI: `tshark -r cap.pcapng -q -z follow,tcp,raw,7 > follow.txt` (stream 7) writes a header block, then one hex line per
chunk; client-to-server chunks start at column 0 and server-to-client chunks start with a TAB. Pick one direction and
convert it, e.g. server side: `grep $'^\t' follow.txt | tr -d '\t' | xxd -r -p > server.bin` (header lines and the
other direction must not reach `xxd`).

## Carve
- Identify file types by magic bytes: `%PDF`, `PK\x03\x04` (zip/docx), `MZ` (PE), `\x89PNG`,
  `\xFF\xD8\xFF` (JPEG).
- Strip protocol framing first (HTTP headers up to `\r\n\r\n`, chunked encoding sizes).
- Find offsets with `grep -obUa -F '%PDF' stream.bin` (byte offset of each match; avoid `-P`, not every grep build has it)
  or Python `bytes.find`, then cut with `dd bs=1 skip=<offset>` or Python slicing. Dedicated carving tools exist; check
  their own documentation.
- Compressed transfer encodings (gzip) must be decompressed (`gzip -d` after stripping headers).

## Verify
- [ ] Carved file opens/parses (`file out/*`), hashes recorded.
- [ ] No "previous segment not captured" inside the stream used.

## Checked (2026-10-22)
- Ran on Wireshark 4.4.1 on a loopback capture of an HTTP/1.1 download: `-z follow,tcp,raw,0` output has the header block and TAB-prefixed server lines as described; the `grep | tr -d | xxd -r -p` pipeline rebuilt the server bytes, the PNG magic was found at offset 138 (after the 134-byte header and CRLFCRLF) and the 109 body bytes hashed identically to the served file (sha256 prefix 72de6f96c0fe). `grep -obUa -F '%PDF'` runs here while `grep -P` is not supported in this Git Bash grep.
- The `[TCP segment of a reassembled PDU]` info text is built in epan/dissectors/packet-tcp.c (`[%s segment of a reassembled PDU]`), `tcp.analysis.lost_segment` and `tcp.reassembled_in` are listed by `tshark -G fields`; the Raw format is described in https://www.wireshark.org/docs/wsug_html_chunked/ChAdvFollowStreamSection.html.
- `tshark -G defaultprefs`: `tcp.reassemble_out_of_order` FALSE, `tcp.desegment_tcp_streams` TRUE, `ip.defragment` TRUE, `ipv6.defragment` TRUE, `http.desegment_body` TRUE, `tls.desegment_ssl_records` TRUE.
- Magic bytes (%PDF, PK 03 04, MZ, 89 50 4E 47, FF D8 FF) match https://en.wikipedia.org/wiki/List_of_file_signatures; the PNG one was also seen in the capture.
- Removed the foremost and binwalk invocations (not installed, not run) and the unverified "2.6+" version tag.
