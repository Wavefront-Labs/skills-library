---
id: computing-software.blockchain-and-web3.consensus-and-protocols.eclipse-and-sybil-defences
name: eclipse-and-sybil-defences
category: computing-software
field: blockchain-and-web3
product: consensus-and-protocols
tags: [eclipse-attack-defence, sybil-resistance, peer-diversity]
level: advanced
status: draft
description: "Configure nodes to resist eclipse attacks: diverse peers, anchors, trusted peers and avoiding single-provider reliance."
sources:
  - https://ethereum.org/en/developers/docs/networking-layer/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Eclipse and Sybil defence
- Threat: an attacker fills a node's peer slots so it sees a false chain. Mitigate with several outbound connections to diverse networks/ASNs, persisted peer tables or anchor connections, and not relying on one RPC provider.
- Cross-check against an independent source (second RPC provider or explorer) when handling large values.
- Keep inbound slots limited; prefer well-known bootnodes plus your own trusted peers.
- Bitcoin Core opens a few block-relay-only connections to reduce topology leakage.

## Verify
- [ ] Your service alerts if its chain head diverges from a second provider by more than a few blocks.
