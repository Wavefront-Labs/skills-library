---
id: computing-software.cybersecurity-defensive.suricata.ip-tcp-icmp-header-keywords
name: ip-tcp-icmp-header-keywords
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [ttl, tcp-flags, itype, geoip, fragbits]
level: practitioner
status: docs-checked
description: "Match packet headers: ttl, ipopts, fragbits, tos, geoip, tcp.flags, seq, window, tcp.mss, itype, icode and header sticky buffers."
sources: ["https://docs.suricata.io/en/latest/rules/header-keywords.html", "https://docs.suricata.io/en/latest/rules/differences-from-snort.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Header keywords

**IP:** `ttl`, `tos` (hex with `x` prefix), `ipopts` (rr, ts, lsrr, ssrr, rtralt, any; at rule start), `sameip`, `ip_proto`, `id`, `fragbits:[*+!=]<[MDR]>` (rule start), `fragoffset`, `geoip: src|dst|both|any,<country codes>` (needs libmaxminddb and a GeoIP2 or GeoLite2 database in YAML).

**TCP:** `tcp.flags:[modifier]<FSRPAUCE0>[,<ignore flags>]` (modifiers `+`, `*`, `!`/`-`, `=`), `seq`, `ack`, `window`, `tcp.mss` and `tcp.wscale` (range, comparison or value), `tcp.hdr` sticky buffer.

**ICMP:** `itype`, `icode` (`min<>max` or `<`/`>`), `icmp_id`, `icmp_seq` (network byte order), `icmpv6.mtu`, `icmpv4.hdr`, `icmpv6.hdr`.

**Other buffers:** `udp.hdr`, `igmp.hdr`, `igmp.type`, `igmp-csum`, `ether.hdr`, `ipv4.hdr`, `ipv6.hdr`.

Suricata does not mix packet keywords (`dsize`, `flags`, `ttl`) with stream keywords (`http_*`) in one rule.

## Checked

2026-11-04. Confirmed against the Header Keywords page (ipopts, geoip, fragbits, tos, tcp.flags, tcp.mss, tcp.wscale, itype, icode, icmp_seq) and Differences From Snort (packet versus stream keywords).

Method: documentation only; no commands were run.
