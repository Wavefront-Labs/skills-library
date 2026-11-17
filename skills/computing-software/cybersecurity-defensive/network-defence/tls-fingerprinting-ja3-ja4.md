---
id: computing-software.cybersecurity-defensive.network-defence.tls-fingerprinting-ja3-ja4
name: tls-fingerprinting-ja3-ja4
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [tls-fingerprinting, ja3, ja4, ja4plus, zeek, encrypted-traffic, threat-hunting]
level: practitioner
status: docs-checked
description: "Use JA3 and JA4+ TLS fingerprints to spot unusual clients in encrypted traffic: what each method is, licensing, available tooling, hunting approach and limits."
sources: ["https://github.com/FoxIO-LLC/ja4"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS fingerprinting (JA3 / JA4)

**Goal:** identify which client software made an encrypted connection (browser, script, malware family) from the TLS handshake, without decryption.

## Fingerprints
- **JA3**: the earlier TLS client fingerprint. Chromium began randomising extension order in 2023, which defeats JA3.
- **JA4** (FoxIO JA4+ suite): TLS client fingerprint that sorts extensions (and ciphers), so randomisation and cipher stunting do not change it; signature algorithms are included so fingerprints stay distinctive after sorting.
- Other JA4+ methods: **JA4S** (TLS server response), **JA4H** (HTTP client), **JA4X** (X.509 certificate), **JA4SSH**, **JA4T/JA4TS** (TCP), **JA4L/JA4LS** (latency), **JA4D/JA4D6** (DHCP), **JA4N** (NTP).
- Licensing: JA4 (TLS client) is BSD 3-Clause like JA3. The other JA4+ methods are under the FoxIO License 1.1, which permits academic and internal business use but not monetisation; check before putting them in a product.

## Collect
The FoxIO repository lists Wireshark (C plugin) and Zeek (plugin) support, lists Suricata support as under development, and recommends Arkime. Check each tool's current documentation for how to enable it.

## Use
1. Baseline fingerprints per network segment: browsers, OS updaters, known agents.
2. Hunt rare fingerprints: seen on very few hosts, especially with uncommon destinations or beacon-like timing.
3. Look fingerprints up in the official JA4 database (ja4db.com), which maps fingerprints to applications; treat matches as leads, not verdicts.
4. Combine client (JA4), server (JA4S) and certificate (JA4X) fingerprints when examining a suspect server.

## Gotchas
- Unrelated programs can share a fingerprint (same TLS library), so a match alone has a false-positive rate.
- A client can imitate another's handshake; a missing match proves nothing.
- A TLS inspection proxy re-originates connections, so fingerprint before the proxy if you need the original client.

## Verify
- [ ] Fingerprint fields populated in logs for a test connection from a known client.
- [ ] Hunts based on rare fingerprints documented with outcomes.

## Checked
2026-11-01. Confirmed in the FoxIO JA4 repository README: list of JA4+ methods, BSD 3-Clause for JA4 and FoxIO License 1.1 for the others, extension and cipher sorting versus 2023 Chromium randomisation, ja4db.com, Wireshark/Zeek/Suricata/Arkime support statements.
Removed: example fingerprint string, the Zeek package install command, Suricata keyword and EVE settings, cloud WAF support, Cobalt Strike/Sliver profile claims and the uTLS claim (not on the page read).
Method: documentation only; no commands were run.
