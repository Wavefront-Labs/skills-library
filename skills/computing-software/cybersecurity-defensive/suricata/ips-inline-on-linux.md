---
id: computing-software.cybersecurity-defensive.suricata.ips-inline-on-linux
name: ips-inline-on-linux
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [ips, nfqueue, iptables, af-packet-ips]
level: practitioner
status: docs-checked
description: "Run Suricata inline on Linux: NFQUEUE with iptables or nftables, queue balancing and bypass, and AF_PACKET copy-mode ips with copy-iface."
sources: ["https://docs.suricata.io/en/latest/ips/setting-up-ipsinline-for-linux.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Inline IPS on Linux

## NFQ
- Confirm NFQ in `suricata --build-info`; start with `-q 0`.
- Gateway: `iptables -I FORWARD -j NFQUEUE`. Host: use INPUT and OUTPUT. Narrow by protocol, port, `-i` and `-o`. `ip6tables` for IPv6. Verify with `iptables -vnL`.
- If Suricata stops while rules remain, traffic stops; `iptables -F` restores it.
- nftables: a dedicated chain hooked at forward, priority 10, with a `queue` statement.
- Balancing: `queue num 3-5` with `suricata -q 3 -q 4 -q 5`; `fanout` maps by CPU; `bypass` makes the rule behave like ACCEPT when nothing listens (no blocking).

## AF_PACKET IPS
No firewall rules. `copy-mode: ips` (or `tap`) and `copy-iface` per interface, with distinct `cluster-id`s, matching MTU, offloading off and `defrag: no`. Multi-thread: `cluster_ebpf`.

Set `stream.inline` to `auto` or `yes`.

## Checked

2026-11-08: read in full against the OISF/suricata doc/userguide rst source (ips/setting-up-ipsinline-for-linux) read in full; the claims, names, values and examples left in this skill match the page text. Nothing else was removed.

Method: documentation only; no commands were run.
