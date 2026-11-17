---
id: computing-software.systems-network-administration.wireshark.display-filter-bitwise-and-arithmetic
name: display-filter-bitwise-and-arithmetic
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, display-filters, bitwise-and, display-filter-arithmetic, slice-operator]
level: practitioner
status: verified
description: "Use Wireshark display filter bitwise AND, arithmetic and slices to test flag bits, compute sums across fields and match header bytes precisely."
sources:
  - https://www.wireshark.org/docs/man-pages/wireshark-filter.html
  - https://www.wireshark.org/docs/wsug_html_chunked/ChWorkBuildDisplayFilterSection.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bitwise and arithmetic display filter operators

## Bitwise AND (`&`, `bitand`)
True if any of the masked bits are set:
```
tcp.flags & 0x12                 # SYN or ACK set
tcp.flags & 0x12 == 0x12         # SYN and ACK both set (4.0+: `&` is a first-class operator, the result can be compared)
ip.flags & 0x2                   # DF bit (or ip.flags.df == 1)
ip.dsfield & 0xfc == 0xb8        # DSCP EF (46 << 2)
dns.flags & 0x8000               # responses
```
Prefer named sub-fields (`tcp.flags.syn == 1`) when they exist; masks help for fields without them.
On a slice the mask must be a byte string with the same length as the slice (`ip[42:2] & 40:ff`), not a number;
`eth.dst[0] & 0x01 == 1` works on a single byte (multicast/broadcast bit). `bitand` and `bitwise_and` are synonyms for `&`.

## Arithmetic (Wireshark 4.0+)
Operators `+ - * / %` and unary minus, with braces for grouping:
```
ip.len - ip.hdr_len - tcp.hdr_len > 0      # TCP payload present
frame.len > {tcp.window_size / 2}
udp.length != {ip.len - 20}                # mismatch with no IP options
tcp.srcport + 1 == tcp.dstport
tcp.dstport >= 4 * {tcp.srcport + 3}
```
Grouping must use curly brackets: parentheses are a syntax error (`"(" was unexpected in this context`). The subtraction
operator must be preceded by a space (`frame.len - ip.len` or `frame.len -ip.len`; `frame.len-ip.len` is parsed as one
unknown field name). Checked on TShark 4.4.1.
Field references `${field}` (or `$field`) read the value from the packet currently selected in the GUI:
`frame.time_relative >= ${frame.time_relative} - 300` (the man page's example). With no selection (tshark) they match nothing.

## Slices
```
eth.src[0:3] == 00:50:56          # VMware OUI
ip.dst[0] == 10
tcp.payload[0:4] == "HTTP"
frame[-4:] == de:ad:be:ef         # last four bytes
```

## Gotchas
- Arithmetic is integer for integer fields; division truncates (`ip.ttl / 7 == 9` matches TTL 64; `ip.ttl % 7 == 1` too).
  A float operand with an integer field is rejected (`ip.ttl / 7.0` gives an error).
- Multi-occurrence fields (e.g. `ip.ttl` in an IP-in-GRE-in-IP packet) match if any occurrence matches;
  use `all` / `any` quantifiers or the layer operator (`ip.addr#2 == 172.16.0.1` is the inner address). Both added in 4.0.

## Verify
- [ ] Spot-check three matched packets by expanding the fields and doing the arithmetic by hand.
