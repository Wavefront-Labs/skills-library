---
id: computing-software.systems-network-administration.wireshark.tshark-verbose-protocol-detail
name: tshark-verbose-protocol-detail
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, tshark, tshark-verbose, packet-details, protocol-tree]
level: practitioner
status: verified
description: "Print full or selected protocol trees with tshark -V, -O and -P, plus hex dumps with -x, to read packet details from a terminal."
sources:
  - https://www.wireshark.org/docs/man-pages/tshark.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tshark -V and -O protocol detail output

On a headless box, tshark can show the same details pane as Wireshark.

## Full tree
```
tshark -r in.pcapng -V -Y "frame.number == 42"
```
Prints every protocol layer, expanded. Without `-Y` this produces megabytes per thousand packets.

## Only some protocols expanded
```
tshark -r in.pcapng -O dns -Y dns                 # one line per other layer + full DNS tree (no packet summary line)
tshark -r in.pcapng -O "tcp,http" -Y http.request
tshark -r in.pcapng -O tls -Y "tls.handshake.type == 1"
```
`-O` is like `-V` for the named protocols and shows only the top-level line for every other layer (man page). On a DNS response `-O dns`
printed `Frame 9: ...`, `Ethernet II, ...`, `Internet Protocol Version 4, ...`, `User Datagram Protocol, ...` then the expanded `Domain Name System`.
Add `-P` if you also want the one-line packet summary.

## Summary plus details
```
tshark -r in.pcapng -P -V -Y icmp       # summary line plus details (-V alone prints details only; -P also prints while writing with -w or under -Q)
tshark -r in.pcapng -x -Y "frame.number==42"    # hex + ASCII dump of the bytes
tshark -r in.pcapng -V --hexdump frames -Y "frame.number==42"   # hexdump of the frame data only (in the 4.4.1 man page; the version that added it is unconfirmed)
```

## Live
```
tshark -i <interface> -f "udp port 67 or udp port 68" -O dhcp
```
A fast way to watch DHCP options on a server with no GUI (syntax accepted on a live capture with `-a duration:2`; no DHCP traffic occurred in the test).
List interface numbers with `tshark -D`.

## Tips
- Add `-o tcp.relative_sequence_numbers:FALSE` or other `-o` prefs to change the rendering.
- `-2` for two-pass if you need forward-looking details in the tree: `-V -Y http.request` showed `Response in frame` only with `-2`.
- Pipe to `less -S` and search with `/`.

## Verify
- [ ] The `-O` output for a known packet shows the expected fields for the same frame (the tree text matches the Wireshark details pane).
