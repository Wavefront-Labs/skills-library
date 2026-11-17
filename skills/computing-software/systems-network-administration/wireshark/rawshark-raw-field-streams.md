---
id: computing-software.systems-network-administration.wireshark.rawshark-raw-field-streams
name: rawshark-raw-field-streams
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, rawshark, tshark, field-extraction, pipelines]
level: practitioner
status: verified
description: "Use rawshark to dissect a raw libpcap stream from a pipe and print selected fields fast, and know when tshark -T fields is the better choice."
sources:
  - https://www.wireshark.org/docs/man-pages/rawshark.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rawshark for raw field streams

rawshark reads a stream of libpcap-style records (`ts_sec`, `ts_usec`, `caplen`, `len`, then the data; the man page's `rawshark_rec_s`) from a pipe
or stdin and prints chosen fields. It is designed to be driven by another program. A regular file given to `-r` is refused:
`rawshark: "t.pcap" is neither an interface nor a pipe`; feed files with `-r -` and a shell redirect.

## Usage
```
rawshark -s -r - -d encap:1 -F ip.src -F ip.dst < in.pcap
<producer writing a pcap stream> | rawshark -s -r - -d encap:1 -F dns.qry.name    # or a named pipe passed to -r
```
`-d` and `-r` are mandatory (man page). The first command ran on RawShark 4.4.1 against a classic pcap.
- `-s` skips the pcap file header at the start of the stream (needed when the input is a normal
  pcap file or tcpdump output).
- `-d encap:<name or number>` declares the link type (`encap:EN10MB`, or the LINKTYPE number: 1 = Ethernet, 101 = raw IP); `-d proto:<protocol>`
  hands the data straight to that dissector (`proto:http`; `proto:udp` ran and decoded the bytes as a UDP header).
- `-F field` (repeatable) selects fields.

## Output format
```
0 FT_IPv4 BASE_NONE - 1 FT_IPv4 BASE_NONE -
1 1="10.0.0.80" 0="10.0.0.5" -
```
Line 0 describes each `-F` field (index, type, display base; `-` ends the list). Each following line is the packet number, then
`fieldindex="value"` pairs in any order, a `1`/`0` flag (did the packet pass the read filter) when a filter is given, and a trailing `-`.
In the test the output above came from `-F ip.src -F ip.dst`; the layout is machine-oriented, so parse it with a script.

## When to use
- Embedding a dissector in another tool that already has packets in pcap record form.
- Dissecting payload bytes that are not Ethernet frames (`-d proto:...`).
For most jobs `tshark -T fields -e ... -E separator=,` is simpler and supports pcapng.

## Gotchas
- pcapng input is not supported: a pcapng file piped in gave `The standard input appears to be damaged or corrupt`. Convert with `editcap -F pcap`.
- No reassembly across packets beyond what single-pass dissection does.

## Verify
- [ ] Field values match `tshark -T fields` on the same file (e.g. `ip.src` values in the same packet order).
