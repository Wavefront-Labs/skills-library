---
id: computing-software.systems-network-administration.wireshark.follow-stream-show-data-as
name: follow-stream-show-data-as
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, follow-stream, show-data-as, c-arrays, yaml, raw-export]
level: practitioner
status: verified
description: "Save Follow Stream payload as raw bytes, C arrays, hex dump or YAML to rebuild files, replay traffic or feed test harnesses."
sources:
  - https://www.wireshark.org/docs/wsug_html_chunked/ChAdvFollowStreamSection.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Saving stream data with Show data as

The Follow Stream dialog's "Show data as" drop-down changes both the display and what Save as...
writes.

| Mode | Use |
|------|-----|
| ASCII | read text protocols (HTTP/1, SMTP, FTP control) |
| Raw | exact bytes; save to rebuild a transferred file or replay with netcat |
| Hex Dump | offsets + hex + ASCII, for reports |
| C Arrays | the stream as C array data for your own C program (GUI only: `tshark -z follow` rejects it as "Invalid display mode") |
| EBCDIC | mainframe traffic |
| UTF-8 / UTF-16 | non-ASCII text (tshark accepts `utf-8`, not `utf-16`, in 4.4.1) |
| YAML | per-packet base64 with peer, packet number, timestamp; machine-readable, keeps direction (`tshark -z follow,tcp,yaml,N` output showed exactly these keys) |

## Rebuilding a file
1. Follow the data connection (FTP-DATA, raw TCP) or set the direction to the sender only.
2. Show data as Raw, select the one direction, Save as `file.bin`.
3. For HTTP, strip headers manually or prefer File > Export Objects > HTTP, which handles
   chunking and compression.

## Replaying
```
# client side bytes saved as client.raw, sent with any netcat-style tool or a few lines of socket code
```
Use YAML (or C Arrays in the GUI) when you need per-message boundaries (request/response pairs) rather than one blob.

## tshark equivalent
```
tshark -r in.pcapng -q -z follow,tcp,raw,7 | sed -n '/^=\+$/,$p'   # raw mode prints hex text, one line per direction block (peer 1 tab-indented)
tshark -r in.pcapng -q -z follow,tcp,yaml,7 > stream7.yaml
```

## Gotchas
- Saving "Entire conversation" in Raw interleaves both directions, which corrupts files.
- tshark's `follow` modes accepted in 4.4.1: ascii, ebcdic, hex, raw, utf-8, yaml (each was run).

## Verify
- [ ] The rebuilt file's hash matches the original or `file` identifies it correctly.
