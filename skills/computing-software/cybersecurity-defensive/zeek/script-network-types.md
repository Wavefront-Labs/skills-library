---
id: computing-software.cybersecurity-defensive.zeek.script-network-types
name: script-network-types
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, addr-type, subnet-type, port-type, count-type]
level: intro
status: docs-checked
description: "Zeek network types: addr and IPv6 bracket syntax, subnet masking and membership, port with protocol suffix, and count as unsigned 64-bit."
sources: ["https://docs.zeek.org/en/current/reference/zeekscript/types.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# network and numeric types

**addr**: IPv4 as `A1.A2.A3.A4`; IPv6 in square brackets, such as `[2001:db8::1]`. IPv4-mapped IPv6 (`[::ffff:192.168.1.100]`) equals the IPv4 address. Supports `==`, `!=`, and ordering. The absolute value gives size in bits (32 or 128). Use `is_v4_addr` and `is_v6_addr`.

**subnet**: CIDR such as `192.168.0.0/16` or `[fe80::]/64`. Mask an address with `/` and test inclusion with `in`:

```
local a: addr = 192.168.1.100;
local s: subnet = 192.168.0.0/16;
if ( a/16 == s ) print "true";
if ( a in s ) print "true";
```

**port**: an unsigned integer followed by `/tcp`, `/udp`, `/icmp` or `/unknown`. For ICMP the source port is the message type and destination the code. Ordering across protocols is unknown < tcp < udp < icmp, so `65535/tcp` is smaller than `0/udp`. Use `get_port_transport_proto` and `port_to_count`.

**count**: 64-bit unsigned; literals without a unary sign are `count`. Overflow wraps modulo 2^64. Hex is `0xff`. Bitwise `&`, `|`, `^`, `<<`, `>>` and `~` work. A unary plus or minus on a count gives an `int`.

Pitfall from the page: `|5 - 9|` is unsigned overflow giving 18446744073709551612, while `|+5 - +9|` uses signed arithmetic and gives 4.

## Checked

2026-11-08. Read the Types page in full; every claim confirmed.

Method: documentation only; no commands were run.
