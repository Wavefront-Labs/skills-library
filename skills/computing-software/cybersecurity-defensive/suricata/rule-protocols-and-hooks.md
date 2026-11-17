---
id: computing-software.cybersecurity-defensive.suricata.rule-protocols-and-hooks
name: rule-protocols-and-hooks
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [rule-protocol, tcp-pkt, tcp-stream, rule-hooks]
level: practitioner
status: docs-checked
description: "Choose the protocol field of a rule: ip, tcp, udp, icmp, app-layer names, tcp-pkt versus tcp-stream, pkthdr, and Suricata 8 hooks."
sources: ["https://docs.suricata.io/en/latest/rules/intro.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Rule protocols

- Network: `ip`, `tcp`, `udp`, `icmp`, `icmpv4`, `icmpv6`, `ipv4`/`ip4`, `ipv6`/`ip6`, `ether`, `arp`.
- `pkthdr`: decoder-event rules. Before Suricata 8 it aliased `ip`; in 9 it is only for decoder events.
- `tcp-pkt` matches content in individual packets; `tcp-stream` only in reassembled streams.
- Application layer: about three dozen (`http`, `tls`, `dns`, `smb`, `ssh`, `smtp`, `quic`...). Some, such as `modbus`, `dnp3` and `enip`, are disabled by default.

List what your build supports with `suricata --list-rule-protos`. Availability follows suricata.yaml, and an `http` rule matches only when the stream carries HTTP.

Suricata 8 added explicit hooks written `<proto>:<hook>`, for example `http1:request_started`, which also work in IDS and IPS rules.

## Checked

2026-11-08: read in full against the OISF/suricata doc/userguide rst source (rules/intro) read in full; the claims, names, values and examples left in this skill match the page text. Replaced the unsupported count of application protocols with a loose one.

Method: documentation only; no commands were run.
