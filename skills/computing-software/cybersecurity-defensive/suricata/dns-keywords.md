---
id: computing-software.cybersecurity-defensive.suricata.dns-keywords
name: dns-keywords
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [dns-query, dns-opcode, dns-rrtype, dns-rcode, rrname]
level: practitioner
status: docs-checked
description: "Match DNS: dns.query, dns.opcode, dns.rcode, dns.rrtype and the Suricata 8 rrname buffers for query, answer, authority and additional records."
sources: ["https://docs.suricata.io/en/latest/rules/dns-keywords.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# DNS keywords

- `dns.query`: sticky buffer for query names in requests only (old `dns_query`). The buffer is the literal name without length bytes or terminating NULL, such as `mail.google.com`.
- `dns.opcode`: unsigned 8-bit; value, negation or range (`dns.opcode:7-15;`).
- `dns.rcode`: 8-bit, accepts enumeration names; only values 0 to 15 supported now.
- `dns.rrtype`: 16-bit, multi-integer, accepts enumeration names.
- Since 8.0.0, sticky buffers for names in records, covering both directions (use `flow` to restrict) with multi-buffer matching: `dns.queries.rrname`, `dns.answers.rrname`, `dns.authorities.rrname`, `dns.additionals.rrname`.
- `dns.response.rrname`: names and rdata across all response sections; rdata only for CNAME, PTR, MX, NS and SOA (mname).

Domain suffix matching combines `dotprefix` with `endswith`.

## Checked

2026-11-04. Every keyword above confirmed against the Suricata DNS Keywords page; the `dotprefix` plus `endswith` example is on the Transformations page.

Method: documentation only; no commands were run.
