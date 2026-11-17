---
id: computing-software.blockchain-and-web3.consensus-and-protocols.running-a-node-and-staking-hygiene
name: running-a-node-and-staking-hygiene
category: computing-software
field: blockchain-and-web3
product: consensus-and-protocols
tags: [ethereum-node-setup, engine-api, staking-key-separation]
level: advanced
status: draft
description: "Set up execution plus consensus clients with JWT auth, and keep withdrawal credentials and signing keys separated."
sources:
  - https://ethereum.org/en/developers/docs/nodes-and-clients/run-a-node/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running a node
- Run one execution client and one consensus client; connect them via the Engine API (port 8551) authenticated with a shared JWT secret file.
- Expose RPC only on localhost or behind authentication; never expose the Engine API.
- Resources: fast NVMe SSD, adequate RAM and bandwidth; sync times and disk sizes vary by client and mode, check client docs.
- Use checkpoint sync for the consensus client to start from a recent finalized state.
- Staking: signing keys live on the validator machine; withdrawal credentials should point to a secure cold address. Diversify client software.

## Verify
- [ ] `eth_syncing` returns false and the consensus client reports synced with peers.
