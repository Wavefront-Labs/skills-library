---
id: computing-software.systems-network-administration.wireshark.testing-capture-filters-bpf-compile
name: testing-capture-filters-bpf-compile
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, bpf-compile, capture-filter, bpf, dumpcap, tcpdump, filter-debugging]
level: practitioner
status: verified
description: "Validate and debug capture filters before a long capture: compile to BPF with dumpcap -d and tcpdump -d, read the instructions, and test against a saved file."
sources:
  - https://www.tcpdump.org/manpages/pcap-filter.7.html
  - https://www.wireshark.org/docs/man-pages/dumpcap.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing capture filters

A wrong capture filter is worse than none: the traffic you needed is gone forever. Validate first.

## Syntax check by compiling
```
dumpcap -i <interface> -f "tcp port 443 and host 10.0.0.5" -d
```
A syntax error prints `dumpcap: Invalid capture filter "..." for interface '...'` (checked with `"tcp port 443 or 53 and"` and with the
display-filter syntax `"tcp.port == 443"`). Success prints `Capturing on '<name>'` and the BPF program:
```
(000) ldh      [12]
(001) jeq      #0x86dd          jt 2    jf 8
...
(008) jeq      #0x800           jt 9    jf 19
```
Reading the program shows what the filter really matches. For `tcp port 443` the output on TShark/dumpcap 4.4.1 had an IPv6 branch
(ethertype 0x86dd, next header 6 at offset 20, ports at 54 and 56, so no IPv6 extension headers are followed) and an IPv4 branch
(`jset #0x1fff` drops non-first fragments, ports found via the IP header length). A hand-written byte offset filter only handles what you wrote.

The link type matters: compile on the interface you will capture (`-i`); the error message above names the interface the filter was
compiled for, and offsets such as `[12]` assume Ethernet.

## Test against existing traffic
Capture filters apply to live capture only: `tshark -r file -f tcp` is refused with `Only read filters, not capture filters, can be
specified when reading a capture file`. To compare, apply the equivalent display filter and check the count:
```
tshark -r sample.pcap -Y 'ip.addr == 10.0.0.5 && tcp.port == 443' -w filtered.pcap
capinfos -c filtered.pcap
```

## Common mistakes
| Wrong | Right | Why |
|---|---|---|
| `host 10.0.0.5 and not port 22 or port 3389` | `host 10.0.0.5 and not (port 22 or port 3389)` | `and`/`or` have equal precedence and group left to right; the two filters compiled to different programs (46 vs 28 output lines) |
| `vlan 20 and host x` on mixed traffic | add `or host x` for untagged traffic | the program starts by testing for ethertype 0x8100/0x88a8, so untagged packets cannot match |
| `tcp.port == 443` | `tcp port 443` | display filter syntax is rejected as an invalid capture filter |
| `ip host name` with IPv6 traffic | `host name` | per pcap-filter(7), `ip host` ignores IPv6 addresses; unqualified `host` covers both families |

Not a mistake: `port 53 or 443` is valid, because pcap-filter(7) lets identical qualifier lists be omitted (`tcp dst port ftp or ftp-data or domain`)
and it compiled without error.

## Gotchas
- Quote the filter in the shell; `()` and `!` are shell characters.
- A filter that compiles is not necessarily the one you meant; read the program or test the equivalent display filter on sample data.

## Verify
- [ ] `dumpcap -d` compiles with no error on the target interface.
- [ ] A test run of a few seconds captures the expected packets (`capinfos -c`).
