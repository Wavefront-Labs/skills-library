---
id: computing-software.blockchain-and-web3.bitcoin.bitcoin-core-node-config
name: bitcoin-core-node-config
category: computing-software
field: blockchain-and-web3
product: bitcoin
tags: [bitcoin-conf, pruned-node, txindex, bc-btc-node]
level: practitioner
status: gated
description: "Configure a full or pruned Bitcoin Core node: data dir, bitcoin.conf, pruning, indexes and network exposure."
sources:
  - https://github.com/bitcoin/bitcoin/blob/master/doc/bitcoin-conf.md
  - https://bitcoin.org/en/full-node
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node configuration
- Pruned mode reduces disk use (bitcoin.org full-node guide: from over 750 GB to around 7 GB); the minimum prune value above 0 is 550 (MiB), and 0 disables pruning.
- A pruned node is incompatible with `-txindex` and `-rescan`, and disables the `importwallet` RPC.
- Inbound connections use port 8333; configure router and firewall to allow it if you want to accept peers.
- The `bitcoin.conf` options `server`, `rpcbind`, `rpcallowip`, `dbcache`, the initial-sync time and size, `backupwallet` and the RPC-on-localhost advice: not listed on the bitcoin-conf page that was read (gated: unconfirmed, source is paywalled or blocked). Read the current Bitcoin Core configuration docs before relying on them.

## Verify
- [ ] `getblockchaininfo` shows the expected pruned value.

## Checked

2026-11-02. Confirmed against bitcoin.org full-node guide (prune sizes, 550 minimum, txindex incompatibility, port 8333). Gated: the other bitcoin.conf options and sync figures; the bitcoin-conf page read does not list them, so the source was read but did not state them.
Method: documentation only; no commands were run.
