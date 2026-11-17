---
id: computing-software.cybersecurity-defensive.network-defence.ja4-tls-fingerprinting-for-network-monitoring
name: ja4-tls-fingerprinting-for-network-monitoring
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [ja4-fingerprinting, ja4, tls-fingerprinting, network-security-monitoring, zeek, suricata]
level: practitioner
status: draft
description: "Use JA4 TLS client fingerprints in Zeek, Suricata and Wireshark for hunting and baselining, and read the JA4 string safely as a signal, not a verdict."
sources: ["https://github.com/FoxIO-LLC/ja4"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# JA4 TLS fingerprinting

**Goal:** identify classes of TLS clients on the wire without decrypting, to spot unknown software and baseline fleets.

## Format
`JA4 = a_b_c`, for example `t13d1516h2_8daaf6152771_b186095e22b6`:
- a: protocol (`t` TCP, `q` QUIC), TLS version, SNI present (`d` domain, `i` no SNI), cipher count, extension count, first ALPN.
- b: truncated SHA-256 of the sorted cipher list.
- c: truncated SHA-256 of sorted extensions plus signature algorithms.
Sorting makes it stable under extension-order randomisation that broke JA3. The wider JA4+ family (server JA4S, HTTP JA4H, certificate JA4X, SSH, TCP) exists; JA4 itself is permissively licensed, other members use a FoxIO licence - check before embedding.

## Tooling
- Zeek: the FoxIO JA4 package adds `ja4` to `ssl.log`.
- Suricata (7.x recent): `ja4` rule keyword and EVE logging (`ja4.hash`), enabled per `tls` EVE settings.
- Wireshark (4.x recent): field `tls.handshake.ja4`; filter `tls.handshake.ja4 == "..."`.
Confirm exact versions and config in each project's docs.

## Use
1. Collect a week of fingerprints per subnet; build a baseline of known (browsers, agents, update clients).
2. Alert on rare fingerprints talking to many hosts or to rare destinations; enrich with SNI, destination reputation, JA4S.
3. Map known-good tools to fingerprints in a watch list; treat matches to a known-bad list as a lead.

## Limits
A fingerprint identifies a TLS stack, not intent. Proxies, shared libraries and updated browsers change it. Attackers can mimic. Use it with other signals; never auto-block on it alone. ECH may hide parts of the handshake.

## Verify
Capture your own browser traffic; the logged JA4 matches the Wireshark value for the same flow.
