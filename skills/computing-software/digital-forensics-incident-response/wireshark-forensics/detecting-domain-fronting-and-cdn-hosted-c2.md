---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.detecting-domain-fronting-and-cdn-hosted-c2
name: detecting-domain-fronting-and-cdn-hosted-c2
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [domain-fronting-detection, cdn-c2, c2-detection, tls-inspection, network-forensics, dfir]
level: advanced
status: draft
description: "Detect domain fronting and CDN-hosted C2: SNI versus HTTP Host mismatch with TLS inspection, CDN-specific behaviour, beacon patterns to CDN edges and proxy-log hunting."
sources: ["https://attack.mitre.org/techniques/T1090/004/", "https://www.bamsoftware.com/papers/fronting/", "https://www.zscaler.com/blogs/security-research", "https://www.wireshark.org/docs/dfref/h/http.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Detecting domain fronting and CDN-hosted C2

Domain fronting (T1090.004) puts a reputable domain in DNS and the TLS SNI, and the real C2 hostname in the encrypted HTTP `Host` header; the CDN routes by Host. Many CDNs now block mismatches (AWS CloudFront, Google, Azure Front Door blocked or restricted it from 2018 to 2024), but variants persist: CDN-hosted C2 on the attacker's own CDN subdomain, "domain hiding" via ESNI/ECH, and fronting through providers that still allow it.

## Detection with TLS inspection (proxy/SSE or lab decryption)
- Compare SNI to HTTP Host for each request:
```text
tls.handshake.extensions_server_name && http.host     # in a decrypted capture
```
In proxy logs, fields like `sni` vs `host` or `cs-host` vs certificate CN; flag `sni != host` where both belong to a CDN.
- Requests to CDN edges with Host values that are random subdomains of CDN domains (`d1abc2xyz.cloudfront.net`, `*.azureedge.net`, `*.workers.dev`).

## Without inspection
- **Beaconing to CDN IPs** from a single host with regular timing and small, consistent sizes; most CDN traffic is bursty browsing.
- **SNI is a high-reputation domain but the process is not a browser** (EDR network events give process names).
- **DNS**: lookups for the fronted domain without the corresponding browsing pattern (no referenced assets, no other domains loaded around it).
- **JA3/JA4 fingerprints** of known C2 frameworks (Cobalt Strike, Sliver, Mythic agents) to CDN IPs.
- Long-lived connections or high POST ratio to CDN endpoints.

## Investigation steps
1. Identify the CDN (ASN, certificate issuer) and the fronted domain.
2. Pull proxy/SSE logs with Host and SNI for the source host over time.
3. On the host, find the process (EDR, Sysmon 3/22) and its config (C2 profile in memory: Cobalt Strike Beacon config parsers show `host` header values).
4. Request the CDN provider take down the attacker's distribution via abuse channels; block the specific Host values at the proxy.

## Gotchas
- Legitimate SaaS uses shared CDN certificates with many names; mismatch between SNI and certificate CN is normal; SNI vs Host mismatch is the signal.
- Blocking the fronted domain (e.g. a major site) is rarely possible; block by Host with inspection or by the process on the endpoint.

## Verify
Each suspected fronting session is supported by SNI/Host evidence from inspection or by the implant's configuration showing the real Host value.
