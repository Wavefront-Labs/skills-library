---
id: computing-software.systems-network-administration.wireshark.display-filter-field-existence-and-not-equal
name: display-filter-field-existence-and-not-equal
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, display-filter, field-existence, not-equal-operator, any-all-quantifiers, filter-pitfalls]
level: practitioner
status: verified
description: "Avoid the classic display filter traps: field existence tests, why ip.addr != x matches almost everything, !== and all/any quantifiers, and negating whole expressions."
sources:
  - https://www.wireshark.org/docs/man-pages/wireshark-filter.html
  - https://www.wireshark.org/docs/wsug_html_chunked/ChWorkBuildDisplayFilterSection.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Field existence and != pitfalls

## Existence
A bare field name is true if the field exists in the packet:
```
tcp.analysis.retransmission
http.request
dns.flags.rcode            # any DNS response (has an rcode field)
!tcp                       # non-TCP packets
```
Field present with value 0 is still true for existence; test values explicitly
(`dns.flags.rcode != 0`).

## Multi-occurrence fields
`ip.addr`, `tcp.port`, `eth.addr` appear twice per packet (source and destination). Comparisons
default to "any occurrence matches":
```
ip.addr == 10.0.0.5        # src OR dst is 10.0.0.5  (what you want)
ip.addr != 10.0.0.5        # version dependent, see below
```
- Wireshark before 3.6: `a != b` meant "any occurrence not equal", so `ip.addr != 10.0.0.5` was
  true for almost every packet (the other address differs). Old guides warn about this.
- Wireshark 3.6 and later: `a != b` is defined as `!(a == b)` ("all not equal", alias `all_ne`). In 3.6 the old
  any-not-equal logic was `a ~= b` or `any_ne`; from 4.0 it is written `!==` (alias `any_ne`) and `~=` is a syntax error.
  Do not read `!==` as an alias of `!=`: on 4.4.1 `ip.addr !== 10.0.0.5` matched every IPv4 packet in a test file.
- 4.x accepts explicit quantifiers: `any ip.addr != x`, `all ip.addr != x`, plus `===` (all equal).

Portable exclusion that works on every version:
```
!(ip.addr == 10.0.0.5)
```
Check the version (`tshark -v`) before trusting a filter copied from an old article.

## Tunnels make it worse
In GRE/VXLAN/IPsec-decrypted traffic a packet can carry several `ip.addr` pairs. `ip.addr == x`
matches outer or inner. Use the layer operator (`ip.addr#2 == x`) for the inner header. With `!=` the
"all" rule means a tunnelled packet is kept only if none of its addresses equals x.

## Negating compound expressions
```
!(tcp.port == 22 || tcp.port == 3389)
not (arp or dns or icmp)
```
De Morgan applies; parentheses avoid surprises because `!` binds tighter than `&&`.

## Strings and case
`http.host == "Example.com"` is case-sensitive (it did not match a `Login.Example.com` host); use `lower(http.host) == "example.com"` or
`http.host matches "(?i)example\\.com"`. In a double-quoted filter string the
regex backslash must be doubled: `"login\.example"` is rejected with `\. is not a valid character escape sequence`.

## Verify
- [ ] `tshark -r cap.pcapng -Y '<filter>'` accepts the filter (no syntax error) and the packet count changes as
  expected when you add or remove the negation.
- [ ] For exclusions, spot-check a packet from the excluded host is really gone (`ip.addr == x`
  count vs total).
