---
id: computing-software.systems-network-administration.wireshark.display-filter-functions
name: display-filter-functions
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, display-filter, display-filter-functions, len, upper, lower, count, string, dfilter-macros]
level: practitioner
status: verified
description: "Use Wireshark display filter functions len(), count(), upper(), lower(), string() and field arithmetic to find odd packets that plain comparisons cannot."
sources:
  - https://www.wireshark.org/docs/man-pages/wireshark-filter.html
  - https://www.wireshark.org/docs/wsug_html_chunked/ChWorkBuildDisplayFilterSection.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Display filter functions

Functions wrap a field in a display filter. Names and availability follow
`man wireshark-filter` for your version (4.x added arithmetic and more functions).

| Function | Example | Finds |
|---|---|---|
| `len()` | `len(http.request.uri) > 500` | long URIs (injection attempts, tracking junk) |
| `len()` on bytes | `len(dns.qry.name) > 60` | long DNS names (tunnelling) |
| `count()` | `count(ip.addr) > 2` | tunnelled packets (IP in IP/GRE/VXLAN) |
| `upper()`/`lower()` | `lower(http.host) contains "login"` | case-insensitive host match |
| `string()` | `string(frame.number) matches "[05]$"` | every packet whose number ends in 0 or 5 (sampling) |
| `abs()`, `min()`, `max()` | `max(tcp.srcport, tcp.dstport) <= 1024` | (4.0+) both ports privileged; arguments must have the same type |
| `vals()` | `vals(pfcp.msg_type) contains "Request"` | match the value-string text shown in columns (man page example) |
| `dec()`/`hex()` | see man page | unsigned integer to decimal/hex string |

Arithmetic (4.0+): `tcp.window_size_value * 2 < 1000`, `frame.len - ip.len > 20`; group with `{ }`, not parentheses.
Field references: `ip.src == ${ip.dst}` uses the value from the packet selected in the GUI (matches nothing in tshark).

## Case-insensitive alternatives
`http.host matches "(?i)example"` (PCRE2) is often simpler than `lower()`. `contains` is
case-sensitive.

## Macros
Analyze > Display Filter Macros: a macro's text uses `$1`, `$2`... for arguments and is invoked as `$name(a,b)` or
`${name:a;b}` (User's Guide example: macro `tcp_conv` used as `$tcp_conv(10.1.1.2,10.1.1.3,1200,1400)`). Macros work in
saved display filters and filter buttons, not capture filters.

## Gotchas
- A function on a missing field is false, not an error: `len(http.request.uri) < 10` does
  not match non-HTTP packets.
- In tshark a bad filter fails at once with a syntax error: `tshark -r x.pcap -Y '<filter>'`.

## Verify
- [ ] `tshark -r cap.pcapng -Y '<filter>' -T fields -e frame.number` accepts the filter and the frame list is plausible; spot check a few packets.
