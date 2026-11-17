---
id: computing-software.blockchain-and-web3.consensus-and-protocols.gossip-discovery-and-mempool
name: gossip-discovery-and-mempool
category: computing-software
field: blockchain-and-web3
product: consensus-and-protocols
tags: [p2p-gossip, peer-discovery, mempool-policy, bc-con-p2p]
level: practitioner
status: draft
description: "Explain how nodes find peers, gossip transactions and blocks, and how mempool policy differs from consensus rules."
sources:
  - https://ethereum.org/en/developers/docs/networking-layer/
  - https://developer.bitcoin.org/devguide/p2p_network.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# P2P and mempool
- Discovery: DNS seeds and addr gossip (Bitcoin); discv5/ENR and bootnodes (Ethereum). Transport: devp2p/RLPx on the execution layer, libp2p gossipsub on the consensus layer.
- Transactions propagate by announcement then request; blocks by compact relay.
- Mempool policy (minimum fee, standardness, size limits, replacement rules) is local node policy; consensus rules decide block validity. A transaction can be valid but not relayed.
- Tune: `maxconnections`, `maxmempool` (Bitcoin); client flags for peer counts (Ethereum).
- Private relays bypass the public mempool.

## Verify
- [ ] `getpeerinfo` or `admin_peers` shows a healthy set of inbound/outbound peers.
