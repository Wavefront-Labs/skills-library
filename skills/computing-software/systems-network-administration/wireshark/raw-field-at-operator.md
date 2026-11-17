---
id: computing-software.systems-network-administration.wireshark.raw-field-at-operator
name: raw-field-at-operator
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, display-filters, raw-field-operator, raw-bytes, dfilter]
level: practitioner
status: verified
description: "Match the raw on-wire bytes of a field with the Wireshark 4.x @ operator, bypassing dissector conversions for strings, flags and encodings."
sources:
  - https://www.wireshark.org/docs/man-pages/wireshark-filter.html
  - https://www.wireshark.org/docs/relnotes/wireshark-4.0.0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Raw field @ operator

Wireshark 4.2 added `@field` (the 4.2.0 release notes list "a new display filter feature for filtering raw bytes"),
which compares the field's raw bytes as captured instead of the converted value. The man page example is
`@browser.comment == 73:74:72:...`.

## Why it matters
- Strings are decoded (charset conversion, escaping); `@` matches the exact bytes.
- Integers are masked and shifted for bit fields; `@` gives the whole containing bytes
  (`@tcp.flags` is two bytes, `50:12` for a SYN-ACK with a 20-byte header).
- Names (DNS labels) are rendered in dotted form; `@dns.qry.name` exposes the length-prefixed
  wire format.

## Examples
```
@dns.qry.name contains 07:65:78:61:6d:70:6c:65      # "\x07example" label on the wire
@http.host contains "Login"                        # exact case, raw bytes
@http.host == "Host: Login.Example.com\r\n"          # raw bytes of http.host are the WHOLE header line
@tcp.flags == 50:12                                 # SYN+ACK including the data-offset nibble
@ip.dsfield == b8                                   # whole DS byte
len(@dns.qry.name) > 60
```
Raw values compare as byte arrays: write hex with colons, or quoted strings. `@http.host == "Login.Example.com"`
matches nothing because the raw bytes include `Host: ` and the CRLF. The examples ran on TShark 4.4.1 against a
generated capture.

## When to use it
- Hunting encodings: UTF-16 file names, overlong UTF-8, mixed-case Host headers used to evade
  filters (compare the exact bytes with `@`).
- Bit fields where you need reserved bits that named sub-fields hide.
- Comparing with byte patterns from an IDS signature.

## Gotchas
- Not available before 4.2; tshark on old servers will reject the filter.
- Generated fields such as `tcp.stream` have no bytes of their own: `@tcp.stream == 00` matched nothing on a capture where
  `tcp.stream == 0` matched seven packets.
- Matching is literal: compression pointers in DNS mean `@dns.resp.name` may contain a pointer
  (c0:0c) rather than the full name (in the test capture `@dns.resp.name == c0:0c` did not match, so do not rely on a
  particular pointer value).

## Verify
- [ ] `tshark -Y "@field ..." -T fields -e field` returns the packets you expect on a sample file.
