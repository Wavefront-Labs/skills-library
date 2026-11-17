---
id: computing-software.blockchain-and-web3.ethereum-evm.websocket-subscriptions
name: websocket-subscriptions
category: computing-software
field: blockchain-and-web3
product: ethereum-evm
tags: [eth-subscribe, newheads-subscription, ws-reconnect]
level: practitioner
status: draft
description: "Subscribe to new heads and logs over WebSocket and recover cleanly from disconnects."
sources:
  - https://ethereum.org/en/developers/docs/apis/json-rpc/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Subscriptions
- `eth_subscribe` with `newHeads`, `logs` (with filter), `newPendingTransactions` over WS.
- Subscriptions die with the connection. On reconnect, backfill with `eth_getLogs` from the last processed block to avoid gaps.
- During reorgs, `logs` notifications arrive with `removed: true`; undo effects for those.
- Keep a heartbeat (periodic `eth_blockNumber`) to detect half-open sockets.

## Verify
- [ ] Kill the socket mid-run; after reconnect there are no missing or duplicated events.
