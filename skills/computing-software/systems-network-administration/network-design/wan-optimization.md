---
id: computing-software.systems-network-administration.network-design.wan-optimization
name: wan-optimization
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, wan-optimization, deduplication, tcp-optimization, caching, riverbed]
level: practitioner
status: docs-checked
description: "Decide when WAN optimisation still helps: deduplication, compression, TCP proxying and protocol acceleration, versus TLS everywhere and SaaS making it ineffective."
sources:
  - https://www.riverbed.com/products/steelhead/
  - https://www.cisco.com/c/en/us/td/docs/routers/sdwan/configuration/appqoe/ios-xe-17/appqoe-book-xe.html
  - https://www.rfc-editor.org/rfc/rfc3135
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WAN optimisation

## Techniques
| Technique | What it does | Still effective when |
|---|---|---|
| Data deduplication (byte caching) | replaces repeated byte patterns with references between peers | same files repeatedly crossing the WAN (CAD, replication) and traffic not encrypted end-to-end, or decrypted by the device |
| Compression | on the fly | uncompressed protocols |
| TCP optimisation / PEP (RFC 3135) | TCP-level proxying to mitigate link-related degradations | high-latency links (satellite, intercontinental) |
| Application acceleration | protocol-specific acceleration | chatty file-sharing protocols over long RTT |

## Reality check
- Most traffic is now TLS to SaaS; dedup cannot see inside without TLS interception, and the
  optimiser needs a peer near the server (impossible for SaaS).
- Cloud alternatives: local caches,
  CDN, moving the application closer to users, VDI.

## When to deploy
Long-RTT sites with heavy file/replication between your own data centres or to a known peer;
satellite links; storage replication not already deduplicated. Measure a pilot: compare
throughput and data reduction in the device reports before buying fleet-wide.

## Design notes
Inline vs out-of-path deployment; RFC 3135 treats asymmetric routing as a PEP issue; plan HA and bypass; exclude real-time traffic.

## Verify
- [ ] Pilot report shows data reduction and transfer-time improvement for the target applications, not just total bytes.

## Checked

- Date: 2026-10-28
- Confirmed: RFC 3135: Performance Enhancing Proxies are used to improve degraded TCP performance caused by link characteristics (satellite links are an example), and the RFC has an asymmetric routing section.
- Removed: TCP feature names, SMB/MAPI claims, FEC row, BBR, cache product names, WCCP/PBR.
Method: documentation only; no commands were run.
